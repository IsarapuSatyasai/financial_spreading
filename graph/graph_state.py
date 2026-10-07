"""Graph state for financial spreading"""

from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict
from langchain_openai import AzureChatOpenAI

class Metric(TypedDict):
    """
    Metric object.
    """
    #worksheet name    
    worksheet: str

    #Metric name
    variable: str

    #Metric description
    description: str

    #Metric formula
    formula: str | None

    #Stakeholders remarks
    remarks: str | None
    

class FinancialGraphState(TypedDict, total=False):
    """
    LangGraph state object.
    Accepts State schema that specifies the shape of the state that the nodes in the graph can access and update.
    """

    #**************Input*****************

    #Path to the Excel template file
    excel_path: str

    #Path to the annual report PDF document stored in blob storage.
    pdf_source: str

    #Output path for the generated Excel file, provided in the config
    output_path: str

    #Name of the source PDF file
    pdf_file_name: str

    # #************Intermediate*************

    # #Parsed Excel rows (variables/definitions)
    excel_data: List[Metric]

    #Parsed PDF document pages
    pdf_pages: List[Dict[str, Any]]

    #Language of the Annual report
    source_language: str

    #LLM model instance
    llm: Optional[AzureChatOpenAI]

    #Selected pages for extraction
    selected_pages: List[Dict[str, Any]]
    
    # #Extracted tables from the PDF document
    # tables: List[Dict[str, Any]]

    # #Metric requested for each Excel row
    # metric_requests: List[Dict[str, Any]]

    #Extracted metrics for each Excel row
    answers: List[Dict[str, Any]]
    
    # Number of attempts allowed for confidence refinement
    refinement_attempts: int


    # #*************Output******************

    # #Validation results for each Excel row
    # validations: List[Dict[str, Any]]

    # #Final answer for each Excel row
    # final_answer: List[Dict[str, Any]]

    #Any errors encountered during execution
    errors: List[str]

    #Final check that all metrics have been extracted
    extraction_completed: bool