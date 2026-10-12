"""This node helps to select relevant pages from the annual report based on given set of keywords"""

# from prompts.selected_keywords import page_score
from prompts.selected_keywords import (
    page_relevance_score,
    page_score,
)
from config import get_settings
from graph.graph_state import FinancialGraphState

CONTINUATION_MARKERS = [
    "continued",
    "continuation",
    "carried forward",
    "brought forward",
]

# def select_pages(state: FinancialGraphState) -> dict:
#   """Select pages by matching keywords from the given set of keywords. The keywords are stored in the variable `selected_keywords`."""

#   settings = get_settings()

#   pdf_pages = state.get("pdf_pages", [])
#   n = settings.first_n_pages

#   selected_pages = []

#   #keep first n pages
#   for page in pdf_pages[:n]:
#     selected_pages.append(page)

#   for page in pdf_pages[n:]:
#     page_text = page["text"]
#     if page_score(page_text) > settings.page_score_threshold:
#       selected_pages.append(page)
  
#   # If the number of pages exceeds the minimum allowed, retain all pages without filtering
#   if len(pdf_pages) < settings.min_pages:
#     selected_pages = pdf_pages

#   return {"selected_pages": selected_pages, 
#           "errors": state.get("errors", []) 
#           }

def select_pages(state: FinancialGraphState) -> dict:
    settings = get_settings()
    pdf_pages = state.get("pdf_pages", [])

    # Assign physical PDF page numbers.
    # Python list indices start at 0, but PDF pages start at 1.
    for index, page in enumerate(pdf_pages):
        page["page_number"] = index + 1

    # Keep existing baseline selection unchanged.
    baseline_pages = []

    for page in pdf_pages[:settings.first_n_pages]:
        baseline_pages.append(page)

    for page in pdf_pages[settings.first_n_pages:]:
        if page_score(page.get("text", "")) > settings.page_score_threshold:
            baseline_pages.append(page)

    if len(pdf_pages) < settings.min_pages:
        baseline_pages = pdf_pages

    # Stage 1: broad keyword candidate filter.
    candidates = []

    for index, page in enumerate(pdf_pages):
        text = page.get("text", "")

        if page_score(text) >= settings.page_score_threshold:
            relevance = page_relevance_score(text)

            candidates.append(
                (
                    index,
                    page,
                    relevance,
                )
            )

    # Stage 2: rank candidates by financial relevance.
    candidates.sort(
        key=lambda item: item[2]["score"],
        reverse=True,
    )

    core_count = max(
        1,
        settings.max_selected_pages
        - settings.max_adjacent_pages,
    )

    selected_indices = {
        item[0]
        for item in candidates[:core_count]
    }

    candidate_map = {
        item[0]: item[2]
        for item in candidates
    }

    # Add adjacent / continuation pages.
    for index in sorted(selected_indices):
        for neighbor_index in (
            index - 1,
            index + 1,
        ):
            if len(selected_indices) >= settings.max_selected_pages:
                break

            if neighbor_index < 0 or neighbor_index >= len(pdf_pages):
                continue

            if neighbor_index in selected_indices:
                continue

            neighbor_text = pdf_pages[
                neighbor_index
            ].get("text", "")

            neighbor_relevance = page_relevance_score(
                neighbor_text
            )

            neighbor_lower = neighbor_text.lower()

            is_continuation = any(
                marker in neighbor_lower
                for marker in CONTINUATION_MARKERS
            )

            is_candidate = neighbor_index in candidate_map

            if is_candidate or (
                is_continuation
                and neighbor_relevance["score"] > 0
            ):
                selected_indices.add(
                    neighbor_index
                )

    selected_pages = [
        pdf_pages[index]
        for index in sorted(selected_indices)
    ]

    print(
        "Improved selected pages:",
        [
            page["page_number"]
            for page in selected_pages
        ],
    )

    print(
        "Improved selected page count:",
        len(selected_pages),
    )

    return {
        "pdf_pages": pdf_pages,
        "selected_pages": selected_pages,
        "baseline_selected_pages": baseline_pages,
        "errors": state.get("errors", []),
    }