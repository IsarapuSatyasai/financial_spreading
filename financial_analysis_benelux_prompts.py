ltu_benelux_financial_analysis_prompts_dict = {
    "General": """
    Identify and extract the additional information for all years:
    - Financial analysis of: (Company Name)
    - Qualified or unqualified: (Qualification Status)
    - Source: (Origination System of input and years)
    - Consolidated or non-consolidated: (Consolidation Status)
    - Amounts printed in: (Units, e.g., Thousands) 
    - Currency: (currency, e.g., EUR)
    """,
    "Key figures": """
    Identify and extract the years mentioned in the document. Populate the extracted values into the table format provided above. Ensure the extracted values correspond accurately to the respective years. If any value is not available for a specific year, leave the cell blank. The document may contain multiple formats and sections. Ensure to extract the values accurately from the relevant financial statements sections. No additional note nor title is needed. For each year, extract the following numerical values:
    - **Revenues**
    - **Net Income**
    - **Net Cash Flow from operations**
    - **Total Assets**
    - **Solvency %**
    - **Net Working Capital**
    """,
    "Profitability": """Analyze the company's profitability over years, considering factors such as changes in sales, cost of goods sold (COGS), operating profit, net profit, and any other relevant financial metrics. Include specific details on how these factors have impacted the overall profitability, referencing any significant increases or decreases in costs, revenues, or other expenses. Include specific figures from the financial statements to support your analysis. If possible, convert numbers into a more readable form using terms like thousand, million, billion, or trillion. The analysis should be concise, focusing on the most impactful elements in a single paragraph. All numerical values exclusively represent the target currency. Always use the target currency for all financial analysis.""",
    "Liquidity / Cash Flow": """Please provide an analysis of the company's liquidity and cash flow, focusing on the following aspects: gross and net operating cash flow, debt obligations, dividends paid, changes in net working capital, days receivable and payable, cash flow from investments, and any additional financing. Include specific figures where available and assess the overall liquidity and cash flow status. Include specific figures from the financial statements to support your analysis. If possible, convert numbers into a more readable form using terms like thousand, million, billion, or trillion. The analysis should be concise, focusing on the most impactful elements in a single paragraph. All numerical values exclusively represent the target currency. Always use the target currency for all financial analysis.""",
    "Solvency": """Please provide an analysis of the company's solvency, including key metrics such as net worth, solvency ratio, changes in total assets, intercompany receivables and debts, intangible assets, long-term debts, and any other relevant financial details. Highlight any significant changes or trends and assess the overall solvency position. Include specific figures from the financial statements to support your analysis. If possible, convert numbers into a more readable form using terms like thousand, million, billion, or trillion. The analysis should be concise, focusing on the most impactful elements in a single paragraph. All numerical values exclusively represent the target currency. Always use the target currency for all financial analysis.""",
}

ltu_benelux_financial_analysis_prompts_dict_additional = {
    "Profitability (additional insights from the annual report)": """
    **Instructions:**  
    Analyze and summarize **revenue, COGS, and profit** using the following structure:  

    1. **Revenue Analysis**  
    - Key drivers of revenue change (e.g., product lines, volumes, demand, geographic markets, pricing strategies, impact of market price, acquisitions, disposals of group companies), indlucing specific years.  

    2. **Cost of Goods Sold (COGS) Analysis**  
    - Factors influencing COGS (e.g., raw material costs, labor, inflation, supply chain efficiencies), indlucing specific years.  

    3. **Profit Analysis**   
    - Key factors affecting profitability (e.g., cost controls, pricing, one-time expenses, extraordinary expenses, extraordinary income, depreciations, amortizations), indlucing specific years. 

    4. **Key Takeaways**  
    - Strengths (e.g., revenue growth outpacing COGS rise).  
    - Weaknesses (e.g., shrinking margins due to cost inflation).  
    - Critical risks or opportunities (e.g., dependency on a single revenue stream).  
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
    - Identify risks or red flags (e.g., declining OCF with rising debt, covenant breaches).  
    - Conclude with an overall liquidity risk assessment and recommendations to strengthen cash resilience (e.g., optimizing working capital, refinancing strategies).  
    """,
    "Solvency (additional insights from the annual report)": """
    **Instructions:**  
    Analyze and summarize **Statement of Changes in Equity** indlucing specific years and using the following structure:  

    1. **Statement of Changes in Equity**  
    - Identify key drivers of equity fluctuations (e.g., retained earnings, dividends, share buybacks, or revaluation reserves).  
    - Assess if equity growth aligns with profitability. Are dividends sustainable, or do they erode equity?  
    - Link equity trends to solvency (e.g., shrinking equity may signal reliance on debt).  

    2. **Overall Solvency Assessment**  
    - Synthesize findings: Does the company have sufficient net worth and cash flow to withstand financial stress?  
    - Based on the data provided above, evaluate the company's overall ability to meet its long-term obligations.
    - Highlight red flags (e.g., negative equity, deteriorating solvency ratios) or strengths (e.g., strong equity growth).  
    - Provide recommendations (e.g., reduce debt, retain earnings, or improve liquidity). 
    """,
}
