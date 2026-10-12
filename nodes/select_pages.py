
"""Select relevant annual report pages using template metrics."""

import re
from collections.abc import Mapping
from config import get_settings
from graph.graph_state import FinancialGraphState
from prompts.selected_keywords import (
    normalize_text,
    numeric_density,
    page_score,
    table_structure_score,
)


CONTINUATION_MARKERS = (
    "continued",
    "continuation",
    "carried forward",
    "brought forward",
)

METRIC_SYNONYM_GROUPS = (
    ("revenue", "turnover"),
    ("total revenue", "total sales", "total turnover"),
    ("cost of sales", "cost of goods sold", "cogs"),
    (
        "profit before tax",
        "income before tax",
        "earnings before tax",
        "pbt",
    ),
    ("profit after tax", "net profit after tax", "pat"),
    ("profit for the year", "profit for the period"),
    ("cash and cash equivalents", "cash equivalents"),
    ("trade receivables", "accounts receivable", "trade debtors"),
    ("trade payables", "accounts payable", "trade creditors"),
    (
        "property plant and equipment",
        "property and equipment",
        "tangible fixed assets",
        "ppe",
    ),
    ("current assets", "short term assets"),
    ("non current assets", "noncurrent assets", "long term assets"),
    ("current liabilities", "short term liabilities"),
    (
        "non current liabilities",
        "noncurrent liabilities",
        "long term liabilities",
    ),
    ("operating profit", "operating income"),
    ("borrowings", "financial borrowings"),
    ("lease liabilities", "lease obligations"),
    ("shareholders equity", "shareholders funds"),
    ("retained earnings", "accumulated profits"),
    (
        "depreciation and amortisation",
        "depreciation and amortization",
    ),
)

def _to_page_record(page, index):
    if isinstance(page, Mapping):
        record = dict(page)
        raw_metadata = record.get("metadata")
        text = record.get("text")

        if text is None:
            text = record.get("page_content", "")
    else:
        raw_metadata = getattr(page, "metadata", None)
        text = getattr(page, "page_content", "")
        record = {}

    metadata = (
        dict(raw_metadata)
        if isinstance(raw_metadata, Mapping)
        else {}
    )

    text = str(text or "")

    def to_int(value):
        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    existing_number = to_int(record.get("page_number"))
    metadata_page = to_int(metadata.get("page"))
    metadata_page_number = to_int(metadata.get("page_number"))

    if existing_number is not None and existing_number >= 1:
        page_number = existing_number
    elif metadata_page is not None and metadata_page >= 0:
        page_number = metadata_page + 1
    elif (
        metadata_page_number is not None
        and metadata_page_number >= 1
    ):
        page_number = metadata_page_number
    else:
        page_number = index + 1

    metadata["page_number"] = page_number

    record["metadata"] = metadata
    record["text"] = text
    record["page_content"] = text
    record["page_number"] = page_number

    return record

def _contains_term(normalized_text, term):
    if not normalized_text or not term:
        return False

    if term in ("current assets", "current liabilities"):
        pattern = (
            r"(?<!non )(?<!\w)"
            + re.escape(term)
            + r"(?!\w)"
        )
    else:
        pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"

    return re.search(pattern, normalized_text) is not None


def _metric_terms(variable):
    base_term = normalize_text(variable)

    if not base_term:
        return set()

    terms = {base_term}

    for group in METRIC_SYNONYM_GROUPS:
        normalized_group = {
            normalize_text(term)
            for term in group
        }

        if base_term in normalized_group:
            terms.update(normalized_group)

    return terms


def _build_template_metrics(excel_data):
    template_metrics = []

    for metric in excel_data:
        variable = str(metric.get("variable") or "").strip()
        worksheet = str(metric.get("worksheet") or "").strip()

        if not variable:
            continue

        terms = _metric_terms(variable)

        template_metrics.append(
            {
                "key": (worksheet, variable),
                "label": f"{worksheet}::{variable}",
                "terms": terms,
            }
        )

    return template_metrics


def _find_metric_matches(normalized_text, template_metrics):
    matched_keys = set()
    matched_labels = []

    for metric in template_metrics:
        if any(
            _contains_term(normalized_text, term)
            for term in metric["terms"]
        ):
            matched_keys.add(metric["key"])
            matched_labels.append(metric["label"])

    return matched_keys, matched_labels


def _page_relevance(text, matched_metric_count):
    normalized_text = normalize_text(text)

    years = set(
        re.findall(r"\b(?:19|20)\d{2}\b", text)
    )

    continuation_bonus = 1.5 if any(
        _contains_term(normalized_text, marker)
        for marker in CONTINUATION_MARKERS
    ) else 0.0

    score = (
        matched_metric_count * 10.0
        + min(numeric_density(text) * 30.0, 5.0)
        + table_structure_score(text) * 2.0
        + min(len(years) * 0.5, 2.0)
        + continuation_bonus
    )

    return round(score, 2)


def _baseline_selection(pdf_pages, settings):
    baseline_pages = []

    for page in pdf_pages[:settings.first_n_pages]:
        baseline_pages.append(page)

    for page in pdf_pages[settings.first_n_pages:]:
        if page_score(page.get("text", "")) > settings.page_score_threshold:
            baseline_pages.append(page)

    if len(pdf_pages) < settings.min_pages:
        baseline_pages = pdf_pages

    return baseline_pages


def select_pages(state: FinancialGraphState) -> dict:
    settings = get_settings()

    raw_pages = state.get("pdf_pages", [])
    excel_data = state.get("excel_data", [])
    errors = list(state.get("errors", []))

    pdf_pages = [
        _to_page_record(page, index)
        for index, page in enumerate(raw_pages)
    ]

    baseline_pages = _baseline_selection(
        pdf_pages,
        settings,
    )

    if not excel_data:
        errors.append(
            "Page selection requires template metrics in excel_data. "
            "Run read_creditlens_template before select_pages."
        )

        return {
            "pdf_pages": pdf_pages,
            "selected_pages": [],
            "baseline_selected_pages": baseline_pages,
            "errors": errors,
        }

    template_metrics = _build_template_metrics(excel_data)
    candidates = []

    for index, page in enumerate(pdf_pages):
        text = page.get("text", "")
        normalized_text = normalize_text(text)

        matched_keys, matched_labels = _find_metric_matches(
            normalized_text,
            template_metrics,
        )

        if not matched_keys:
            continue

        candidates.append(
            {
                "index": index,
                "page": page,
                "page_number": page["page_number"],
                "metric_keys": matched_keys,
                "matched_metrics": matched_labels,
                "score": _page_relevance(
                    text,
                    len(matched_keys),
                ),
            }
        )

    max_selected_pages = max(
        0,
        int(settings.max_selected_pages),
    )

    remaining = list(candidates)
    selected_candidates = []
    covered_metrics = set()

    while remaining and len(selected_candidates) < max_selected_pages:
        best = max(
            remaining,
            key=lambda candidate: (
                len(candidate["metric_keys"] - covered_metrics),
                candidate["score"],
                -candidate["page_number"],
            ),
        )

        selected_candidates.append(best)
        covered_metrics.update(best["metric_keys"])
        remaining.remove(best)

    selected_indices = {
        candidate["index"]
        for candidate in selected_candidates
    }

    selected_pages = [
        page
        for index, page in enumerate(pdf_pages)
        if index in selected_indices
    ]

    if not selected_pages:
        errors.append(
            "No PDF pages matched the template metric names or "
            "configured synonyms. Review the metric names and "
            "METRIC_SYNONYM_GROUPS."
        )

    print(
        "Improved selected pages:",
        [page["page_number"] for page in selected_pages],
    )
    print("Improved selected page count:", len(selected_pages))
    print(
        "Template metrics matched:",
        len(covered_metrics),
        "of",
        len({metric["key"] for metric in template_metrics}),
    )

    for candidate in sorted(
        selected_candidates,
        key=lambda item: item["page_number"],
    ):
        print(
            f"PDF page {candidate['page_number']}: "
            f"{candidate['matched_metrics']}"
        )

    return {
        "pdf_pages": pdf_pages,
        "selected_pages": selected_pages,
        "baseline_selected_pages": baseline_pages,
        "errors": errors,
    }
