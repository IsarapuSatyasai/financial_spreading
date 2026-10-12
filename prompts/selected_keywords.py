import re
import unicodedata


FINANCIAL_TERMS = [
    "balance sheet",
    "statement of financial position",
    "income statement",
    "statement of profit and loss",
    "profit and loss account",
    "statement of comprehensive income",
    "cash flow statement",
    "statement of cash flows",
    "statement of changes in equity",
    "total assets",
    "current assets",
    "non current assets",
    "fixed assets",
    "intangible assets",
    "property plant and equipment",
    "accounts receivable",
    "trade receivables",
    "inventories",
    "cash and cash equivalents",
    "total liabilities",
    "current liabilities",
    "non current liabilities",
    "accounts payable",
    "trade payables",
    "borrowings",
    "long term debt",
    "short term debt",
    "lease liabilities",
    "total equity",
    "share capital",
    "retained earnings",
    "revenue",
    "total revenue",
    "net revenue",
    "sales",
    "net sales",
    "cost of sales",
    "gross profit",
    "operating income",
    "operating profit",
    "operating expenses",
    "finance costs",
    "interest expense",
    "depreciation",
    "amortisation",
    "amortization",
    "profit before tax",
    "profit after tax",
    "net profit",
    "net income",
    "profit for the year",
    "loss for the year",
    "earnings per share",
    "ebit",
    "ebitda",
    "operating activities",
    "investing activities",
    "financing activities",
    "net cash flow",
    "capital expenditure",
    "financial highlights",
    "financial summary",
    "financial performance",
    "financial position",
    "segment reporting",
    "related party transactions",
    "contingent liabilities",
    "financial instruments",
    "working capital",
    "net debt",
    "total debt",
]

STRONG_FINANCIAL_TERMS = [
    "balance sheet",
    "statement of financial position",
    "income statement",
    "statement of profit and loss",
    "statement of comprehensive income",
    "statement of cash flows",
    "cash flow statement",
    "statement of changes in equity",
    "consolidated financial statements",
    "consolidated balance sheet",
    "consolidated income statement",
    "notes to the financial statements",
    "total assets",
    "total liabilities",
    "total equity",
    "profit before tax",
    "profit after tax",
]

UNIT_TERMS = [
    "in thousands",
    "in thousand",
    "in millions",
    "in million",
    "in billions",
    "in billion",
    "thousands of dollars",
    "millions of dollars",
    "thousands of euros",
    "millions of euros",
    "amounts in",
    "figures in",
    "usd",
    "eur",
    "gbp",
    "inr",
    "currency",
    "$",
    "€",
    "£",
]

DUTCH_TERMS = [
    "balans",
    "winst-en-verliesrekening",
    "kasstroomoverzicht",
    "totale activa",
    "totale passiva",
    "eigen vermogen",
    "bedrijfsopbrengsten",
    "nettowinst",
    "financiele positie",
    "financiele resultaten",
]

GERMAN_TERMS = [
    "bilanz",
    "gewinn- und verlustrechnung",
    "kapitalflussrechnung",
    "gesamte aktiva",
    "gesamte passiva",
    "eigenkapital",
    "umsatzerlose",
    "jahresuberschuss",
    "finanzlage",
    "finanzergebnis",
]

FRENCH_TERMS = [
    "bilan",
    "compte de resultat",
    "tableau des flux de tresorerie",
    "total de l actif",
    "total du passif",
    "capitaux propres",
    "chiffre d affaires",
    "resultat net",
    "situation financiere",
    "resultat financier",
]

LOW_VALUE_TERMS = [
    "table of contents",
    "glossary",
    "index",
    "contact us",
    "contact details",
    "corporate directory",
    "management team",
    "notice of meeting",
]

all_keywords = list(
    dict.fromkeys(
        FINANCIAL_TERMS
        + STRONG_FINANCIAL_TERMS
        + UNIT_TERMS
        + DUTCH_TERMS
        + GERMAN_TERMS
        + FRENCH_TERMS
    )
)


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKD", str(text).lower())
    text = "".join(
        char for char in text
        if not unicodedata.combining(char)
    )
    text = text.replace("&", " and ")
    text = re.sub(r"[^\w]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def contains_phrase(text: str, phrase: str) -> bool:
    text = normalize_text(text)
    phrase = normalize_text(phrase)

    if not text or not phrase:
        return False

    return re.search(
        r"(?<!\w)" + re.escape(phrase) + r"(?!\w)",
        text,
    ) is not None


def page_score(text: str) -> int:
    return sum(
        1 for keyword in all_keywords
        if contains_phrase(text, keyword)
    )


def numeric_density(text: str) -> float:
    tokens = str(text).split()

    if not tokens:
        return 0.0

    numbers = re.findall(
        r"(?<!\w)\(?[-+]?\d[\d,]*(?:\.\d+)?%?\)?(?!\w)",
        str(text),
    )

    return min(len(numbers) / len(tokens), 1.0)


def table_structure_score(text: str) -> float:
    lines = [
        line.strip()
        for line in str(text).splitlines()
        if line.strip()
    ]

    if not lines:
        return 0.0

    numeric_lines = sum(
        1 for line in lines
        if len(re.findall(r"\d[\d,.]*", line)) >= 2
    )

    score = min(
        (numeric_lines / len(lines)) * 2,
        2.0,
    )

    if any(re.search(r"\s{2,}|\t|\|", line) for line in lines):
        score += 1.0

    return min(score, 3.0)


def page_relevance_score(text: str) -> dict:
    normalized_text = normalize_text(text)

    if not normalized_text:
        return {
            "score": 0.0,
            "keyword_matches": [],
        }

    keyword_matches = [
        keyword for keyword in all_keywords
        if contains_phrase(normalized_text, keyword)
    ]

    strong_matches = [
        term for term in STRONG_FINANCIAL_TERMS
        if contains_phrase(normalized_text, term)
    ]

    unit_matches = [
        term for term in UNIT_TERMS
        if contains_phrase(normalized_text, term)
    ]

    years = set(re.findall(r"\b(?:19|20)\d{2}\b", text))
    number_density = numeric_density(text)
    table_score = table_structure_score(text)

    score = (
        min(len(strong_matches) * 3.0, 12.0)
        + min(len(keyword_matches) * 1.0, 10.0)
        + min(len(unit_matches) * 1.5, 4.5)
        + min(len(years) * 0.75, 3.0)
        + min(number_density * 30.0, 5.0)
        + table_score
    )

    penalty = sum(
        1.0 for term in LOW_VALUE_TERMS
        if contains_phrase(normalized_text, term)
    )

    if len(normalized_text.split()) < 30:
        penalty += 1.0

    score = max(score - min(penalty, 3.0), 0.0)

    return {
        "score": round(score, 2),
        "keyword_matches": keyword_matches,
    }