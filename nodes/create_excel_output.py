"""Node: that write final output to the excel file."""

import pandas as pd
from graph.graph_state import FinancialGraphState
from template.excel_writer import excel_write


def create_excel_output(state: FinancialGraphState):
    """
    Create an excel file with the extracted metrics from LLM.
    """
    
    answers = state.get("answers")
    output_path = state.get("output_path")
    pdf_file_name = state.get("pdf_file_name")

    output_excel = "dbfs:" + output_path + pdf_file_name.removeprefix("InputData").removesuffix(".pdf") + ".xlsx"

    # Convert answers list to dict of DataFrames keyed by worksheet
    worksheet_dict = {}
    for a in answers:
        row = {k: v for k, v in a.items() if k != "worksheet"}
        worksheet_dict.setdefault(a["worksheet"], []).append(row)

    # Convert lists to DataFrames
    worksheet_dict = {ws: pd.DataFrame(rows) for ws, rows in worksheet_dict.items()}

    try:
        status = excel_write(dataframes=worksheet_dict, output_path=output_excel)
        return {"output_excel": status, "errors": state.get("errors", [])}
    
    except Exception as e:
        error = f"Error writing excel file: {e}"
        return {"output_excel": "", "error": state.get("errors", []) + [error]}