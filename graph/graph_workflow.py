# """Graph builder — assembles and compiles the LangGraph StateGraph.

# Keeps graph topology in one place so it can be imported by the notebook
# (for interactive use) or by a production entry point.
# """

# from langgraph.graph import StateGraph, END

# from state.graph_state import GraphState
# from nodes.read_excel import read_excel_template
# from nodes.parse_pdf import parse_pdf_document
# from nodes.connect_llm import connect_llm
# from nodes.answer_questions import answer_questions


# def build_graph():
#     """Construct and compile the financial spreading graph.

#     Returns
#     -------
#     CompiledStateGraph
#         Ready to invoke with an initial GraphState.
#     """
#     workflow = StateGraph(GraphState)

#     # Register nodes
#     workflow.add_node("read_excel_template", read_excel_template)
#     workflow.add_node("parse_pdf_document", parse_pdf_document)
#     workflow.add_node("connect_llm", connect_llm)
#     workflow.add_node("answer_questions", answer_questions)

#     # Define sequential edges
#     workflow.set_entry_point("read_excel_template")
#     workflow.add_edge("read_excel_template", "parse_pdf_document")
#     workflow.add_edge("parse_pdf_document", "connect_llm")
#     workflow.add_edge("connect_llm", "answer_questions")
#     workflow.add_edge("answer_questions", END)

#     return workflow.compile()


from langgraph.graph import StateGraph, START, END
from graph.graph_state import FinancialGraphState

# from template.excel_reader import read_xlsx
from nodes.read_creditlens_template import read_creditlens_template
from nodes.annual_report_parser import annual_report_parser
from nodes.source_language import source_language
from nodes.select_pages import select_pages
from nodes.keyword_search import keyword_search
from nodes.connect_llm import connect_llm
from nodes.answer_questions import answer_questions
from nodes.create_excel_output import create_excel_output

def complete(state: FinancialGraphState) -> dict:
    return {"extraction_completed": True}

def build_graph():
    """Construct and compile the financial spreading graph.

    Returns
    -------
    CompiledStateGraph
        Ready to invoke with an initial GraphState.
    """
        
    # Build the LangGraph
    workflow = StateGraph(FinancialGraphState)

    workflow.add_node("read_creditlens_template", read_creditlens_template)
    workflow.add_node("annual_report_parser", annual_report_parser)
    workflow.add_node("source_language", source_language)
    workflow.add_node("select_pages", select_pages)
    workflow.add_node("keyword_search", keyword_search)
    workflow.add_node("connect_llm", connect_llm)
    workflow.add_node("answer_questions", answer_questions)
    workflow.add_node("create_excel_output", create_excel_output)
    workflow.add_node("complete", complete)
    # workflow.add_node("ingest_documents", ingest_documents)
    # workflow.add_node("load_document", load_document)
    # workflow.add_node("parse_document", parse_document)
    # workflow.add_node("extract_metrics", extract_metrics)
    # workflow.add_node("validate_and_save", validate_and_save)

    # workflow.set_entry_point("ingest_documents")
    workflow.add_edge(START, "read_creditlens_template")
    workflow.add_edge("read_creditlens_template", "annual_report_parser")
    workflow.add_edge("annual_report_parser", "source_language")
    workflow.add_edge("source_language", "select_pages")
    #workflow.add_edge("select_pages", "connect_llm")
    workflow.add_edge("select_pages", "keyword_search")
    workflow.add_edge("keyword_search", "connect_llm")
    workflow.add_edge("connect_llm", "answer_questions")
    workflow.add_edge("answer_questions", "create_excel_output")
    workflow.add_edge("create_excel_output", "complete")
    # workflow.add_edge("ingest_documents", "load_document")
    # workflow.add_edge("load_document", "parse_document")
    # workflow.add_edge("parse_document", "extract_metrics")
    # workflow.add_edge("extract_metrics", "validate_and_save")
    # workflow.add_edge("validate_and_save", END)
    workflow.add_edge("complete", END)

    return workflow.compile()