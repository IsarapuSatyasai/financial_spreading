"""pydantic response model"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, TypedDict

class ExtractedAnswer(BaseModel):
    """For each metric extraction, LLM should follow this schema"""
    # worksheet: str
    # variable: str
    # description: str = ""
    # answer: str
    worksheet: str = Field(description="The worksheet name this variable belongs to")
    variable: str = Field(description="The name of the variable being extracted")
    answer: str = Field(description="The extracted value as given in the source document, or 'N/A' if not found")
    confidence: float = Field(
        description="Confidence score between 0.0 and 1.0 based on how clearly the document states the value."
    )
    page_number: int = Field(
        description="The page number where the information was found. Set to -1 if not found."
    )
    source_fields: List[str] = Field(
        default_factory=list, 
        description="List of fields in the source document that were used to extract the answer. One name for 1 to 1 mapping. List of several names if there is a calculation"
    )
    formula: str = Field(
        default=None, 
        description="Formula used to calculate the answer based on source fields. Set to null if not applicable for e.g. in case of 1 to 1 mapping."
    )
    

class ExtractionResponse(BaseModel):
    """Overall extracted response from the LLM model."""
    year: Optional[int] = Field(
        default=None, 
        description="The financial year this metric applies to (e.g., 2023, 2024). Set to null if not found."
    )
    currency: Optional[str] = Field(
        default=None, 
        description="The currency used for e.g. 'EUR', 'GBP', 'USD'. Set to null if not found."
    )
    scale: Optional[str] = Field(
        default=None, 
        description="The scale used for e.g. 'thousands' or 'millions'. Set to null if not found."
    )
    answers: List[ExtractedAnswer] = Field(
        default_factory=list, 
        description="List of extracted answers for all requested variables."
    )
    errors: List[str] = Field(default_factory=list)

# class ValidationResult(BaseModel):
#     method: str = Field(description="Name of the validation method.")
#     formula: Optional[str] = Field(None, description="Formula used for validation.")
#     expected_value: Optional[float] = Field(None, description="Expected value of the validation.")
#     actual_value: Optional[float] = Field(None, description="Actual value of the validation.")
#     passed: bool = Field(..., description="Whether the validation passed or failed.")
#     severity: str = Field("info", description="Severity level of the validation, such as 'info', 'warning', or 'error'.")
#     message: str = Field(..., description="Message describing the validation result to a real human in easy understandable language.")