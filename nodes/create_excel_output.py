# """Node: that write final output to the excel file."""

# import pandas as pd
# from graph.graph_state import FinancialGraphState
# from template.excel_writer import excel_write


# def create_excel_output(state: FinancialGraphState):
#     """
#     Create an excel file with the extracted metrics from LLM.
#     """
    
#     answers = state.get("answers")
#     output_path = state.get("output_path")
#     pdf_file_name = state.get("pdf_file_name")

#     output_excel = "dbfs:" + output_path + pdf_file_name.removeprefix("InputData").removesuffix(".pdf") + ".xlsx"

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

"""Node: Write final financial spreading output to local Excel file."""

from pathlib import Path

from graph.graph_state import FinancialGraphState
from template.excel_writer import excel_write


def create_excel_output(state: FinancialGraphState) -> dict:
    """
    Create the final Excel output locally.
    """

    answers = state.get("answers", [])

    if not answers:
        return {
            "output_excel": "",
            "errors": state.get(
                "errors",
                []
            ) + ["No answers available for Excel output."]
        }

    try:
        # --------------------------------------------------
        # Output directory
        # --------------------------------------------------

        output_dir = Path(
            state.get(
                "output_dir",
                "output"
            )
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # --------------------------------------------------
        # Output filename
        # --------------------------------------------------

        pdf_file_name = state.get(
            "pdf_file_name",
            "financial_spreading"
        )

        pdf_stem = Path(
            pdf_file_name
        ).stem

        output_path = (
            output_dir
            / f"{pdf_stem}_output.xlsx"
        )

        # --------------------------------------------------
        # Convert answers into worksheet DataFrames
        # --------------------------------------------------

        dataframes = {}

        for answer in answers:

            worksheet = answer.get(
                "worksheet",
                "Output"
            )

            row = {
                key: value
                for key, value in answer.items()
                if key != "worksheet"
            }

            dataframes.setdefault(
                worksheet,
                []
            ).append(row)

        dataframes = {
            sheet_name: __import__(
                "pandas"
            ).DataFrame(rows)
            for sheet_name, rows
            in dataframes.items()
        }

        # --------------------------------------------------
        # Write Excel
        # --------------------------------------------------

        excel_write(
            dataframes=dataframes,
            output_path=str(output_path),
            overwrite=True,
        )

        return {
            "output_excel": str(
                output_path.resolve()
            ),
            "errors": state.get(
                "errors",
                []
            ),
        }

    except Exception as e:

        return {
            "output_excel": "",
            "errors": state.get(
                "errors",
                []
            ) + [
                f"Excel output error: {str(e)}"
            ],
        }