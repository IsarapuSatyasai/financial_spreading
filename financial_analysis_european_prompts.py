ltu_europe_financial_analysis_prompts_dict = {
    "General": """
    Identify and extract the additional information for all years:
    - Financial analysis of: (Company Name)
    - Qualified or unqualified: (Qualification Status)
    - Source: (Origination System of input)
    - Dates: (All relevant statement dates covering all reporting periods)
    - Consolidated or non-consolidated: (Consolidation Status)
    - Amounts printed in: (Units, e.g., Thousands) 
    - Currency: (Target currency, e.g., EUR)
    - Key figures values (the table below) expressed in: Millions
    - MFA ID: (MFA ID)
    """,
    "Key figures": """
    Output a single Markdown table with YEARS AS ROWS (never as columns). The first column must be **Year**; all other columns are fixed metric names listed below. Return ONLY the table—no titles, notes, or commentary.

    TABLE STRUCTURE
    - Rows: One row per unique **Year** (4-digit, e.g., 2019, 2020).
    - Columns (in this exact order):
    - Year
    - Net Sales
    - Net Income
    - Gross income %
    - Sustainable EBITDA
    - Sustainable EBITDA %
    - Total Assets
    - NW / Total Assets
    - Net Working Capital
    - Debt/EBITDA
    - Financing Payment
    - Net Cash Income

    ORDERING & DEDUPLICATION
    - List years in chronological order from oldest to latest.
    - If multiple values exist for the same year, use the primary consolidated figure. If still ambiguous, choose the most recent/reliable source for that year.

    MISSING VALUES
    - If any value is not available for a specific year, leave the cell blank.

    UNIT STANDARDIZATION — DISPLAY IN MILLIONS (mln)
    - All monetary amounts must be converted and displayed in **millions** (mln), numeric only (no unit text in the cell).
    - Convert units if the source uses thousands, billions, etc. (e.g., 1,200,000 → 1.2; 2.3B → 2,300).
    - Preserve sign for negatives **except for Financing Payment**, which must always show its **absolute value**.
    - Use standard number formatting without currency symbols.
    - Recommended rounding: one decimal place for monetary values (e.g., 123.4).

    PERCENTAGES & RATIOS
    - For percentage columns (**Gross income %**, **Sustainable EBITDA %**, **NW / Total Assets**), display values with a **%** sign, rounded to one decimal (e.g., 12.3%).
    - For **Debt/EBITDA**, display as a plain numeric ratio (e.g., 3.2), no units or %.

    STRICT OUTPUT RULES
    - Do NOT create columns for years; years MUST be rows.
    - Do NOT add extra columns or text.
    - Use numeric values only in cells (except the % sign for percentage columns).
    - If the source uses labels like “FY2020” or “2020E”, map to the base year “2020”. If a fiscal year spans two calendar years, use the labeled fiscal year’s terminal year (e.g., FY2020 → 2020).

    TASK
    Populate the extracted values into the Markdown table format described above, ensuring each metric aligns to its respective year, ordered from oldest to latest, leaving blanks where data is unavailable.
    """,
    "Profitability": """Use ONLY the provided standardized income statement (P&L) figures for the most recent two fiscal years (no external assumptions, no peer benchmarks, no invented causes). If any required P&L anchor line (Revenue/Sales, Operating Profit/EBIT, Net Profit) is missing, state that the assessment is constrained.

    Task: Produce ONE concise, insight-dense paragraph (150–180 words) analyzing profitability across the two most recent fiscal years. Prioritize interpretation and judgment over description. Do NOT provide a line-by-line P&L walkthrough.

    Always include (regardless of materiality ranking):
    - Direction and strength of change in Revenue/Sales, Operating Profit (EBIT), and Net Profit (and note any sign change: profit↔loss).
    - A concluding categorical judgment: “Profitability: Strong/Adequate/Weak; Earnings quality: Strong/Adequate/Weak.”

    Materiality filter (apply before writing additional drivers beyond the anchors, do not make reference to the filter in the output and do not mention items that do not pass the filter):
    - Parameter: TOP_N = 3 (configurable).
    1) Compute year-over-year (YoY) changes for all available P&L line items (e.g., Revenue/Sales, COGS, gross profit, operating expenses, depreciation/amortization, other income/expense, interest, taxes).
    2) Set the anchor profit metric: Net Profit if available; otherwise EBIT.
    3) Rank non-anchor P&L line items by absolute YoY change in their contribution to the anchor profit change.
    4) Select candidates as the TOP_N absolute contributors.
    5) Discuss ONLY candidate items that also pass this threshold test: the item’s absolute YoY change must exceed the absolute YoY change in at least one of: Revenue/Sales, COGS, Operating Expenses (OPEX).
    6) If fewer than TOP_N items pass the threshold test, discuss only those that pass.
    Ignore all other items.

    Tie-break rule (for equal absolute YoY changes or ambiguous ranking):
    Apply the following priority order, highest first:
    (1) Core operating items (COGS, OPEX, gross profit components) over non-operating items,
    (2) Recurring items over “other/one-off” items (e.g., “Other income/expense”),
    (3) Operating items (EBIT/EBITDA-related) over below-the-line items (interest, taxes),
    (4) If still tied, choose the item with the larger absolute level in the most recent year.

    Content requirements (one paragraph, no bullet points):
    - Start with what the movement in Revenue, EBIT, and Net Profit implies about profitability trajectory and resilience (avoid narration).
    - Explain margin dynamics qualitatively (gross and/or operating), focusing on whether cost pressure or operating leverage strengthened or weakened; do not include a ratio breakdown section. Quantify only if essential and keep it minimal.
    - Discuss drivers ONLY for the material items selected by the filter, and ONLY if explicitly supported by the document; otherwise omit driver commentary (no inference or placeholders).
    - Flag profit-quality concerns only if they pass the materiality filter (e.g., profits driven by “other income” vs core operations; unusual interest/tax movement), and state the implication for sustainability.

    Output constraints:
    - Single paragraph only.
    - Use readable number formats when numbers are necessary (k/mln/bln) and prefix currency code (e.g., EUR 100k or EUR 152mln).
    - Avoid long year-by-year numeric strings; if you must quantify, keep to one level + YoY % change OR one delta + YoY %, not multiple comparisons.
    - Do not invent explanations; if the statements do not specify drivers, state the limitation briefly and proceed with judgment based on observed movements.
    """,
    "Liquidity / Cash Flow": """
    Use ONLY the provided standardized financial statement figures for the most recent two fiscal years (no external assumptions, no industry averages, no invented drivers). If any required cash flow section or Cash & Bank balance is missing, state that the assessment is constrained.

    Task: Write ONE insight-dense paragraph (150–180 words) assessing liquidity and cash flow performance across the two most recent fiscal years. Prioritize interpretation and judgment over description. Do NOT narrate individual cash flow line items.

    Materiality filter (apply before writing, do not make reference to the filter in the output and do not mention items that do not pass the filter):
    - Parameter: TOP_N = 3 (configurable).
    1) Compute year-over-year (YoY) changes for all cash flow line items and for year-end Cash & Bank.
    2) Rank cash flow line items by absolute YoY change.
    3) Select candidates as the TOP_N absolute contributors to the YoY change in total net cash movement.
    4) Discuss ONLY candidate items that also pass this threshold test: the item’s absolute YoY change must exceed the absolute change in at least one of: trade receivables, inventories, trade payables.
    5) If fewer than TOP_N items pass the threshold test, discuss only those that pass.
    Ignore all other items.

    Content requirements (in one paragraph, no bullet points):
    - Compare gross operating cash flow and net cash from operations, explaining what the movement implies about cash generation strength (do not print figures).
    - Mention investing and financing cash flows ONLY for the material items selected by the filter, stating whether they support or pressure liquidity.
    - Explain working-capital impacts (receivables, inventory, payables) as cash tightening/easing and comment on efficiency via cash impact (no DSO/DIO/DPO; quantify only if essential and keep it minimal).
    - State whether operating cash generation covers financing payments, and end with a definitive conclusion on debt service capacity and overall liquidity strength.
    - Note any material change in year-end Cash & Bank and its implication for liquidity.

    Output constraints:
    - Single paragraph only.
    - No ratio breakdowns.
    - No “YYYY: X vs Y” or other year-by-year numeric strings.
    - No parenthetical numeric comparisons.
    - End with a clear categorical judgment: “Debt service capacity: Strong/Adequate/Weak; Liquidity: Strong/Adequate/Weak.
    """,
    "Solvency": """Use ONLY the provided standardized balance sheet and debt metrics for the most recent two fiscal years (no external assumptions, no peer benchmarks, no invented causes). If any required anchor metric (Risk-bearing capital, Total assets, Long-term interest-bearing debt, Cash & equivalents or debt, EBITDA if debt/EBITDA is provided) is missing, state that the assessment is constrained.

    Task: Produce ONE concise, insight-dense paragraph (150–180 words) analyzing solvency across the two most recent fiscal years. Prioritize interpretation and credit judgment over description. Do NOT provide a line-by-line balance sheet walkthrough.

    Always include (regardless of materiality ranking):
    - Direction of change in risk-bearing capital and in Risk-bearing capital / Total assets, and what that implies for capital adequacy.
    - Direction of change in total assets and whether asset growth (if any) appears debt-funded or capital-funded.
    - Direction of change in long-term interest-bearing debt and in leverage (debt/EBITDA), noting limitations: if EBITDA ≤ 0 or missing, state that debt/EBITDA is not meaningful or constrained.
    - End with a definitive categorical judgment: “Solvency: Strong/Adequate/Weak; Capital quality: Strong/Adequate/Weak.”

    Materiality filter (apply before writing additional drivers beyond the anchors, do not make reference to the filter in the output and do not mention items that do not pass the filter):
    - Parameter: TOP_N = 3 (configurable).
    1) Compute year-over-year (YoY) changes for all available solvency-relevant items (e.g., equity/risk-bearing capital components, total assets, long-term debt, short-term debt if provided, intercompany receivables/debts, intangible assets).
    2) Set the anchor outcome as the change in Risk-bearing capital / Total assets (primary) and the change in debt/EBITDA (secondary, if meaningful).
    3) Rank non-anchor items by absolute YoY change in their contribution to the anchor outcome(s), prioritizing capital adequacy effects over presentation reclassifications.
    4) Select candidates as the TOP_N absolute contributors.
    5) Discuss ONLY candidate items that also pass this threshold test: the item’s absolute YoY change must exceed the absolute YoY change in at least one of: total assets, risk-bearing capital, long-term debt.
    6) If fewer than TOP_N items pass the threshold test, discuss only those that pass.
    Ignore all other items.

    Tie-break rule (for equal absolute YoY changes or ambiguous ranking):
    Apply the following priority order, highest first:
    (1) External capital structure items (equity/risk-bearing capital, interest-bearing debt) over intra-group or non-funding items,
    (2) Interest-bearing debt over non-interest-bearing liabilities,
    (3) Balance-sheet strengthening/weakening drivers (capital injections, debt build/repayment if explicitly shown) over valuation/reclassification lines,
    (4) Items affecting capital quality (intangibles) over neutral items,
    (5) If still tied, choose the item with the larger absolute level in the most recent year.

    Content requirements (one paragraph, no bullet points):
    - Interpret what the movement in capital adequacy and leverage implies for resilience to stress and creditor protection.
    - Discuss intercompany receivables/debts ONLY if material per the filter, stating the structural risk or support implication without speculation.
    - Discuss intangibles ONLY if material per the filter, focusing on capital quality/tangible buffer implications.
    - Mention any anomaly only if material (e.g., sharp leverage increase, equity erosion, meaningful shift to intra-group funding), and link it to solvency risk.
    - Avoid framing asset contractions as 'not debt-funded'; for balance-sheet shrinkage, focus on whether deleveraging, capital depletion, or structural stability is implied by the observed changes.

    Output constraints:
    - Single paragraph only.
    - Use readable number formats when numbers are necessary (k/mln/bln) and prefix currency code (e.g., EUR 100k or EUR 152mln).
    - Avoid long year-by-year numeric strings; if you must quantify, keep to one level + YoY % change OR one delta + YoY %, not multiple comparisons.
    - Do not invent explanations; if the statements do not specify drivers, state the limitation briefly and proceed with judgment based on observed movements.
    - Do not include ratio breakdown sections; only reference the named solvency ratios minimally when essential.
    """,
}

ltu_europe_financial_analysis_prompts_dict_additional = {
    "Profitability (additional insights from the annual report)": """
    **Instructions:**  
    Analyze and summarize **revenue, COGS, and profit** using the following structure:  

    1. **Introduction**  
    - Briefly summarize the company’s industry, core business model, and key financial metrics (e.g., gross margin, operating margin, net margin trends over 3–5 years).  

    2. **Revenue Analysis**  
    - Key drivers of revenue change (e.g., product lines, volumes, demand, geographic markets, pricing strategies, impact of market price, acquisitions, disposals of group companies), indlucing specific years.  

    3. **Cost of Goods Sold (COGS) Analysis**  
    - Key drivers of COGS change (e.g.,  raw materials, prices, inflation, exchange effects, supply chain), indlucing specific years.

    4. **Profit Analysis**   
    - Analyse the Figures that lead to the result/net profit and highlight the significant changes. 

    5. **Key Takeaways**  
    - Strengths (e.g., revenue growth outpacing COGS rise).  
    - Weaknesses (e.g., shrinking margins due to cost inflation).  
    - Critical risks or opportunities (e.g., dependency on a single revenue stream).  

    Only use consolidated figures. If a specific example is provided, incorporate its details only if relevant data is available; otherwise, omit any mention of the example. Prioritize and base your analysis on the information provided in the notes to the consolidated financial statements, whenever available.
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

    5. **Payment Capacity**
    - Calculate Payment Capacity by using the formular (Net income / profit after tax / comprehensive income / net profit / net loss/result) + interest payments+depreciation+amortization - (Liabilities to banks/5) for all years. 

    **Overall Liquidity / Cash flow Assessment**  
    - Highlight interconnections between components (e.g., OCF funding investments vs. debt dependency).  
    - Identify strengths (e.g. strong cash conversion cycle, conservative leverage, diversified funding sources).
    - Identify risks or red flags (e.g., Negative OCF, shrinking cash reserves, rising debt/EBITDA).  
    - Conclude with an overall liquidity risk assessment and recommendations to strengthen cash resilience (e.g., optimizing working capital, refinancing strategies).  

    Only use consolidated figures. If a specific example is provided, incorporate its details only if relevant data is available; otherwise, omit any mention of the example. Prioritize and base your analysis on the information provided in the notes to the consolidated financial statements, whenever available.
    """,
    "Solvency (additional insights from the annual report)": """
    **Instructions:**  
    Assess the company's long-term solvency and ability to meet its debt obligations. Focus on **capital structure sustainability, debt repayment capacity, and risks to financial stability** indlucing specific years and using the following structure:  

    1. **Instruction**  
    Briefly summarize the company's industry (e.g., capital-intensive vs. asset-light), business model, and key solvency metrics (e.g., debt-to-equity ratio, interest coverage ratio, debt-to-EBITDA) over 3-5 years.  

    2. **Debt Load Analysis**:
    - **Debt-to-Equity Ratio** Is the company becoming overleveraged? Compare to industry peers.  
    - **Debt-to-EBITDA** How many years of earnings are needed to repay debt? A ratio >4x often signals risk.  

    3. **Cash Flow Adequacy**  
    - **Free Cash Flow to Debt (FCF/Debt):** Can free cash flow reduce debt?  

    4. **External & Strategic Factors**  
    - **Industry Risks** Are there any industry risk. 
    - **Management Strategy** Summarize Management Strategy.
    - Dividend policies: Are payouts draining cash needed for debt repayment?  

    5. **Synthesis:**  
    - **Sustainability of Capital Structure**  
        - Is debt growth outpacing earnings or cash flow?  
        - Can the company generate sufficient EBITDA to deleverage?  
    - **Red Flags vs. Strengths**  
        - Red flags: Declining interest coverage, shrinking equity cushion, covenant breaches.  
        - Strengths: Long debt maturities, strong FCF generation, conservative leverage ratios.  

    Only use consolidated figures. If a specific example is provided, incorporate its details only if relevant data is available; otherwise, omit any mention of the example. Prioritize and base your analysis on the information provided in the notes to the consolidated financial statements, whenever available.
    """,
}
