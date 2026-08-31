"""
Configration of paths and setup of environment variables for financial spreading project.
Import this to main notebook to setup the openai and storage account.
"""

import os
from databricks.sdk.runtime import dbutils

class Settings:
    os.environ["AZURE_OPENAI_API_KEY"] = dbutils.secrets.get(
        scope="azure-key-vault-scope", key="openai-apim-api-key"
        )
    os.environ["AZURE_OPENAI_ENDPOINT"] = "https://msc-apim-gailtu-prd.azure-api.net/openai-api"
    os.environ["STORAGE_ACCOUNT"] = "mscstagailtuprd03"
    os.environ["SA_ACCESSKEY"] = dbutils.secrets.get(
        scope="azure-key-vault-scope", key="sta-eu-accesskey"
    )
    os.environ["ENVIRONMENT"] = "prd"

    # --- Azure OpenAI ---
    openai_api_key: str = ""
    azure_openai_deployment: str = "gpt-5.6-luna"
    azure_openai_api_version: str = "2024-10-21"

    # --- LLM parameters ---
    llm_temperature: float = 0.0
    llm_top_p: float = 1.0
    llm_seed: int = 1234

    # --- Page selection ---
    first_n_pages = 5
    page_score_threshold = 1
    min_pages = 30

    # --- Sharepoint ---
    sharepoint_link = "https://connect2dll.sharepoint.com/:b:/r/sites/Grp-FinancialSpreading/Shared%20Documents/General/5.%20Input%20data"

    paths = [
        {
            'name': 'input_path',
            'type': 'Azure blob storage',
            'reference': '/mnt/projects/FinancialSpreading/InputData',
            'comment': 'Input location for storing annual reports for each country'
        },
        {
            'name': 'output_path',
            'type': 'Azure blob storage',
            'reference': '/mnt/projects/FinancialSpreading/OutputData',
            'comment': 'Output location for storing annual reports for each country'
        },   
    ]
                                                          
def get_settings() -> Settings:
    return Settings()

