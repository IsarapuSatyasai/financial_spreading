import io
import logging
import re
from copy import deepcopy
from pathlib import Path

import fitz
from custom_lcel_components.ingest import load_document
from custom_lcel_components.word_template_utils import (
    prepare_input,
    replace_cell_text_keep_format,
    replace_section,
)
from docx import Document
from docx.oxml import OxmlElement
from docx.shared import Inches
from docx.text.paragraph import Paragraph

logger = logging.getLogger(__name__)

TEMPLATE_PATH = Path(__file__).with_name("Credit-Report-Template-Rabobank.docx")


def generate_final_response(_dir):
    """
    Combine and order response sections from multiple report-generation sources.

    The function aggregates response sections from:

        - ``_dir["financial_analysis"]["financial_analysis_responses"]``:
          Financial analysis response sections.
        - ``_dir["annual_report"]["agent_responses"]``:
          Agent-generated annual report sections.
        - ``_dir["annual_report"]["rag_responses"]``:
          RAG-generated annual report sections.

    Any missing keys, ``None`` values, or empty response lists are treated as
    empty collections and ignored during aggregation.

    The combined responses are sorted according to a predefined section
    hierarchy defined in ``order``. Sections whose titles are not present in
    the hierarchy are placed after all ordered sections. Their relative order
    among themselves is preserved by Python's stable sorting behavior.

    Args:
        _dir (dict): Dictionary containing report-generation outputs. Expected
            structure::

                {
                    "financial_analysis": {
                        "financial_analysis_responses": list[dict]
                    },
                    "annual_report": {
                        "agent_responses": list[dict],
                        "rag_responses": list[dict]
                    }
                }

    Returns:
        list[dict]: Combined and ordered list of response sections. Sections
        matching entries in the predefined ordering appear first, followed by
        any unmatched sections.
    """
    responses = (
        (_dir.get("financial_analysis") or {}).get("financial_analysis_responses", [])
        + (_dir.get("annual_report") or {}).get("agent_responses", [])
        + (_dir.get("annual_report") or {}).get("rag_responses", [])
    )

    order = [
        "Warning",
        "Business description (include Connected Clients)",
        "Emerging Risks",
        "ESG and Climate and Environmental Risk Assessment$Climate and Environmental Risk Assessment (CERA)",
        "ESG and Climate and Environmental Risk Assessment$Climate-related reputational and litigation risks",
        "ESG and Climate and Environmental Risk Assessment$ESG screening",
        "Sector Outlook",
        "Management, organization and strategy of the company",
        "Financial performance realised and projected",
        "Financial performance realised and projected$Key figures (x EUR mln)",
        "Financial performance realised and projected$Profitability",
        "Financial performance realised and projected$Liquidity / Cash Flow",
        "Financial performance realised and projected$Solvency",
    ]

    order_map = {title: idx for idx, title in enumerate(order)}

    final_response = sorted(
        responses, key=lambda item: order_map.get(item["title"], len(order))
    )

    return final_response


def get_warning_message(_dict):
    """
    Extract the warning message from a report response dictionary.

    Returns
    -------
    str
        "⚠ WARNING: <message>" if found, otherwise an empty string.
    """
    items = _dict.get("responses", [])

    for item in items:
        if item.get("title") == "Warning":
            answer = item.get("answer", "").strip()
            if answer:
                return f"⚠ WARNING: {answer}"

    return ""


def populate_credit_report(_dict):
    """
    Populate a Rabobank credit report Word document using client data and
    generated analysis content.

    This function loads the credit report template, inserts any applicable
    warning message, populates the client name, and replaces the content of
    predefined report sections with generated answers. The resulting document
    is returned as a modified ``python-docx`` Document object.

    Args:
        _dict (dict): Input data containing client information and report
            attributes used to generate warnings, company details, and
            section content.

    Returns:
        Document: A populated ``python-docx`` Document instance representing
        the completed credit report.

    Notes:
        - The report is based on the
          ``Credit-Report-Template-Rabobank.docx`` template.
        - Warning messages are inserted immediately before the
          "Introduction (incl. request and rationale)" heading.
        - The client name is populated in the first table at row 0,
          column 1, as required by the template structure.
        - Section content is generated from ``final_response`` via
          ``prepare_input()`` and inserted using ``replace_section()``.
    """
    doc = Document(TEMPLATE_PATH)

    warning_text = get_warning_message(_dict)
    if warning_text:
        for para in doc.paragraphs:
            if para.text.strip() == "Introduction (incl. request and rationale)":
                # Create new paragraph XML
                new_p = OxmlElement("w:p")
                para._p.addprevious(new_p)

                warning_para = Paragraph(new_p, para._parent)
                warning_para.add_run(warning_text).bold = True
                break

    # add client_name
    client_name = _dict["company_name"]
    if client_name:
        # The client name cell is always expected to be located in the first table
        # (row 0, column 1). We use a fixed index because the original template
        # requires the field to be populated in this specific cell and does not
        # provide a reliable identifier or condition for dynamic lookup.
        client_name_cell = doc.tables[0].rows[0].cells[1]
        replace_cell_text_keep_format(client_name_cell, client_name)

    sections = [
        ("Business description (include Connected Clients)", "Emerging Risks"),
        ("Emerging Risks", "Customer Due Diligence"),
        ("ESG and Climate and Environmental Risk Assessment", "Sector outlook"),
        ("Sector outlook", "Management, organization and strategy of the company"),
        ("Management, organization and strategy of the company", "Client intimacy"),
        (
            "Financial performance realised and projected",
            "Structure analysis & Protection",
        ),
        ("Structure analysis & Protection", "Risk parameters"),
    ]

    answer_map = prepare_input(_dict["responses"])

    for start_heading, end_heading in sections:
        replace_section(
            doc=doc,
            start_heading=start_heading,
            end_heading=end_heading,
            answer=answer_map.get(start_heading, ""),
        )

    # When CreditLens is available, it will be converted into an image and included in the appendix of the credit report.
    if _dict["credit_lens_source"]:
        pdf = load_document(_dict, "fitz", "credit_lens_source")
        insert_pdf_pages_at_placeholder(doc, pdf)

    # When an existing credit report is available, Part 1 of the report will be appended to the credit report appendix after the "Previous decision" section.
    if _dict["existing_credit_report"]:
        try:
            existing_credit_report_doc = load_document(
                _dict, source_key="existing_credit_report"
            )
            insert_tables_before_marker(existing_credit_report_doc, doc)

        except Exception as e:
            logger.warning(
                "Failed to load existing_credit_report. Skipping table insertion. Error: %s",
                e,
            )

    return doc


def insert_pdf_pages_at_placeholder(
    template_doc, pdf, placeholder="CreditLens reports"
):
    """
    Find the second occurrence of a placeholder paragraph in a Word document
    and insert all PDF pages as images immediately after it.

    Args:
        template_doc: python-docx Document object
        pdf: fitz.Document (PyMuPDF PDF document)
        placeholder: paragraph text to search for
    """

    matches = [
        p for p in template_doc.paragraphs
        if p.text.strip() == placeholder
    ]

    p = matches[1]  # second occurrence
    last_element = p._element

    for page_num in range(len(pdf)):
        page = pdf[page_num]

        # Render page to image
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

        # Convert image to stream
        img_stream = io.BytesIO(pix.tobytes("png"))

        # Create paragraph with image
        img_para = template_doc.add_paragraph()
        img_para.add_run().add_picture(img_stream, width=Inches(6.5))

        # Insert after second placeholder
        last_element.addnext(img_para._element)
        last_element = img_para._element


def insert_tables_before_marker(
    src_doc,
    template_doc,
    marker_text: str = "Part 2",
    insert_after_paragraph: str = "Previous decision",
) -> None:
    """
    Insert tables from a source Word document into a template document.

    The function copies all tables that appear before the first table whose
    first cell in the first row matches `marker_text`. The copied tables are
    inserted into `template_doc` immediately after the second paragraph whose
    text matches `insert_after_paragraph`, preserving the original table
    structure and formatting.

    Args:
        src_doc:
            Source `python-docx` Document containing the tables to copy.
        template_doc:
            Target `python-docx` Document where tables will be inserted.
        marker_text:
            Text expected in the first cell of the first row of the marker
            table. All tables before this table are copied.
            Defaults to `"Part 2"`.
        insert_after_paragraph:
            Paragraph text in `template_doc` after whose second occurrence
            the copied tables will be inserted.
            Defaults to `"Previous decision"`.

    Returns:
        None. The function modifies `template_doc` in place.

    Notes:
        - Empty tables are ignored.
        - If no table starting with `marker_text` is found, a warning is logged
          and no tables are inserted.
        - If fewer than two matching insertion paragraphs are found, a warning
          is logged and no tables are inserted.
        - Table XML elements are deep-copied to preserve formatting and content.
    """
    table_index = None

    # Find the marker table
    for i, table in enumerate(src_doc.tables):
        if not table.rows:
            continue

        first_row = table.rows[0]

        if not first_row.cells:
            continue

        first_cell_text = first_row.cells[0].text.strip()

        if first_cell_text == marker_text:
            table_index = i
            break

    if table_index is None:
        logger.warning(
            f"Could not find the table starting with '{marker_text}'. "
            "No tables will be inserted."
        )
        return

    # Find the second occurrence of the insertion paragraph
    match_count = 0
    insert_para = None

    for paragraph in template_doc.paragraphs:
        if paragraph.text.strip() == insert_after_paragraph:
            match_count += 1

            if match_count == 2:
                insert_para = paragraph
                break

    if insert_para is None:
        logger.warning(
            f"Could not find the second occurrence of paragraph "
            f"'{insert_after_paragraph}'. Found {match_count} occurrence(s). "
            "No tables will be inserted."
        )
        return

    # Insert tables after the second matching paragraph
    anchor = insert_para._element

    for table in src_doc.tables[:table_index]:
        new_table = deepcopy(table._element)
        anchor.addnext(new_table)
        anchor = new_table
