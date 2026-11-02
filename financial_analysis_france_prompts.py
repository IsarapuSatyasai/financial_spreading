ltu_france_financial_analysis_prompts_dict = {
    "General": """
    Identify and extract the additional information for all years:
    - Financial analysis of: (Company Name)
    - Qualified or unqualified: (Qualification Status)
    - Source: (Origination System of input and years)
    - Consolidated or non-consolidated: (Consolidation Status)
    - Amounts printed in: (Units, e.g., Thousands) 
    - Currency: (currency, e.g., EUR)
    - MFA ID: (MFA ID)
    """,
    "Key figures": """
    Identify and extract the years mentioned in the document. Populate the extracted values into the table format provided above. Ensure the extracted values correspond accurately to the respective years. If any value is not available for a specific year, leave the cell blank. The document may contain multiple formats and sections. Ensure to extract the values accurately from the relevant financial statements sections. No additional note nor title is needed. For each year, extract the following numerical values:
    - **Revenues**
    - **Net Income**
    - **Net Cash Flow from operations**
    - **Total Assets**
    - **Solvency %**
    - **Net Working Capital**
    - **Debt/Net worth**
    """,
    "Profitability": """Analyze the company's profitability over years, considering factors such as changes in sales, cost of goods sold (COGS), operating profit, net profit, and any other relevant financial metrics. Include specific details on how these factors have impacted the overall profitability, referencing any significant increases or decreases in costs, revenues, or other expenses. Include specific figures from the financial statements to support your analysis. If possible, convert numbers into a more readable form using terms like thousand, million, billion, or trillion. The analysis should be concise, focusing on the most impactful elements in a single paragraph.""",
    "Liquidity / Cash Flow": """Please provide an analysis of the company's liquidity and cash flow over years, focusing on the following aspects: gross and net operating cash flow, debt obligations, dividends paid, changes in net working capital, days receivable and payable, cash flow from investments, and any additional financing. Include specific figures where available and assess the overall liquidity and cash flow status. Include specific figures from the financial statements to support your analysis. If possible, convert numbers into a more readable form using terms like thousand, million, billion, or trillion. The analysis should be concise, focusing on the most impactful elements in a single paragraph.""",
    "Solvency": """Please provide an analysis of the company's solvency over years, including key metrics such as net worth, solvency ratio, changes in total assets, intercompany receivables and debts, intangible assets, long-term debts, and any other relevant financial details. Highlight any significant changes or trends and assess the overall solvency position. Include specific figures from the financial statements to support your analysis. If possible, convert numbers into a more readable form using terms like thousand, million, billion, or trillion. The analysis should be concise, focusing on the most impactful elements in a single paragraph.""",
}

ltu_france_financial_analysis_prompts_dict_additional = {
    "Profitability (additional insights from the annual report)": """
    **Objective:**
    Analyze a company’s profitability using its annual report, focusing on **underlying drivers, strategic decisions, and external factors** rather than surface-level trends. Structure your analysis to answer: *“Why are profitability metrics changing, and what does this reveal about the company’s competitive position and sustainability?”*  

    ---
    **Instructions:**
    1. **Context Setup:**  
    - Briefly summarize the company’s industry, core business model, and key financial metrics (e.g., gross margin, operating margin, net margin trends over 3–5 years).  

    2. **Deep Dive into Drivers:**  
    For each profitability metric, **explain the “why”** using qualitative and quantitative evidence from the report:  
    - **Gross Profit Margin:**  
        - Investigate COGS drivers: Input cost inflation, supplier negotiations, production efficiency, or pricing power.  
        - Example: *“If gross margin declined despite revenue growth, is the company absorbing higher material costs due to weak pricing power?”*  
    - **Operating Profit Margin:**  
        - Link SG&A/R&D expenses to strategic priorities (e.g., market expansion, digital transformation).  
        - Highlight one-time costs (e.g., layoffs, lawsuits) vs. structural shifts.  
    - **Net Profit Margin:**  
        - Assess interest burden (debt levels), tax strategies, and non-operational income (e.g., asset sales).  

    3. **Revenue Quality & Cash Flow:**  
    - Differentiate between volume-driven vs. price-driven revenue growth.  
    - Compare net income to operating cash flow. Flag working capital issues (e.g., rising receivables/inventory).  

    4. **External & Strategic Factors:**  
    - **Industry Context:** Cyclical pressures, disruption risks, or regulatory changes (e.g., carbon taxes, tariffs).  
    - **Management Decisions:** Capital allocation (dividends vs. reinvestment), M&A impact, or long-term bets (e.g., R&D).  
    - **Hypothetical Scenarios:** *“Could a 10% rise in interest rates cripple net margins given current debt?”*  

    5. **Synthesis:**  
    - Connect the dots: Are profitability drivers sustainable (e.g., patented tech, loyal customer base) or temporary (e.g., cost-cutting)?  
    - Conclude with the company’s **competitive moat** (or lack thereof) and risks to future profitability.  
    """,
    "Liquidity / Cash Flow (additional insights from the annual report)": """
    **Objective:**  
    Evaluate the company’s liquidity and cash flow health using its annual report, focusing on **short-term solvency, cash generation efficiency, and risks to financial flexibility**. Answer: *“Can the company meet its obligations, fund operations, and invest in growth without excessive reliance on external financing?”*  

    ---  
    **Instructions:**  
    1. **Context Setup:**  
    - Summarize the company’s industry, business model (e.g., capital-intensive vs. asset-light), and key liquidity metrics (e.g., current ratio, quick ratio, operating cash flow trends over 3–5 years).  

    2. **Deep Dive into Cash Flow Drivers:**  
    - **Operating Cash Flow (OCF):**  
        - Analyze cash conversion efficiency: Compare net income to OCF.  
        - Investigate working capital changes:  
        - Rising receivables: Are customers delaying payments? Is there customer concentration risk?  
        - Inventory buildup: Is the company overproducing or facing obsolescence?  
        - Payables: Are suppliers tightening credit terms?  
        - Example: *“If OCF declined despite stable net income, is working capital draining cash (e.g., inventory +20% YoY)?”*  
    - **Investing Cash Flow:**  
        - Capital expenditures (CapEx): Are investments aligned with growth (e.g., new factories) or maintenance (e.g., replacing old equipment)?  
        - Asset sales: Is the company divesting to raise emergency cash?  
    - **Financing Cash Flow:**  
        - Debt issuance/repayment: Is the company refinancing maturing debt? Are interest rates rising?  
        - Dividends/buybacks: Are shareholder returns sustainable relative to free cash flow?  

    3. **Liquidity Risk Assessment:**  
    - **Short-Term Obligations:**  
        - Compare cash reserves + short-term investments to current liabilities.  
        - Calculate liquidity ratios (current ratio, quick ratio). Identify trends (e.g., declining quick ratio due to inventory bloat).  
    - **Debt Maturity Profile:**  
        - Are large debt repayments due soon? Can the company refinance at reasonable rates?  
    - **Contingent Liabilities:**  
        - Do guarantees, lawsuits, or off-balance-sheet commitments threaten liquidity?  

    4. **External & Strategic Factors:**  
    - **Industry Dynamics:**  
        - Cyclical businesses (e.g., construction) may face seasonal cash crunches.  
        - Subscription-based models (e.g., SaaS) often have predictable OCF.  
    - **Management Strategy:**  
        - Aggressive growth (high CapEx) vs. austerity (cost-cutting).  
        - Reliance on short-term debt (rollover risk) vs. long-term financing.  
    - **Macro Risks:**  
        - Example: *“Could a credit market freeze limit the company’s ability to refinance?”*  

    5. **Synthesis:**  
    - **Cash Flow Sustainability:**  
        - Is the company funding operations through organic cash flow or debt/equity raises?  
        - Are dividends/buybacks supported by free cash flow, or are they eroding liquidity?  
    - **Red Flags vs. Strengths:**  
        - Red flags: Negative OCF, shrinking cash reserves, rising debt/EBITDA.  
        - Strengths: Strong cash conversion cycle, conservative leverage, diversified funding sources.   
    """,
    "Solvency (additional insights from the annual report)": """
    **Objective:**  
    Assess the company’s long-term solvency and ability to meet its debt obligations using its annual report. Focus on **capital structure sustainability, debt repayment capacity, and risks to financial stability**. Answer: *“Can the company service its debt, avoid bankruptcy, and sustain operations through economic cycles?”*  

    ---  
    **Instructions:**  
    1. **Context Setup:**  
    - Briefly summarize the company’s industry (e.g., capital-intensive vs. asset-light), business model, and key solvency metrics (e.g., debt-to-equity ratio, interest coverage ratio, debt-to-EBITDA) over 3–5 years.  

    2. **Deep Dive into Solvency Drivers:**  
    - **Debt Load Analysis:**  
        - **Debt-to-Equity Ratio:** Is the company becoming overleveraged? Compare to industry peers.  
        - **Debt-to-EBITDA:** How many years of earnings are needed to repay debt? A ratio >4x often signals risk.  
    - **Interest Coverage:**  
        - Calculate EBIT / Interest Expense. Can operating profits comfortably cover interest payments?  
        - Example: *“If interest coverage fell to 2x, does a downturn risk default?”*  
    - **Debt Maturity Profile:**  
        - When are major debt repayments due? Is there a “maturity wall” requiring refinancing in a high-rate environment?  
        - Assess refinancing risk: Are credit ratings stable or deteriorating?  

    3. **Cash Flow Adequacy:**  
    - **Free Cash Flow to Debt (FCF/Debt):** Can organic cash flow reduce debt?  
    - **Debt Covenants:** Are there restrictive terms (e.g., minimum liquidity ratios) the company might breach?  
    - **Asset Liquidation Value:** In distress, could asset sales (e.g., real estate, IP) cover liabilities?  

    4. **External & Strategic Factors:**  
    - **Industry Risks:** Cyclical industries (e.g., airlines) face solvency risks during downturns.  
    - **Management Strategy:**  
        - Debt-funded acquisitions vs. equity issuance.  
        - Dividend policies: Are payouts draining cash needed for debt repayment?  
    - **Macro Risks:** Rising interest rates, inflation, or currency devaluation (for foreign-denominated debt).  

    5. **Synthesis:**  
    - **Sustainability of Capital Structure:**  
        - Is debt growth outpacing earnings or cash flow?  
        - Can the company generate sufficient EBITDA to deleverage?  
    - **Red Flags vs. Strengths:**  
        - Red flags: Declining interest coverage, shrinking equity cushion, covenant breaches.  
        - Strengths: Long debt maturities, strong FCF generation, conservative leverage ratios.  
    """,
}
