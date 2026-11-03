ltu_european_annual_report_prompts_list = [
    {
        "title": "ESG and Climate and Environmental Risk Assessment$ESG screening$thermal coal checker",
        "question": """
        Objective
        Using only the provided information, determine whether the client derives more than 5% of its total turnover from thermal coal activities.  

        Scope & Definitions 
        -	Thermal coal activities include thermal coal mining, processing, trading, and electricity generation primarily based on thermal coal.
        -	Total Turnover is defined as the consolidated total operating revenue or turnover for the legal entity that is in the application.

        Decision and Output Rules
        Your output must follow this exact format:
        <Insert one of: "Yes", "No"> (Explanation: <Brief explanation citing the specific data used>)
        Interpretation rules:
        "Yes" indicates the client derives more than 5% of its total turnover from thermal coal.
        "No" indicates the client derives less than or equal to 5% of its total turnover from thermal coal.
        If the given document does not contain any information about whether the company has any thermal coal–related revenue, then the answer must be "No".
        """,
    },
    {
        "title": "ESG and Climate and Environmental Risk Assessment$ESG screening$non-conventionals checker",
        "question": """
        Objective 
        Using only the provided information, determine whether the client has operating revenue specifically related to shale gas or other non conventional fossil natural resources that exceeds 5% (upstream) or 20% (midstream or downstream). 
 
        Scope & Definitions: 
        -	Value-chain stage definitions 
            -	Upstream: exploration, development, extraction, or primary production activities or related assets. 
            -	Midstream: processing, trading, transportation, or storage between production and end-market distribution activities or related assets. 
            -	Downstream: refining, marketing, sales, distribution, or other consumer-facing activity or relates assets. 
        -	Non conventional fossil natural resources: Oil & gas derived from tar sands, hydraulic fracturing and shale extraction: shale rock ('shale gas' or 'tight oil'), oil from bituminous sands ('tar sand' oil or'oil sands'), coal bed methane ('coal seam gas') or retorting ('oil shale'). 
        -	Numerator by value chain stage = operating revenue or turnover explicitly attributable to qualifying nonconventional resources at that value chain stage. 
        -	Denominator = Total Turnover, defined as the consolidated total operating revenue or turnover for the legal entity that is in the application.
        -	Calculate the share for each stage separately: upstream share against the >5% threshold; midstream share against the >20% threshold; downstream share against the >20% threshold. 

        Decision and Output Rules:       
        Your output must follow this exact format:
        <Insert one of: "Yes", "No"> (Explanation: The client is classified as <Upstream / Midstream / Downstream> because <short explanation>, its non conventional operating revenue or turnover above the relevant threshold (>5% for upstream; >20% for midstream/downstream) is <Yes/No> because <Brief explanation citing the specific data used>.)
        """,
    },
]

ltu_european_annual_report_agent_prompts_list = [
    {
        "title": "Business description (include Connected Clients)",
        "question": """
        Provide a **concise, business-focused description of the company**.

        ### Required Content
        **Business Model**  
        In a short paragraph, describe the company's business model, including its position in the value chain, core products and/or services, headquarters location, founding year, and legal entity type. Keep this factual and essential.

        **Distinctive Capabilities**  
        In one short paragraph, explain the company's distinctive capabilities relative to its **three most important competitors**, focusing only on material competitive differentiators.

        **Future Resilience**  
        In a concise paragraph, assess the future resilience of the business model, highlighting the most critical market, competitive, technological, or macroeconomic factors affecting sustainability and earnings stability.

        **Porter's Five Forces**  
        Summarize the Porter Five Forces in a **single compact paragraph**. Address each force in **one sentence only**, identifying the main risk exposure, key mitigating factors, and overall impact (low, medium, or high), integrated into continuous prose.

        **SWOT Analysis**  
        Provide a short paragraph covering strengths, weaknesses, opportunities, and threats. Focus only on the most material internal and external factors. No sub-lists or tables.

        **Key Performance Drivers**  
        In a brief paragraph, explain the key operational and strategic drivers of performance. Do **not** repeat information from earlier sections and do **not** restate KPIs.

        **Key Performance Indicators (KPIs)**  
        In one compact paragraph, list and briefly contextualize the most relevant financial and operational KPIs that directly reflect business performance.

        **Key Stakeholder Relationships and Interconnectedness Risk**  
        In a short paragraph, analyze key stakeholder relationships (major clients and suppliers), assess economic interconnectedness or concentration risk (low, medium, or high), and briefly explain mitigation.
        """,
    },
    {
        "title": "Emerging Risks",
        "question": """
        Provide a **concise, company-specific emerging risk assessment** based **solely on information available in the annual report**, while applying structured analytical judgement.

        ### Required Content
        **Risk Identification**  
        Identify the **five most material emerging risks** specific to the company using only the annual report as input. Where risks are not explicitly stated, derive them **logically from disclosed strategy, growth profile, market positioning, and operating model**, but do not introduce external knowledge.  

        Prioritise **forward-looking and business-relevant risks** (e.g., scaling challenges in fast-growing companies), not just control, audit, or compliance risks mentioned by auditors.  

        Present the risks as **five concise structured bullet points**, where each bullet follows this format:
        - **Risk Name:** [short label]  
        - **Risk:** [clear description of the risk]  
        - **Mitigation (if available):** [only if explicitly disclosed or clearly evidenced; otherwise state "Not explicitly disclosed"]
        Collectively, the risks must cover personnel, country/political/geopolitical exposure, technology, supply and labour constraints, environmental factors, and economic cyclicality. Do not include examples here.

        **Risk Examples and Impact**  
        In a focused paragraph, provide **company-specific examples grounded in the annual report** showing how each of the five risks could materialise. Assess the **business impact** of each (low, medium, or high), ensuring impacts are operational or financial and consistent with the company’s disclosed scale and activities. Do not rely on external assumptions.

        **Mitigating Measures**  
        In one concise paragraph, describe the **primary mitigants explicitly mentioned or clearly evidenced in the annual report** for each risk. If mitigation is not clearly disclosed, state this transparently rather than inferring unsupported measures.

        **Geopolitical and Conflict Exposure**  
        In a single integrated paragraph, analyse the impact of **global conflicts and geopolitical tensions** strictly based on the company’s disclosed geographic footprint, supply chain, and market exposure in the annual report. Address both **short-term disruption** and **potential longer-term implications**, but avoid speculation beyond what can reasonably be inferred from the report.

        ### Important Limitation Disclosure  
        Explicitly acknowledge in one sentence that the assessment is **fully dependent on the annual report**, and therefore may **omit material risks not disclosed or insufficiently detailed**, particularly forward-looking, strategic, or rapidly evolving risks (e.g., scaling risks in high-growth companies).
        """,
    },
    {
        "title": "Management, organization and strategy of the company",
        "question": """
        Provide a **concise, company-specific assessment of management, organization, and strategy**.

        ### Required Content
        Organization  
        Explain how the company is organized from an operating perspective, strictly excluding any geographical segmentation. Describe the operating structure only in terms of business units, product lines, or functional divisions. If no operating structure is disclosed or applicable, explicitly state: “There is no operating structure.”  
        Separately, describe the geographical structure of the company, identifying the regions or countries in which it operates and how activities are distributed across them. If no geographical structure is disclosed or applicable, explicitly state: “There is no geographical structure.”  
        Assess whether the organizational chart is clear and whether its level of complexity is proportionate to the company's business model.

        Legal Structure  
        Describe the company's legal structure, including the type of legal entity, ownership structure, and any material regulatory or compliance factors affecting governance or control. Assess whether the legal and organizational setup supports effective oversight or adds structural risk.

        Management and Internal Control  
        Assess how the company is managed and controlled, including whether the Management Information System (MIS) appears sufficient to steer and monitor the business. Identify the key information or metrics used by management, if disclosed, and assess their adequacy for decision-making and control.

        Strategy and Strategic Execution  
        Describe the company's stated strategy and strategic priorities. Assess whether management appears adequately equipped to execute the strategy, taking into account sector-specific and company-specific challenges.

        Key Management Profiles  
        Provide a factual assessment of the CEO and CFO, including names, ages (if disclosed), titles, tenure, educational background, and relevant professional experience. Clearly indicate any recent or announced changes in the CEO or CFO role.

        Governance and Key-Man Risk  
        Where a dominant shareholder or CEO exists, assess whether countervailing powers are in place and whether key-man risk is adequately mitigated through governance structures or management depth.
        """,
    },
    {
        "title": "ESG and Climate and Environmental Risk Assessment$Climate and Environmental Risk Assessment (CERA)",
        "question": """
        Answer the following questions. Display each question first, followed by a concise, evidence-based answer. Only include information explicitly supported by the provided documents. Do not use bullet points, numbered lists, tables, or structured lists.

        Keep answers short, factual, and focused. Do not speculate, infer, or provide recommendations that are not explicitly supported by the source documents.

        If the documents do not contain relevant information for a question, use the specified fallback response for that question.
        1. What climate and environmental risks are identified? Mention any physical, transition, governmental, or regulatory risks (e.g., wildfire, drought, flooding, extreme weather, high emissions, carbon pricing, environmental regulation).
        If no relevant information is found, respond:
        "No climate and environmental risks identified in the provided documents."

        2. What risk reduction (mitigation and adaptation) measures are identified? Mention any measures, initiatives, or actions taken, such as insurance coverage, decarbonization plans, diversification, resilience programs, sustainability strategies, or environmental management initiatives.
        If no relevant information is found, respond:
        "No climate risk mitigation or adaptation measures identified in the provided documents."

        3. What are the key challenges and risks facing the company? Include climate-related, environmental, market, regulatory, operational, financial, or foreign exchange risks only if explicitly mentioned. Briefly describe any reported impact on sales, revenue, profitability, cash flow, costs, liabilities, reserves, market exposure, currency exposure, or overall financial position.
        If no relevant information is found, respond:
        "No key company challenges, risks, or financial impacts identified in the provided documents."

        4. What key strategies, targets, metrics, innovations, collaborations, or recommendations related to climate risk management, mitigation, or adaptation are identified?
        If no relevant information is found, respond:
        "No climate-related strategies, targets, metrics, innovations, collaborations, or recommendations identified in the provided documents."
        """,
    },
    {
        "title": "ESG and Climate and Environmental Risk Assessment$Climate-related reputational and litigation risks",
        "question": """
        List any known ESG or climate-related reputational or litigation risks facing the company. Include environmental, social, and governance controversies, lawsuits, regulatory investigations, fines, penalties, greenwashing allegations, environmental incidents, or other sustainability-related issues. Describe any actual or potential financial, operational, strategic, or reputational impacts on the business.
        """,
    },
    {
        "title": "Sector outlook",
        "question": """
        Sector Outlook Analysis
        Objective
        Assess the borrower's market position, sector outlook, key sector developments, risks, opportunities, and credit implications over the next three years.

        ============================================================
        ANALYSIS REQUIREMENTS
        ============================================================

        1. Identify Market Position
        Determine:
        •	principal business activities;
        •	relevant sector and subsector;
        •	primary geographic markets;
        •	position within the value chain;
        •	supported competitive position.
        Consider evidence such as:
        •	scale and market presence;
        •	customer base;
        •	geographic reach;
        •	product or service differentiation;
        •	technology capabilities;
        •	customer concentration;
        •	supplier concentration;
        •	recurring or contracted revenue;
        •	barriers to entry.
        If evidence is limited:
        •	provide a qualitative assessment;
        •	explain the basis for the conclusion;
        •	do not infer unsupported market leadership.
        Classify borrower position as:
        •	Strong;
        •	In line;
        •	Weak;
        •	Insufficient evidence.

        2. Assess the Three-Year Sector Outlook
        Evaluate the outlook for the relevant sector and geography over the next three years.
        Consider:
        •	demand trends;
        •	market growth or contraction;
        •	pricing developments;
        •	input-cost developments;
        •	labour availability;
        •	competitive dynamics;
        •	supply-chain developments;
        •	technology changes;
        •	regulatory developments;
        •	industry consolidation;
        •	financing conditions.
        Classify the outlook as:
        •	Favourable;
        •	Stable;
        •	Mixed;
        •	Challenging;
        •	Adverse;
        •	Uncertain.
        Support conclusions with available evidence.
        Avoid unsupported forecasts or false precision.

        3. Identify Key Sector Developments
        Select the three to five sector developments most likely to affect the borrower during the next three years.
        Only include developments with a credible credit impact.
        For each development assess:
        Development
        What is changing?
        Sector Impact
        How is the sector expected to be affected?
        Borrower Transmission
        Through which channel could the borrower be affected?
        Possible channels include:
        •	customer demand;
        •	pricing;
        •	margins;
        •	input costs;
        •	labour costs;
        •	customer credit quality;
        •	supplier stability;
        •	working capital;
        •	investment requirements;
        •	regulation;
        •	technology;
        •	refinancing conditions.
        Borrower Impact
        Potential impact on:
        •	revenue;
        •	profitability;
        •	cash generation;
        •	working capital;
        •	investment requirements;
        •	liquidity;
        •	debt-service capacity.
        Mitigant or Opportunity
        Identify supported borrower characteristics that may reduce risk or create opportunity.
        Do not force mitigants when none are supported.

        4. Assess Sector-Related Risks
        Identify material sector-related risks relevant to the borrower.
        Examples include:
        •	demand weakness;
        •	cost inflation;
        •	labour shortages;
        •	competitive pressure;
        •	supply-chain disruption;
        •	regulatory changes;
        •	technological disruption;
        •	customer concentration;
        •	supplier concentration;
        •	refinancing pressure.
        Only include risks with a credible borrower-specific transmission channel.
        Avoid generic industry commentary.

        5. Assess Sector-Related Opportunities
        Identify material opportunities the borrower appears positioned to capture.
        Examples include:
        •	structural demand growth;
        •	market expansion;
        •	industry consolidation;
        •	technology advantages;
        •	product differentiation;
        •	new customer segments;
        •	favourable regulation;
        •	replacement cycles.
        Do not assume the borrower will benefit simply because the sector is growing.
        Consider:
        •	execution capability;
        •	investment requirements;
        •	funding requirements;
        •	timing.
 
        6. Assess Overall Credit Relevance
        Assess how sector conditions may affect:
        •	revenue stability;
        •	profitability;
        •	cash generation;
        •	working-capital requirements;
        •	investment needs;
        •	liquidity;
        •	debt-service capacity.
        Identify:
        •	the most important external dependency;
        •	the most significant risk;
        •	the most significant opportunity.

        8. Asset and Transaction Relevance
        Only assess where relevant to the transaction.
        Consider whether sector developments could affect:
        •	demand for financed assets;
        •	asset utilisation;
        •	useful life;
        •	technology obsolescence;
        •	residual value;
        •	secondary-market liquidity;
        •	replacement cycles;
        •	recovery environment.
        Do not substitute asset strength for repayment capacity.
        Include only incremental implications not already covered.

        ============================================================
        Materiality Rules
        ============================================================
        Include only developments that may materially affect:
        •	revenue;
        •	margins;
        •	working capital;
        •	cash generation;
        •	investment requirements;
        •	liquidity;
        •	debt-service capacity;
        •	financed assets;
        •	transaction structure.
        Exclude:
        •	generic economic commentary;
        •	unsupported market-share claims;
        •	promotional company language;
        •	speculative developments;
        •	low-materiality news;
        •	duplicated content.

        ============================================================
        FINAL RESPONSE FORMAT
        ============================================================
        Opening Paragraph

        Provide a concise sector-focused overview that summarises:
        • the relevant sector, subsector, and geography;
        • the three-year sector outlook;
        • the key sector drivers, challenges, and opportunities;
        • the principal credit implication arising from sector conditions.
        Include only one brief sentence describing how the borrower is positioned relative to the sector.
        Do not describe the borrower's activities, products, services, business model, history, scale, or operations.

        Key Developments
        Focus primarily on sector developments and their implications for participants in the sector.

        Use the following structure:
        1. [Development]
        [Evidence-based sector trend and expected sector impact.]
        For the borrower, this may affect [borrower-specific transmission and impact].
        [Supported mitigant or opportunity where applicable.]

        2. [Development]
        ...
        Keep discussion of the borrower concise and only where needed to explain transmission channels or credit implications.

        Conclusion
        Provide a sector-focused conclusion summarising:
        • whether sector conditions are supportive, neutral, or challenging;
        • the most important sector risk;
        • the most important sector opportunity;
        • the key external dependency affecting sector performance;
        • forecast alignment assessment where applicable.
        Refer to the borrower only where required to explain whether its positioning is likely to strengthen or weaken its ability to navigate sector conditions.
        Do not repeat a general description of the borrower.

        End exactly with:
        Sector outlook:
        Favourable / Stable / Mixed / Challenging / Adverse / Uncertain

        Borrower position:
        Strong / In line / Weak / Insufficient evidence

        Forecast alignment:
        Supportive / Broadly consistent / Requires review / Not assessed
        """,
    },
]
