"""This node helps to select relevant pages from the annual report based on given set of keywords"""

# from prompts.selected_keywords import page_score
from prompts.selected_keywords import (
    page_relevance_score,
    page_score,
)
from config import get_settings
from graph.graph_state import FinancialGraphState

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
    n = settings.first_n_pages

    # Baseline page selection
    baseline_pages = []

    for page in pdf_pages[:n]:
        baseline_pages.append(page)

    for page in pdf_pages[n:]:
        page_text = page["text"]

        if page_score(page_text) > settings.page_score_threshold:
            baseline_pages.append(page)

    if len(pdf_pages) < settings.min_pages:
        baseline_pages = pdf_pages

    # Improved selection
    improved_pages = sorted(
    pdf_pages,
    key=lambda page: page_score(page.get("text", "")),
    reverse=True,
    )[:settings.max_selected_pages]

    return {
        "selected_pages": improved_pages,
        "baseline_selected_pages": baseline_pages,
        "errors": state.get("errors", []),
    }