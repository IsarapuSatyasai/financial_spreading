from operator import itemgetter

from custom_lcel_components.chains import (
    get_sentence_window_rag_chain_from_config,
)
from custom_lcel_components.ingest import ingest_documents
from custom_lcel_components.llm import get_response_gpt
from custom_lcel_components.postprocessing import (
    string_to_docx,
)
from custom_lcel_components.postretrieval import (
    augment_prompt,
)
from custom_lcel_components.preprocessing import (
    clean_documents,
    combine_documents,
)
from custom_lcel_components.utils import (
    get_country_prompts_dict_per_country,
    reformat_for_final_report_with_rag,
    reformat_for_final_report_without_rag,
    translate_response,
    wrap_invoke_chain_with_multiple_questions_process_dict,
)
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from utils_financial_analysis import (
    clean_conversion_block,
    generate_final_response,
    remove_currency_block,
)


def get_financial_analysis_chain(
    ltu_financial_analysis_countries_prompts_dict,
    ltu_financial_analysis_countries_prompts_dict_additional,
    experiment=True,
):
    config = {
        "llm_model": "gpt-5",
        "temperature": 0,
        "top_p": 1,
        "embedding_model_name": "text-embedding-3-large",
        "pdf_loader_type_credit_lens": "PyPDFLoader", # pdf loader for credit lens
        "pdf_loader_type": "PyMuPDFLoader", # pdf loader for annual report
        "include_source": False,
        "hybrid_search_args": None,
        "remove_duplicate_chunks": True,
        "sentence_chunker_window_size": 5,
        "similarity_top_k": 20,
        "rerank_args": {"top_n": 10, "model": "cross-encoder/ms-marco-MiniLM-L-2-v2"},
        "system_message": "You are an intelligent financial assistant helping credit teams analyze and extract valuable insights from annual reports of companies. If no information is available about asked question, skip that section entirely. Do not include any inferences or placeholders. Always write in a clear and simple way. Use short sentences. Avoid complex words. When mentioning money, use the full currency code (e.g., EUR, USD, GBP) instead of symbols (€, $, £). Convert large numbers into a more readable format using terms like k (thousand), mln (million), or bln (billion). All monetary values should follow the format: CURRENCY_CODE XX unit, e.g., EUR 25 mln.",
    }

    # COMMAND ----------

    # """Pipeline functions"""
    # # in the future when env vars can be passed to the deployment;
    # # we do not need the custom function and we can pass the llm directly in LCEL

    """LCEL pipeline"""

    # define LCEL runnables
    # Assigns a chain of operations to ingest documents
    ingest_chain = RunnablePassthrough.assign(
        context=RunnableLambda(ingest_documents).bind(
            pdf_loader_type=config["pdf_loader_type_credit_lens"]
        )
        | RunnableLambda(clean_conversion_block)
        | RunnableLambda(remove_currency_block)
        | RunnableLambda(combine_documents)
        | RunnableLambda(lambda output: output[0]["text"])
    )

    translation_step = RunnableLambda(translate_response)

    # Defines a step to augment the prompt
    prompt_step = RunnableLambda(augment_prompt)

    # Defines a step to get a response from GPT, binding various configurations
    llm_step = RunnableLambda(get_response_gpt).bind(
        model_name=config["llm_model"],
        top_p=config["top_p"],
        temperature=config["temperature"],
        system_prompt=config["system_message"],
    )

    # Chains the prompt augmentation step with the GPT response step
    generate_answer_chain = {
        "generated_report_language": RunnableLambda(
            lambda x: x["generated_report_language"]
        ),
        "llm_output": prompt_step | llm_step,
    } | translation_step

    # Assigns a chain to get country-specific prompts
    get_country_prompts_dict = RunnablePassthrough.assign(
        country_prompts_dict=RunnableLambda(get_country_prompts_dict_per_country).bind(
            countries_prompts_dict=ltu_financial_analysis_countries_prompts_dict
        )
    )

    # Wraps the chain without RAG with a function to process multiple questions
    sequential_question_func = wrap_invoke_chain_with_multiple_questions_process_dict(
        chain=generate_answer_chain
    )

    # Assigns a step to invoke the chain with multiple questions
    invoke_chain_with_multiple_questions_step = RunnablePassthrough.assign(
        responses=RunnableLambda(sequential_question_func)
    )

    reformat_output_step_without_rag = RunnableLambda(
        reformat_for_final_report_without_rag
    )

    # Assigns the final credit lens chain, invoking the core chain and extracting responses
    credit_lens_chain = RunnablePassthrough.assign(
        credit_lens_chain_responses=(
            {
                "source": itemgetter("credit_lens_source"),
                "country_name": itemgetter("country_name"),
                "generated_report_language": itemgetter("generated_report_language"),
            }
            | ingest_chain
            | get_country_prompts_dict
            | invoke_chain_with_multiple_questions_step
            | reformat_output_step_without_rag
        )
    )

    # The following defines a RAG chain that can enhance financial analysis with an additional report. This report could be an annual report, a local agency report, or any report up to hundreds of pages.
    # Initialize the RAG chain with the given configuration
    (
        rag_chain,
        index_chain,
        chain_without_index,
    ) = get_sentence_window_rag_chain_from_config(config)

    # Create a passthrough step to assign the country prompts dictionary
    additional_report_get_country_prompts_dict = RunnablePassthrough.assign(
        additional_report_country_prompts_dict=RunnableLambda(
            get_country_prompts_dict_per_country
        ).bind(
            countries_prompts_dict=ltu_financial_analysis_countries_prompts_dict_additional
        )
    )

    # Wrap the RAG chain with a function to process multiple questions
    additional_report_sequential_question_func = (
        wrap_invoke_chain_with_multiple_questions_process_dict(
            chain=(
                {
                    "generated_report_language": RunnableLambda(
                        lambda x: x["generated_report_language"]
                    ),
                    "llm_output": chain_without_index,
                }
                | translation_step
            )
        )
    )

    # Create a passthrough step to invoke the chain with multiple questions
    additional_report_invoke_chain_with_multiple_questions_step = (
        RunnablePassthrough.assign(
            responses=index_chain
            | RunnableLambda(additional_report_sequential_question_func).bind(
                questions_dict_key="additional_report_country_prompts_dict"
            ),
        )
    )

    reformat_output_step_with_rag = RunnableLambda(reformat_for_final_report_with_rag)

    # Define the core chain for the additional report
    additional_report_core_chain = (
        {
            "source": itemgetter("additional_report_source"),
            "country_name": itemgetter("country_name"),
            "generated_report_language": itemgetter("generated_report_language"),
        }
        | additional_report_get_country_prompts_dict
        | additional_report_invoke_chain_with_multiple_questions_step
        | reformat_output_step_with_rag
    )

    # The code defines a RunnableBranch named additional_report_chain that processes an input dictionary x based on the presence or absence of the key "additional_report_source".
    # Only when additional_report_source is not None, the additional_report_core_chain is invoked.

    def additional_report_chain(x):
        if x.get("additional_report_source") == "":
            return {**x, "additional_report_chain_responses": None}
        else:
            response = additional_report_core_chain.invoke(x)
            return {**x, "additional_report_chain_responses": response}

    additional_report_chain_step = RunnableLambda(additional_report_chain)

    # Step to assign the final response generation function
    get_final_response_step = RunnablePassthrough.assign(
        responses=RunnableLambda(generate_final_response)
    )

    # Conditional step to format the output based on the experiment flag
    if experiment:
        format_output = RunnablePassthrough.assign(
            final_response_doc=RunnableLambda(string_to_docx).bind(
                generated_report_name="Financial Performance Report",
                table_font_size=7,
                table_header_font_size=6,
            )
        )
    else:
        format_output = RunnableLambda(string_to_docx).bind(
            generated_report_name="Financial Performance Report",
            table_font_size=7,
            table_header_font_size=6,
        )

    # Define the financial analysis chain
    financial_analysis_chain = (
        credit_lens_chain
        | additional_report_chain_step
        | get_final_response_step
        | format_output
    )
    financial_analysis_chain.name = "chain_GAILTU-FinancialAnalysis"

    return financial_analysis_chain
