"""
Node: Search for relevant keywords within selected PDF pages.

The node searches the selected PDF page text for keywords derived
from the Excel metric and extracts surrounding text as context.
"""

import re
from typing import Dict, Any, List

from graph.graph_state import FinancialGraphState


# Words that usually don't provide useful search signals
STOP_WORDS = {
    "the",
    "and",
    "for",
    "from",
    "with",
    "this",
    "that",
    "during",
    "year",
    "years",
    "company",
    "companies",
    "total",
    "value",
    "amount",
    "financial",
    "information",
}


def clean_keywords(words: List[str]) -> List[str]:
    """
    Remove unnecessary words and duplicate keywords.
    """

    cleaned = []

    for word in words:
        word = word.strip().lower()

        if not word:
            continue

        if word in STOP_WORDS:
            continue

        if len(word) < 3:
            continue

        if word not in cleaned:
            cleaned.append(word)

    return cleaned


def build_keywords(metric: Dict[str, Any]) -> List[str]:
    """
    Build search keywords from the Excel metric.

    Priority:
        1. Variable
        2. Description
        3. Remarks
    """

    keywords = []

    variable = metric.get("variable", "")
    description = metric.get("description", "")
    remarks = metric.get("remarks", "")

    # Keep the complete variable phrase
    if variable:
        keywords.append(variable.strip())

    # Add individual meaningful words from variable
    if variable:
        keywords.extend(variable.split())

    # Add meaningful words from description
    if description:
        keywords.extend(description.split())

    # Add meaningful words from remarks
    if remarks:
        keywords.extend(remarks.split())

    return clean_keywords(keywords)


def extract_context(
    text: str,
    start: int,
    end: int,
    before: int = 500,
    after: int = 1000,
) -> str:
    """
    Extract surrounding text around a keyword match.
    """

    context_start = max(0, start - before)
    context_end = min(len(text), end + after)

    context = text[context_start:context_end]

    return context.strip()


def find_keyword_matches(
    text: str,
    keyword: str,
    max_matches: int = 5,
) -> List[Dict[str, Any]]:
    """
    Find keyword occurrences in text.

    Matching is case-insensitive.
    """

    matches = []

    if not text or not keyword:
        return matches

    # Escape keyword so special characters don't break regex
    escaped_keyword = re.escape(keyword)

    # Word-boundary matching
    pattern = rf"\b{escaped_keyword}\b"

    for match in re.finditer(
        pattern,
        text,
        flags=re.IGNORECASE,
    ):
        context = extract_context(
            text,
            match.start(),
            match.end(),
        )

        matches.append(
            {
                "keyword": keyword,
                "start": match.start(),
                "end": match.end(),
                "context": context,
            }
        )

        if len(matches) >= max_matches:
            break

    return matches


def keyword_search(state: FinancialGraphState) -> dict:
    """
    Search for Excel metric keywords inside selected PDF pages.

    Returns:
        keyword_contexts
    """

    excel_data = state.get("excel_data", [])
    selected_pages = state.get("selected_pages", [])

    keyword_contexts = []

    for metric in excel_data:

        variable = metric.get("variable", "")
        keywords = build_keywords(metric)

        metric_matches = []

        for index, page in enumerate(selected_pages):

            page_text = page.get("text", "")

            # Prefer the original PDF page number if available
            page_number = page.get(
                "page_number",
                page.get("page", index + 1),
            )

            for keyword in keywords:

                matches = find_keyword_matches(
                    page_text,
                    keyword,
                    max_matches=5,
                )

                for match in matches:

                    metric_matches.append(
                        {
                            "page_number": page_number,
                            "keyword": match["keyword"],
                            "context": match["context"],
                        }
                    )

        keyword_contexts.append(
            {
                "variable": variable,
                "keywords": keywords,
                "matches": metric_matches,
            }
        )

    return {"keyword_contexts": keyword_contexts}