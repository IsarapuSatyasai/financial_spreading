"""
This imports and excel file and converts them into spark dataframes
"""

import pandas as pd
from databricks.sdk.runtime import dbutils
import openpyxl
import re

def _sanitize_name(name: str, default: str = "Sheet") -> str:
    """
    Sanitizes a worksheet name to make it compatible to unity catalog table name.
    """
    sanitized = re.sub(r"[^a-zA-Z0-9]", "_", str(name)).strip("_")
    if not sanitized:
        sanitized = default
    if sanitized[0].isdigit():
        sanitized = "sheet_" + sanitized
    return sanitized


def _sanitize_columns(pd_df: pd.DataFrame) -> pd.DataFrame:
    """
    Sanitizes the column names of a DataFrame to make them compatible with Unity Catalog column names.
    """
    
    seen: dict[str, int] = {}
    new_columns: list[str] = []

    for col in pd_df.columns:
        key = _sanitize_name(col, default="column")
        
        if key in seen:
            seen[key] += 1
            key = f"{key}_{seen[key]}"
        else:
            seen[key] = 1

        new_columns.append(key)
    return pd_df.rename(columns=dict(zip(pd_df.columns, new_columns)))


def read_xlsx(file_path: str) -> dict[str, pd.DataFrame]:
    """
    This function reads an Excel file and returns a dictionary of DataFrames, where each DataFrame corresponds to a worksheet in the Excel file.

    Parameters:
    file_path (str): The path to the Excel file. This should be a string that starts with "/dbfs/mnt" and ends with ".xlsx". For example: "/dbfs/mnt/projects/FinancialSpreading/Test/test_file.xlsx".

    Returns:
    A dictionary where the keys are the sanitized worksheet names and the values are the DataFrames.
    """
    

    #convert absolute file path to standard dbfs path
    dbfs_path = file_path.replace("/dbfs", "dbfs:")

    #validate pathi think here you can crete a 
    try:
        dbutils.fs.ls(dbfs_path)
    except:
        raise Exception(f"File not found: {dbfs_path}")

    # Read the Excel file using pandas
    pd_worksheets = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")

    pandas_dfs = {}
    for worksheet_name, pd_df in pd_worksheets.items():
        # Sanitize the worksheet name
        sanitized_worksheet_name = _sanitize_name(worksheet_name)      
        pd_df = _sanitize_columns(pd_df)
        pandas_dfs[sanitized_worksheet_name] = pd_df

    return pandas_dfs
    