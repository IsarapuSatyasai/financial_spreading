"""Node: that write final output to the excel file."""

import re
import pandas as pd
from graph.graph_state import FinancialGraphState
from template.excel_writer import excel_write
from langchain_core.runnables import RunnableLambda

def clean_llm_output(pydantic_response: list[dict]) -> list[dict]:
    """
    Clean LLM output before writing numbers.
    """

    normalized_output = []

    for row in pydantic_response:
        cleaned_row = row.copy()

        if str(cleaned_row.get("answer")).strip().upper() == "N/A":
            cleaned_row["answer"] = None

        if str(cleaned_row.get("source_link")).strip().upper() == "N/A":
            cleaned_row["source_link"] = None

        if str(cleaned_row.get("formula")).strip().lower() == "null":
            cleaned_row["formula"] = None

        if cleaned_row.get("source_fields") in ("[]", []):
            cleaned_row["source_fields"] = None

        if cleaned_row.get("formula") == "":
            cleaned_row["formula"] = None

        normalized_output.append(cleaned_row)

    return normalized_output
        
def build_excel_dateframes(answers: list[dict]) -> dict[str, pd.DataFrame]:
    """
    Build a dict of DataFrames keyed by worksheet.
    """
    worksheet_dict = {}
    for a in answers:
        row = {k: v for k, v in a.items() if k not in ("worksheet", "page_number")}
        worksheet_dict.setdefault(a["worksheet"], []).append(row)

    # Convert lists to DataFrames
    worksheet_dict = {ws: pd.DataFrame(rows) for ws, rows in worksheet_dict.items()}
    return worksheet_dict

#Create a chain for cleaning the output
excel_preparation_chain = (
    RunnableLambda(clean_llm_output, name="Clean extracted metrics from LLM")
    | RunnableLambda(build_excel_dateframes, name="Build excel dateframes")
)

#Create a function for creating LangGraph node that writes directly to the excel file
def create_excel_output(state: FinancialGraphState):
    """
    Create an excel file with the extracted metrics from LLM.
    """
    
    answers = state.get("answers")
    output_path = state.get("output_path")
    pdf_file_name = state.get("pdf_file_name")

    # Support both abfss:// and legacy /mnt/ output paths
    if output_path.startswith("/mnt/"):
        output_excel = "dbfs:" + output_path + pdf_file_name.removeprefix("InputData")
        output_excel = output_excel.removesuffix(".pdf") + ".xlsx"
    else:
        output_excel = output_path + pdf_file_name.removeprefix("InputData").removesuffix(".pdf") + ".xlsx"

    try:
        worksheet_dict = excel_preparation_chain.invoke(answers)
        status = excel_write(dataframes=worksheet_dict, output_path=output_excel)
        return {"output_excel": status, "errors": state.get("errors", [])}
    
    except Exception as e:
        error = f"Error writing excel file: {e}"
        return {"output_excel": "", "errors": state.get("errors", []) + [error]}

# def create_excel_output(state: FinancialGraphState):
#     """
#     Create an excel file with the extracted metrics from LLM.
#     """
    
#     answers = state.get("answers")
#     output_path = state.get("output_path")
#     pdf_file_name = state.get("pdf_file_name")

#     # Support both abfss:// and legacy /mnt/ output paths
#     if output_path.startswith("/mnt/"):
#         output_excel = "dbfs:" + output_path + pdf_file_name.removeprefix("InputData").removesuffix(".pdf") + ".xlsx"
#     else:
#         output_excel = output_path + pdf_file_name.removeprefix("InputData").removesuffix(".pdf") + ".xlsx"

#     # Convert answers list to dict of DataFrames keyed by worksheet
#     worksheet_dict = {}
#     for a in answers:
#         row = {k: v for k, v in a.items() if k != "worksheet"}
#         worksheet_dict.setdefault(a["worksheet"], []).append(row)

#     # Convert lists to DataFrames
#     worksheet_dict = {ws: pd.DataFrame(rows) for ws, rows in worksheet_dict.items()}

#     try:
#         status = excel_write(dataframes=worksheet_dict, output_path=output_excel)
#         return {"output_excel": status, "errors": state.get("errors", [])}
    
#     except Exception as e:
#         error = f"Error writing excel file: {e}"
#         return {"output_excel": "", "error": state.get("errors", []) + [error]}