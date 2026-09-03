"""Node: Answer Questions using LLM.

Iterates over each Excel row and extracts the corresponding financial
data point from the PDF context and added source hyperlink.
"""

from typing import List, Dict, Any, Optional
from langchain_core.messages import HumanMessage, SystemMessage

from graph.graph_state import FinancialGraphState
from prompts.system_prompt import SYSTEM_PROMPT
from prompts.user_prompt import get_user_prompt
from models import ExtractionResponse

from config import get_settings


def build_hyperlink(page_number: Optional[int], source_link: str) -> str:
    """Helper function applying the exact Excel HYPERLINK formula logic."""
    if page_number is not None and page_number != -1 and source_link:
        return f'=HYPERLINK("{source_link}#page={page_number}", "Page {page_number}")'
    return "N/A"


def answer_questions(state: FinancialGraphState) -> dict:
    """Extract metrics via LLM and enrich each answer with an Excel hyperlink."""
    llm = state.get("llm")
    structured_llm = llm.with_structured_output(ExtractionResponse)

    excel_data = state.get("excel_data", [])
    errors = state.get("errors", [])
    selected_pages = state.get("selected_pages", [])
    pdf_file_name = state.get("pdf_file_name", "")
  
    settings = get_settings()
    sharepoint_link = settings.sharepoint_link
    source_link = settings.sharepoint_link + pdf_file_name.replace(" ", "%20")


    USER_PROMPT = get_user_prompt(excel_data)
    
    full_context = "\n\n".join(
        [f"--- Page {i+1} ---\n{page.get('text', '')}" for i, page in enumerate(selected_pages)]
    )

    user_content = (
        f"Please extract the following variables:\n{USER_PROMPT}\n\n"
        f"Document context:\n{full_context}\n\n"
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT), 
        HumanMessage(content=user_content)
    ]
    
    try:
        response: ExtractionResponse = structured_llm.invoke(messages)
        
        if errors:
            response.errors.extend(errors)
            
        final_answers = []
        
        for answer in response.answers:
            answer.source_link = build_hyperlink(answer.page_number, source_link)
            final_answers.append(answer.model_dump())
            
        return {
            "answers": final_answers, 
            "errors": response.errors
        }
        
    except Exception as e:
        error_msg = f"Bulk LLM extraction error: {str(e)}"
        errors.append(error_msg)
        return {
            "answers": [],
            "errors": errors
        }

# from typing import List, Optional
# from pydantic import BaseModel, Field
# from langchain_core.messages import HumanMessage, SystemMessage

# from graph.graph_state import FinancialGraphState

# from prompts.system_prompt import SYSTEM_PROMPT
# from prompts.user_prompt import get_user_prompt
# from models import ExtractionResponse


# def answer_questions(state: FinancialGraphState) -> ExtractionResponse:
#     """Use the LLM to answer each question from the Excel template.

#     For each row:
#     - Constructs a prompt with the PDF context and the specific question
#     - Sends to LLM for extraction
#     - Collects the answer
#     """
#     llm = state.get("llm")
#     # Invoke LLM with Structured Output
#     structured_llm = llm.with_structured_output(ExtractionResponse)

#     excel_data = state.get("excel_data", [])
#     # pdf_pages = state.get("pdf_pages", [])
#     errors = state.get("errors", [])
#     selected_pages = state.get("selected_pages", [])

#     USER_PROMPT = get_user_prompt(excel_data)
    
#     # Prepare Document Context
#     full_context = "\n\n".join(
#         [f"--- Page {i+1} ---\n{page.get('text', '')}" for i, page in enumerate(selected_pages)]
#     )

#     user_content = (
#         f"Please extract the following variables:\n{USER_PROMPT}\n\n"
#         f"Document context:\n{full_context}"
#     )

#     messages = [
#         SystemMessage(content=SYSTEM_PROMPT), 
#         HumanMessage(content=user_content)
#         ]
    
#     try:
#         response: ExtractionResponse = structured_llm.invoke(messages)
        
#         # Merge any existing errors with new ones if they occurred
#         if errors:
#             response.errors.extend(errors)
            
#         return response
        
#     except Exception as e:
#         errors.append(f"Bulk LLM extraction error: {str(e)}")
#         return ExtractionResponse(errors=errors)



# SYSTEM_PROMPT = (
#     "You are an intelligent financial assistant helping credit teams analyze "
#     "and extract valuable insights from annual reports of companies. "
#     "Extract the requested financial data point from the provided document context. "
#     "If the information is not available in the document, respond with 'N/A'. "
#     "Be precise and provide only the requested value without additional explanation."
# )


# def answer_questions(state: FinancialGraphState) -> ExtractionResponse:
#     """Use the LLM to answer each question from the Excel template.

#     For each row:
#     - Constructs a prompt with the PDF context and the specific question
#     - Sends to LLM for extraction
#     - Collects the answer
#     """
#     llm = state.get("llm")
#     excel_data = state.get("excel_data", [])
#     pdf_pages = state.get("pdf_pages", [])
#     errors = state.get("errors", [])

    
#     if llm is None:
#         errors.append("LLM not available")
#         return ExtractionResponse(errors=errors)
#     if not pdf_pages:
#         errors.append("No PDF content available")
#         return ExtractionResponse(errors=errors)
#     if not excel_data:
#         errors.append("No questions from Excel")
#         return ExtractionResponse(errors=errors)

    
#     full_context = "\n\n".join(
#         [f"--- Page {i+1} ---\n{page.get('text', '')}" for i, page in enumerate(pdf_pages)]
#     )

#     system_msg = SystemMessage(content=SYSTEM_PROMPT)
#     answers = []

#     for item in excel_data:
#         variable = item["variable"]
#         description = item.get("description") or ""
#         worksheet = item["worksheet"]

#         question = f"From the following document, extract the value for: {variable}"
#         if description:
#             question += f"\nDescription: {description}"
#         question += f"\n\nDocument context:\n{full_context}"

#         try:
#             response = llm.invoke([system_msg, HumanMessage(content=question)])
#             answer_text = response.content.strip()
#         except Exception as e:
#             answer_text = f"ERROR: {str(e)}"
#             errors.append(f"LLM error for '{variable}': {str(e)}")

        
#         answers.append(
#             ExtractedAnswer(
#                 worksheet=worksheet,
#                 variable=variable,
#                 description=description,
#                 answer=answer_text,
#             )
#         )

    
#     return ExtractionResponse(answers=answers, errors=errors)