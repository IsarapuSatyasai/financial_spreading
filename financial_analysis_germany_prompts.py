ltu_germany_financial_analysis_prompts_dict = {
    "General": """
    Identify and extract the additional information for all years:
    - Financial analysis of: (Company Name)
    - Qualified or unqualified: (Qualification Status)
    - Source: (Origination System of input and dates)
    - Consolidated or non-consolidated: (Consolidation Status)
    - Amounts printed in: (Units, e.g., Thousands) 
    - Currency: (currency, e.g., EUR)
    """,
    "Key figures": """
    Identify and extract the years mentioned in the document. Populate the extracted data into the table format above, ensuring that the rows are sorted chronologically from the oldest to the newest year. If any value is not available for a specific year, leave the cell blank. The document may contain multiple formats and sections. Ensure to extract the values accurately from the relevant financial statements sections. No additional note nor title is needed. For each year, extract the following numerical values:
    - **Revenues**
    - **Net Income**
    - **Gross Operating Cash Flow**
    - **Total Assets**
    - **Solvency %**
    - **Net Working Capital**
    """,
    "Profitability": """Analyze the company's profitability over years, considering factors such as changes in sales, cost of goods sold (COGS), operating profit, net profit, and any other relevant financial metrics. Include specific details on how these factors have impacted the overall profitability, referencing any increases or decreases in costs, revenues, or other expenses. Include specific figures from the financial statements to support your analysis. Where applicable, express monetary values in EUR and convert large numbers into a more readable format using terms like k (thousand), mln (million), or bln (billion).""",
    "Liquidity / Cash Flow": """Analyze the company's liquidity and cash flow over years, considering factors such as changes in gross and net operating cash flow, debt obligations, dividends paid, changes in net working capital, days receivable and payable, days inventories, current ratio and any additional financing. Additionally, calculate and assess a metric derived from gross operating cash flow minus financing payments, and explain its significance in evaluating the company’s financial flexibility. Include specific figures where available and assess the overall liquidity and cash flow status. Include specific figures from the financial statements to support your analysis. Where applicable, express monetary values in EUR and convert large numbers into a more readable format using terms like k (thousand), mln (million), or bln (billion).""",
    "Solvency": """Analyze the company's solvency, considering factors such as changes in risk bearing capital, Risk Bearing Cap / Total Assets, changes in total assets, intercompany receivables and debts, intangible assets, long-term debts, and any other relevant financial details. Highlight any changes or trends and assess the overall solvency position. Include specific figures from the financial statements to support your analysis. Where applicable, express monetary values in EUR and convert large numbers into a more readable format using terms like k (thousand), mln (million), or bln (billion).""",
}

ltu_germany_financial_analysis_prompts_dict_additional = {
    "Profitability (additional insights from the annual report)": """
    **Instructions:**  
    Analyze and summarize **revenue, COGS, and profit** using the following structure:  

    1. **Introduction**  
    - Briefly summarize the company’s industry, core business model, and key financial metrics (e.g., gross margin, operating margin, net margin trends over 3–5 years).  

    2. **Revenue Analysis**  
    - Key drivers of revenue change (e.g., product lines, volumes, demand, geographic markets, pricing strategies, impact of market price, acquisitions, disposals of group companies), indlucing specific years.  

    3. **Cost of Goods Sold (COGS) Analysis**  
    - Factors influencing COGS of the company indlucing specific years.

    4. **Profit Analysis**   
    - Key factors affecting profitability (e.g., cost controls, pricing, one-time expenses, extraordinary expenses, extraordinary income, depreciations, amortizations), indlucing specific years. 

    5. **Key Takeaways**  
    - Strengths (e.g., revenue growth outpacing COGS rise).  
    - Weaknesses (e.g., shrinking margins due to cost inflation).  
    - Critical risks or opportunities (e.g., dependency on a single revenue stream).  

    Only use consolidated figures. If a specific example is provided, incorporate its details only if relevant data is available; otherwise, omit any mention of the example.
    """,
    "Liquidity / Cash Flow (additional insights from the annual report)": """
    **Instructions:**  
    Analyze and summarize **Operating cash flow, cash from investments, cash flow from financing, used credit facility, unused credit facilities** indlucing specific years and using the following structure:  

    1. **Operating cash flow (OCF)**  
    - How much cash does the company generate through the operating cash flow?
    - Hom much cash (on the balance sheet) does the company has per year end and what is the net cash?
    - Has the company access to cash? This can be via capital increase, unused credit facilities, additional debts, if for example the net debts/EBITDA ratio is low the company is more likely to be able to lend extra money which might not be the case is net debt/EBITDA ratio is high)
 
    2. **Cash from Investing Activities**  
    - Discuss the impact of these activities on liquidity and long-term operational capacity, indlucing specific years.  

    3. **Cash Flow from Financing Activities**  
    - Identify sources/uses (e.g., debt issuance/repayment, equity transactions, dividends), indlucing specific years.  
    - Assess reliance on external financing to fund operations or growth.  
    - Note any dividend policies or share buybacks affecting liquidity.  

    4. **Credit Facilities:**  
    - **Used Credit Facility:** Quantify drawn amounts, repayment terms, and interest obligations. Evaluate reliance on credit for liquidity needs.  
    - **Unused Credit Facility:** Determine remaining availability, covenant compliance, and flexibility to address unexpected cash shortfalls.  

    **Overall Liquidity / Cash flow Assessment**  
    - Highlight interconnections between components (e.g., OCF funding investments vs. debt dependency).  
    - Identify strengths (e.g. strong cash conversion cycle, conservative leverage, diversified funding sources).
    - Identify risks or red flags (e.g., Negative OCF, shrinking cash reserves, rising debt/EBITDA).  
    - Conclude with an overall liquidity risk assessment and recommendations to strengthen cash resilience (e.g., optimizing working capital, refinancing strategies).  

    Only use consolidated figures. If a specific example is provided, incorporate its details only if relevant data is available; otherwise, omit any mention of the example.
    """,
    "Solvency (additional insights from the annual report)": """
    **Instructions:**  
    Analyze and summarize **Statement of Changes in Equity** indlucing specific years and using the following structure:  

    1. **Statement of Changes in Equity**  
    - Identify key drivers of equity fluctuations (e.g., retained earnings, dividends, or share buybacks).  
    - Assess if equity growth aligns with profitability. Are dividends sustainable, or do they erode equity?  
    - Link equity trends to solvency (e.g., shrinking equity may signal reliance on debt).  

    2. **Overall Solvency Assessment**  
    - Synthesize findings: Does the company have sufficient net worth and cash flow to withstand financial stress?  
    - Based on the data provided above, evaluate the company's overall ability to meet its long-term obligations.
    - Highlight red flags (e.g., negative equity, deteriorating solvency ratios) or strengths (e.g., strong equity growth).  
    - Provide recommendations (e.g., reduce debt, retain earnings, or improve liquidity). 

    Only use consolidated figures. If a specific example is provided, incorporate its details only if relevant data is available; otherwise, omit any mention of the example.
    """,
}
