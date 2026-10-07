"""Create template-aligned Excel output."""

import pandas as pd

from graph.graph_state import FinancialGraphState
from template.excel_writer import excel_write


def align_answers_to_template(
    excel_data,
    answers,
):
    """Ensure final output contains exactly template metrics."""

    answer_map = {
        (
            answer["worksheet"],
            answer["variable"],
        ): answer
        for answer in answers
    }

    aligned = []

    for metric in excel_data:
        key = (
            metric["worksheet"],
            metric["variable"],
        )

        answer = answer_map.get(key, {})

        aligned.append(
            {
                "worksheet": metric["worksheet"],
                "variable": metric["variable"],
                "answer": answer.get(
                    "answer",
                    "N/A",
                ),
                "confidence": answer.get(
                    "confidence",
                    0.0,
                ),
                "page_number": answer.get(
                    "page_number",
                    -1,
                ),
                "source_fields": answer.get(
                    "source_fields",
                    [],
                ),
                "formula": answer.get(
                    "formula",
                ),
                "source_link": answer.get(
                    "source_link",
                    "N/A",
                ),
            }
        )

    return aligned


def build_comparison_dataframes(
    excel_data,
    original_answers,
    final_answers,
    baseline_pages,
    improved_pages,
):
    """Create comparison worksheets."""

    original_map = {
        (
            answer["worksheet"],
            answer["variable"],
        ): answer
        for answer in original_answers
    }

    final_map = {
        (
            answer["worksheet"],
            answer["variable"],
        ): answer
        for answer in final_answers
    }

    baseline_numbers = {
        page.get("page_number")
        for page in baseline_pages
    }

    improved_numbers = {
        page.get("page_number")
        for page in improved_pages
    }

    comparison_data = {}

    for metric in excel_data:
        worksheet = metric["worksheet"]

        key = (
            worksheet,
            metric["variable"],
        )

        original = original_map.get(key, {})
        final = final_map.get(key, {})

        original_answer = original.get(
            "answer",
            "N/A",
        )

        refined_answer = final.get(
            "answer",
            original_answer,
        )

        confidence = original.get(
            "confidence",
            0.0,
        )

        original_page = original.get(
            "page_number",
            -1,
        )

        refined_page = final.get(
            "page_number",
            original_page,
        )

        original_source_fields = original.get(
            "source_fields",
            [],
        )

        refined_source_fields = final.get(
            "source_fields",
            original_source_fields,
        )

        original_formula = original.get(
            "formula",
        )

        refined_formula = final.get(
            "formula",
            original_formula,
        )

        original_source_link = original.get(
            "source_link",
            "N/A",
        )

        refined_source_link = final.get(
            "source_link",
            original_source_link,
        )

        baseline_page = original_page
        improved_page = refined_page

        baseline_selected = (
            baseline_page in baseline_numbers
        )

        improved_selected = (
            improved_page in improved_numbers
        )

        page_changed = (
            baseline_page != improved_page
        )

        changed = (
            original_answer != refined_answer
            or page_changed
            or (
                original_source_fields
                != refined_source_fields
            )
            or (
                original_formula
                != refined_formula
            )
            or (
                original_source_link
                != refined_source_link
            )
        )

        row = {
            "variable": metric["variable"],
            "answer_original": original_answer,
            "answer_refined": refined_answer,
            "confidence": confidence,
            "baseline_page": baseline_page,
            "improved_page": improved_page,
            "page_changed": page_changed,
            "baseline_selected": baseline_selected,
            "improved_selected": improved_selected,
            "source_fields_original": (
                original_source_fields
            ),
            "source_fields_refined": (
                refined_source_fields
            ),
            "formula_original": original_formula,
            "formula_refined": refined_formula,
            "source_link_original": (
                original_source_link
            ),
            "source_link_refined": (
                refined_source_link
            ),
        }

        comparison_data.setdefault(
            worksheet,
            [],
        ).append(row)

    return {
        worksheet: pd.DataFrame(rows)
        for worksheet, rows in comparison_data.items()
    }

# def build_page_selection_comparison(
#     pdf_pages,
#     baseline_pages,
#     improved_pages,
# ):
#     """Compare baseline and improved page selection."""

#     baseline_numbers = {
#         page.get("page_number")
#         for page in baseline_pages
#     }

#     improved_numbers = {
#         page.get("page_number")
#         for page in improved_pages
#     }

#     rows = []

#     for index, page in enumerate(pdf_pages, start=1):
#         page_number = page.get("page_number", index)

#         baseline_selected = page_number in baseline_numbers
#         improved_selected = page_number in improved_numbers

#         rows.append(
#             {
#                 "page_number": page_number,
#                 "baseline_selected": baseline_selected,
#                 "improved_selected": improved_selected,
#                 "changed": (
#                     baseline_selected != improved_selected
#                 ),
#             }
#         )

#     return pd.DataFrame(rows)

def create_excel_output(
    state: FinancialGraphState,
):
    """Create Excel output using template-defined metrics."""

    excel_data = state.get(
        "excel_data",
        [],
    )

    original_answers = state.get(
        "original_answers",
        [],
    )

    answers = state.get(
        "answers",
        [],
    )

    output_path = state.get(
        "output_path",
        "",
    )

    pdf_file_name = state.get(
        "pdf_file_name",
        "",
    )

    if not excel_data:
        return {
            "output_excel": "",
            "comparison_excel": "",
            "errors": state.get(
                "errors",
                [],
            ) + [
                "No template metrics available for Excel output."
            ],
        }

    if not answers:
        answers = []

    output_name = (
        pdf_file_name.removeprefix(
            "InputData"
        ).removesuffix(
            ".pdf"
        )
        + ".xlsx"
    )

    output_excel = (
        output_path.rstrip("/")
        + "/"
        + output_name
    )

    comparison_name = (
        pdf_file_name.removeprefix(
            "InputData"
        ).removesuffix(
            ".pdf"
        )
        + "-comparison.xlsx"
    )

    comparison_excel = (
        output_path.rstrip("/")
        + "/"
        + comparison_name
    )

    aligned_answers = align_answers_to_template(
        excel_data,
        answers,
    )

    worksheet_dict = {}

    for answer in aligned_answers:
        worksheet = answer["worksheet"]

        row = {
            key: value
            for key, value in answer.items()
            if key != "worksheet"
        }

        worksheet_dict.setdefault(
            worksheet,
            [],
        ).append(row)

    worksheet_dict = {
        worksheet: pd.DataFrame(rows)
        for worksheet, rows in worksheet_dict.items()
    }

    comparison_dict = build_comparison_dataframes(
        excel_data,
        original_answers,
        answers,
        state.get("baseline_selected_pages", []),
        state.get("selected_pages", []),
    )
    # page_selection_comparison = build_page_selection_comparison(
    #     state.get("pdf_pages", []),
    #     state.get("baseline_selected_pages", []),
    #     state.get("selected_pages", []),
    # )

    # comparison_dict["Page Selection"] = page_selection_comparison

    try:
        print(
            f"Creating Excel output: {output_excel}"
        )

        print(
            f"Creating comparison output: {comparison_excel}"
        )

        print(
            f"Template metrics: {len(excel_data)}"
        )

        print(
            f"Final answers: {len(aligned_answers)}"
        )

        print(
            f"Worksheets: {list(worksheet_dict.keys())}"
        )

        print(
            f"Comparison worksheets: "
            f"{list(comparison_dict.keys())}"
        )

        status = excel_write(
            dataframes=worksheet_dict,
            output_path=output_excel,
        )

        comparison_status = excel_write(
            dataframes=comparison_dict,
            output_path=comparison_excel,
        )

        return {
            "output_excel": status,
            "comparison_excel": comparison_status,
            "errors": state.get(
                "errors",
                [],
            ),
        }

    except Exception as exc:
        error = f"Error writing excel file: {exc}"

        print(error)

        return {
            "output_excel": "",
            "comparison_excel": "",
            "errors": state.get(
                "errors",
                [],
            ) + [error],
        }


# """Node: that write final output to the excel file."""

# import re
# import pandas as pd
# from graph.graph_state import FinancialGraphState
# from template.excel_writer import excel_write
# from langchain_core.runnables import RunnableLambda

# def clean_llm_output(pydantic_response: list[dict]) -> list[dict]:
#     """
#     Clean LLM output before writing numbers.
#     """

#     normalized_output = []

#     for row in pydantic_response:
#         cleaned_row = row.copy()

#         if str(cleaned_row.get("answer")).strip().upper() == "N/A":
#             cleaned_row["answer"] = None

#         if str(cleaned_row.get("source_link")).strip().upper() == "N/A":
#             cleaned_row["source_link"] = None

#         if str(cleaned_row.get("formula")).strip().lower() == "null":
#             cleaned_row["formula"] = None

#         if cleaned_row.get("source_fields") in ("[]", []):
#             cleaned_row["source_fields"] = None

#         if cleaned_row.get("formula") == "":
#             cleaned_row["formula"] = None

#         normalized_output.append(cleaned_row)

#     return normalized_output
        
# def build_excel_dateframes(answers: list[dict]) -> dict[str, pd.DataFrame]:
#     """
#     Build a dict of DataFrames keyed by worksheet.
#     """
#     worksheet_dict = {}
#     for a in answers:
#         row = {k: v for k, v in a.items() if k not in ("worksheet", "page_number")}
#         worksheet_dict.setdefault(a["worksheet"], []).append(row)

#     # Convert lists to DataFrames
#     worksheet_dict = {ws: pd.DataFrame(rows) for ws, rows in worksheet_dict.items()}
#     return worksheet_dict

# #Create a chain for cleaning the output
# excel_preparation_chain = (
#     RunnableLambda(clean_llm_output, name="Clean extracted metrics from LLM")
#     | RunnableLambda(build_excel_dateframes, name="Build excel dateframes")
# )

# #Create a function for creating LangGraph node that writes directly to the excel file
# def create_excel_output(state: FinancialGraphState):
#     """
#     Create an excel file with the extracted metrics from LLM.
#     """
    
#     answers = state.get("answers")
#     output_path = state.get("output_path")
#     pdf_file_name = state.get("pdf_file_name")

#     # Support both abfss:// and legacy /mnt/ output paths
#     if output_path.startswith("/mnt/"):
#         output_excel = "dbfs:" + output_path + pdf_file_name.removeprefix("InputData")
#         output_excel = output_excel.removesuffix(".pdf") + ".xlsx"
#     else:
#         output_excel = output_path + pdf_file_name.removeprefix("InputData").removesuffix(".pdf") + ".xlsx"

#     try:
#         worksheet_dict = excel_preparation_chain.invoke(answers)
#         status = excel_write(dataframes=worksheet_dict, output_path=output_excel)
#         return {"output_excel": status, "errors": state.get("errors", [])}
    
#     except Exception as e:
#         error = f"Error writing excel file: {e}"
#         return {"output_excel": "", "errors": state.get("errors", []) + [error]}

# # def create_excel_output(state: FinancialGraphState):
# #     """
# #     Create an excel file with the extracted metrics from LLM.
# #     """
    
# #     answers = state.get("answers")
# #     output_path = state.get("output_path")
# #     pdf_file_name = state.get("pdf_file_name")

# #     # Support both abfss:// and legacy /mnt/ output paths
# #     if output_path.startswith("/mnt/"):
# #         output_excel = "dbfs:" + output_path + pdf_file_name.removeprefix("InputData").removesuffix(".pdf") + ".xlsx"
# #     else:
# #         output_excel = output_path + pdf_file_name.removeprefix("InputData").removesuffix(".pdf") + ".xlsx"

# #     # Convert answers list to dict of DataFrames keyed by worksheet
# #     worksheet_dict = {}
# #     for a in answers:
# #         row = {k: v for k, v in a.items() if k != "worksheet"}
# #         worksheet_dict.setdefault(a["worksheet"], []).append(row)

# #     # Convert lists to DataFrames
# #     worksheet_dict = {ws: pd.DataFrame(rows) for ws, rows in worksheet_dict.items()}

# #     try:
# #         status = excel_write(dataframes=worksheet_dict, output_path=output_excel)
# #         return {"output_excel": status, "errors": state.get("errors", [])}
    
# #     except Exception as e:
# #         error = f"Error writing excel file: {e}"
# #         return {"output_excel": "", "error": state.get("errors", []) + [error]}