import re
from typing import Dict, Any, Optional, List

QUIZ_BANK = {
    "Data Warehousing": {
        "Beginner": [
            {
                "q": "What is the primary purpose of a data warehouse?",
                "options": [
                    "To support reporting and analysis",
                    "To process daily retail transactions",
                    "To replace all source systems",
                    "To store only images"
                ],
                "answer_index": 0,
                "explanation": "A data warehouse is mainly built to support analysis, reporting, and business decision-making.",
                "tags": ["purpose", "analysis", "reporting", "warehouse"]
            },
            {
                "q": "Which schema is commonly used in data warehousing?",
                "options": [
                    "Star schema",
                    "Binary schema",
                    "Loop schema",
                    "Flat schema"
                ],
                "answer_index": 0,
                "explanation": "Star schema is commonly used because it organizes fact and dimension tables clearly for BI analysis.",
                "tags": ["star schema", "schema", "dimensions", "facts"]
            },
            {
                "q": "What does a fact table usually store?",
                "options": [
                    "Measures such as sales and quantity",
                    "Only store names",
                    "Only customer addresses",
                    "Only product descriptions"
                ],
                "answer_index": 0,
                "explanation": "Fact tables contain measurable values such as revenue, quantity sold, or cost.",
                "tags": ["fact table", "measures", "sales", "quantity"]
            },
            {
                "q": "Which of the following is most likely a dimension table?",
                "options": [
                    "Store",
                    "Revenue",
                    "Profit",
                    "Discount amount"
                ],
                "answer_index": 0,
                "explanation": "Store is a descriptive business entity used to analyze facts, so it belongs in a dimension table.",
                "tags": ["dimension", "store", "descriptive"]
            },
            {
                "q": "Why would a retailer combine POS and e-commerce data in a warehouse?",
                "options": [
                    "To get one unified view of business performance",
                    "To slow down reporting",
                    "To reduce the number of products sold",
                    "To avoid analysis"
                ],
                "answer_index": 0,
                "explanation": "Combining multiple retail sources creates a consistent and complete view for decision-making.",
                "tags": ["pos", "e-commerce", "integration", "unified view"]
            },
        ],
        "Intermediate": [
            {
                "q": "What is the role of a surrogate key in a data warehouse?",
                "options": [
                    "To uniquely identify dimension records independently of source systems",
                    "To replace dashboards",
                    "To store measures in fact tables",
                    "To remove joins"
                ],
                "answer_index": 0,
                "explanation": "Surrogate keys provide stable warehouse-specific identifiers for dimension records.",
                "tags": ["surrogate key", "dimension", "keys"]
            },
            {
                "q": "Why is a star schema often preferred for BI queries?",
                "options": [
                    "Because it simplifies joins and makes analysis easier",
                    "Because it is more transactional",
                    "Because it removes dimensions",
                    "Because it stores only text"
                ],
                "answer_index": 0,
                "explanation": "Star schema simplifies querying because fact tables connect directly to dimension tables.",
                "tags": ["star schema", "joins", "analysis"]
            },
            {
                "q": "What is the grain of a fact table?",
                "options": [
                    "The level of detail represented by each row",
                    "The total number of rows",
                    "The schema color",
                    "The storage format"
                ],
                "answer_index": 0,
                "explanation": "Grain defines what one row in the fact table represents, such as one sales transaction line.",
                "tags": ["grain", "fact table", "detail"]
            },
            {
                "q": "Which pair best represents dimensions in a retail warehouse?",
                "options": [
                    "Store and Product",
                    "Revenue and Quantity",
                    "Sales and Profit",
                    "Discount and Tax"
                ],
                "answer_index": 0,
                "explanation": "Store and Product are descriptive entities used to analyze measures stored in facts.",
                "tags": ["dimensions", "store", "product"]
            },
            {
                "q": "Why is historical data important in a warehouse?",
                "options": [
                    "It supports trend and time-based analysis",
                    "It increases transaction speed",
                    "It removes the need for ETL",
                    "It replaces dashboards"
                ],
                "answer_index": 0,
                "explanation": "Historical data enables comparisons over time, such as monthly or seasonal performance.",
                "tags": ["historical data", "trends", "time analysis"]
            },
        ],
        "Advanced": [
            {
                "q": "Why are surrogate keys especially useful with slowly changing dimensions?",
                "options": [
                    "They allow multiple historical versions of records",
                    "They remove all dimensions",
                    "They replace source data",
                    "They reduce fact table size to zero"
                ],
                "answer_index": 0,
                "explanation": "Surrogate keys support historical tracking by allowing multiple versions of the same business entity.",
                "tags": ["slowly changing dimensions", "scd", "surrogate key"]
            },
            {
                "q": "What is a conformed dimension?",
                "options": [
                    "A dimension shared consistently across multiple fact tables",
                    "A temporary ETL table",
                    "A fact table without keys",
                    "A dashboard filter"
                ],
                "answer_index": 0,
                "explanation": "Conformed dimensions enable consistent analysis across multiple business processes.",
                "tags": ["conformed dimension", "fact tables", "consistency"]
            },
            {
                "q": "Why is dimensional modeling favored in BI over fully normalized OLTP structures?",
                "options": [
                    "Because it improves analytical usability and query simplicity",
                    "Because it removes all keys",
                    "Because it prevents aggregation",
                    "Because it stores only current data"
                ],
                "answer_index": 0,
                "explanation": "Dimensional models are optimized for analysis and are easier for business users to query.",
                "tags": ["dimensional modeling", "oltp", "analysis"]
            },
            {
                "q": "Which design choice most improves cross-subject analysis in a warehouse?",
                "options": [
                    "Using conformed dimensions",
                    "Removing date dimensions",
                    "Deleting historical data",
                    "Replacing fact tables with spreadsheets"
                ],
                "answer_index": 0,
                "explanation": "Conformed dimensions support analysis across sales, inventory, customers, and other subjects.",
                "tags": ["cross-subject analysis", "conformed dimensions"]
            },
            {
                "q": "What problem occurs if grain is not clearly defined in a fact table?",
                "options": [
                    "Metrics may become inconsistent or misleading",
                    "Charts become colorful",
                    "Dimensions disappear automatically",
                    "ETL no longer requires validation"
                ],
                "answer_index": 0,
                "explanation": "Unclear grain can lead to double counting or incorrect aggregation in BI reports.",
                "tags": ["grain", "metrics", "aggregation"]
            },
        ],
    },

    "ETL": {
        "Beginner": [
            {
                "q": "What does ETL stand for?",
                "options": [
                    "Extract, Transform, Load",
                    "Enter, Transfer, Link",
                    "Evaluate, Test, Learn",
                    "Export, Translate, List"
                ],
                "answer_index": 0,
                "explanation": "ETL stands for Extract, Transform, and Load.",
                "tags": ["etl", "extract", "transform", "load"]
            },
            {
                "q": "What happens in the Extract step?",
                "options": [
                    "Data is collected from source systems",
                    "Data is visualized in dashboards",
                    "Data is permanently deleted",
                    "Data is printed only"
                ],
                "answer_index": 0,
                "explanation": "Extract pulls raw data from source systems such as POS, inventory, or e-commerce databases.",
                "tags": ["extract", "source systems"]
            },
            {
                "q": "What is the main purpose of Transform?",
                "options": [
                    "To clean and standardize data",
                    "To build websites",
                    "To remove all columns",
                    "To create user accounts"
                ],
                "answer_index": 0,
                "explanation": "Transform prepares raw data by cleaning, standardizing, and applying business rules.",
                "tags": ["transform", "cleaning", "standardization"]
            },
            {
                "q": "What happens in the Load step?",
                "options": [
                    "Data is moved into the target system such as a warehouse",
                    "Data is sent to customers",
                    "Data is converted into charts only",
                    "Data is ignored"
                ],
                "answer_index": 0,
                "explanation": "Load places transformed data into the final analytical storage system.",
                "tags": ["load", "warehouse", "target"]
            },
            {
                "q": "Why is ETL important in retail BI?",
                "options": [
                    "It combines data from multiple business sources into consistent form",
                    "It removes all dashboards",
                    "It reduces the number of stores",
                    "It replaces KPIs"
                ],
                "answer_index": 0,
                "explanation": "ETL integrates multiple retail data sources for consistent reporting and analysis.",
                "tags": ["retail", "integration", "sources"]
            },
        ],
        "Intermediate": [
            {
                "q": "Why is a staging area used in ETL?",
                "options": [
                    "To temporarily store raw extracted data before transformation",
                    "To permanently replace the warehouse",
                    "To display final dashboards",
                    "To remove all duplicates automatically"
                ],
                "answer_index": 0,
                "explanation": "A staging area safely stores raw data before cleaning and transformation.",
                "tags": ["staging", "raw data", "etl"]
            },
            {
                "q": "Which is an example of a data quality check in ETL?",
                "options": [
                    "Checking for missing values and duplicates",
                    "Changing all values randomly",
                    "Deleting all product rows",
                    "Converting every field to text"
                ],
                "answer_index": 0,
                "explanation": "Data quality checks commonly include missing-value and duplicate detection.",
                "tags": ["data quality", "duplicates", "missing values"]
            },
            {
                "q": "What is incremental loading?",
                "options": [
                    "Loading only new or changed data",
                    "Reloading the full database every hour",
                    "Skipping the load phase",
                    "Loading only old records"
                ],
                "answer_index": 0,
                "explanation": "Incremental loading improves efficiency by processing only new or modified data.",
                "tags": ["incremental", "loading", "updates"]
            },
            {
                "q": "Why is standardizing SKU formats useful in retail ETL?",
                "options": [
                    "It ensures products can be matched consistently across systems",
                    "It removes the need for dimensions",
                    "It makes analysis slower",
                    "It prevents data loading"
                ],
                "answer_index": 0,
                "explanation": "SKU standardization ensures the same product can be identified consistently.",
                "tags": ["sku", "standardization", "retail"]
            },
            {
                "q": "What is a common ETL output in retail analytics?",
                "options": [
                    "A cleaned sales fact table",
                    "A deleted customer list",
                    "A dashboard image",
                    "A random chart color theme"
                ],
                "answer_index": 0,
                "explanation": "Cleaned fact tables are a common ETL result because they support reliable KPI analysis.",
                "tags": ["fact table", "sales", "etl"]
            },
        ],
        "Advanced": [
            {
                "q": "What is the benefit of Change Data Capture (CDC) in ETL?",
                "options": [
                    "It processes only changed records efficiently",
                    "It replaces dashboards",
                    "It deletes historical data",
                    "It removes transformations"
                ],
                "answer_index": 0,
                "explanation": "CDC helps ETL handle inserts, updates, and deletes without full reprocessing.",
                "tags": ["cdc", "change data capture", "incremental"]
            },
            {
                "q": "Why are quarantine tables useful in ETL design?",
                "options": [
                    "They isolate problematic records without stopping valid processing",
                    "They permanently replace fact tables",
                    "They remove referential integrity",
                    "They speed up charts only"
                ],
                "answer_index": 0,
                "explanation": "Quarantine tables hold invalid records so ETL pipelines can continue with clean data.",
                "tags": ["quarantine", "bad records", "data quality"]
            },
            {
                "q": "What is a high-water mark in incremental ETL?",
                "options": [
                    "A stored value marking the latest successfully processed point",
                    "A chart scale setting",
                    "A table color format",
                    "A surrogate key"
                ],
                "answer_index": 0,
                "explanation": "A high-water mark tracks the last processed timestamp or ID to support safe incremental loads.",
                "tags": ["high-water mark", "incremental", "etl"]
            },
            {
                "q": "Why is referential integrity important during ETL loading?",
                "options": [
                    "It ensures facts correctly link to dimensions",
                    "It removes the need for dimensions",
                    "It eliminates business rules",
                    "It replaces monitoring"
                ],
                "answer_index": 0,
                "explanation": "Referential integrity keeps analytical relationships valid and trustworthy.",
                "tags": ["referential integrity", "dimensions", "facts"]
            },
            {
                "q": "Which ETL practice improves recoverability after failure?",
                "options": [
                    "Checkpointing and retries",
                    "Removing logs",
                    "Skipping validation",
                    "Deleting staging data immediately"
                ],
                "answer_index": 0,
                "explanation": "Checkpointing and retries help ETL pipelines resume safely after interruptions.",
                "tags": ["checkpointing", "retries", "recovery"]
            },
        ],
    },

    "KPIs": {
        "Beginner": [
            {
                "q": "What is a KPI?",
                "options": [
                    "A key performance measure used to track business success",
                    "A database schema",
                    "A chart type",
                    "A product barcode"
                ],
                "answer_index": 0,
                "explanation": "A KPI measures performance against a business objective.",
                "tags": ["kpi", "performance", "measure"]
            },
            {
                "q": "Which of these is a common retail KPI?",
                "options": [
                    "Average Order Value",
                    "Screen brightness",
                    "Keyboard size",
                    "File extension"
                ],
                "answer_index": 0,
                "explanation": "Average Order Value is a common retail KPI used to assess customer spending per order.",
                "tags": ["aov", "average order value", "retail"]
            },
            {
                "q": "What does revenue usually measure?",
                "options": [
                    "Total income generated from sales",
                    "Number of employees only",
                    "Warehouse size",
                    "Database speed"
                ],
                "answer_index": 0,
                "explanation": "Revenue measures the money earned from sales.",
                "tags": ["revenue", "sales"]
            },
            {
                "q": "Why are KPIs useful in BI?",
                "options": [
                    "They help monitor business performance",
                    "They replace all data sources",
                    "They remove dashboards",
                    "They eliminate decision-making"
                ],
                "answer_index": 0,
                "explanation": "KPIs help decision-makers monitor whether the business is meeting goals.",
                "tags": ["monitoring", "business performance", "kpis"]
            },
            {
                "q": "If Average Order Value increases, what might it mean?",
                "options": [
                    "Customers are spending more per order",
                    "The number of stores has decreased",
                    "All products are out of stock",
                    "ETL has stopped"
                ],
                "answer_index": 0,
                "explanation": "A higher AOV means each customer order generates more revenue on average.",
                "tags": ["aov", "spending", "interpretation"]
            },
        ],
        "Intermediate": [
            {
                "q": "How is Average Order Value (AOV) calculated?",
                "options": [
                    "Total revenue divided by number of orders",
                    "Total orders divided by revenue",
                    "Revenue divided by number of stores",
                    "Quantity divided by price"
                ],
                "answer_index": 0,
                "explanation": "AOV = total revenue / number of orders.",
                "tags": ["aov", "formula", "calculation"]
            },
            {
                "q": "Why should KPIs be aligned with business goals?",
                "options": [
                    "So they measure what matters strategically",
                    "So they replace source systems",
                    "So they remove data quality issues",
                    "So they reduce SQL usage"
                ],
                "answer_index": 0,
                "explanation": "KPIs should support the actual business objectives the organization is trying to achieve.",
                "tags": ["alignment", "business goals", "strategy"]
            },
            {
                "q": "Which KPI is useful for monitoring a retail discount strategy?",
                "options": [
                    "Weighted discount rate",
                    "Browser version",
                    "File size",
                    "Warehouse color"
                ],
                "answer_index": 0,
                "explanation": "Discount rate helps assess how heavily promotions are being used.",
                "tags": ["discount", "discount rate", "retail"]
            },
            {
                "q": "What is one risk of using too many KPIs?",
                "options": [
                    "Information overload",
                    "More clarity automatically",
                    "Better strategy instantly",
                    "Perfect decisions"
                ],
                "answer_index": 0,
                "explanation": "Too many KPIs can overwhelm users and reduce focus on what matters most.",
                "tags": ["information overload", "too many kpis"]
            },
            {
                "q": "Which KPI best supports store comparison?",
                "options": [
                    "Revenue per store",
                    "Wallpaper color",
                    "Keyboard count",
                    "Logo size"
                ],
                "answer_index": 0,
                "explanation": "Revenue per store supports direct performance comparison across locations.",
                "tags": ["revenue per store", "store comparison"]
            },
        ],
        "Advanced": [
            {
                "q": "Why is it useful to distinguish leading and lagging KPIs?",
                "options": [
                    "They show future drivers versus past outcomes",
                    "They remove the need for dashboards",
                    "They prevent reporting",
                    "They replace ETL"
                ],
                "answer_index": 0,
                "explanation": "Leading KPIs suggest future results, while lagging KPIs reflect historical outcomes.",
                "tags": ["leading", "lagging", "kpis"]
            },
            {
                "q": "What makes a KPI analytically weak?",
                "options": [
                    "It is ambiguous and lacks business context",
                    "It is clearly defined",
                    "It is tied to decisions",
                    "It is tracked consistently"
                ],
                "answer_index": 0,
                "explanation": "Weak KPIs are hard to interpret and may not support useful decisions.",
                "tags": ["weak kpi", "business context", "ambiguity"]
            },
            {
                "q": "Why should KPI definitions be standardized across regions or stores?",
                "options": [
                    "To enable fair comparison and consistency",
                    "To make performance harder to compare",
                    "To remove dimensions",
                    "To avoid data governance"
                ],
                "answer_index": 0,
                "explanation": "Standardized definitions make KPI comparisons trustworthy and meaningful.",
                "tags": ["standardization", "comparison", "consistency"]
            },
            {
                "q": "What might it mean if revenue rises but AOV falls?",
                "options": [
                    "More orders may be driving growth despite lower spend per order",
                    "No customers are buying",
                    "The warehouse is corrupted",
                    "Dimensions were deleted"
                ],
                "answer_index": 0,
                "explanation": "Revenue can increase if order volume rises enough to offset lower order values.",
                "tags": ["revenue", "aov", "interpretation"]
            },
            {
                "q": "Why should KPI dashboards include comparison targets or time context?",
                "options": [
                    "To make KPI interpretation more meaningful",
                    "To reduce usability",
                    "To hide information",
                    "To replace BI tools"
                ],
                "answer_index": 0,
                "explanation": "KPIs become much more useful when compared to history, targets, or benchmarks.",
                "tags": ["comparison", "benchmark", "time context", "dashboard"]
            },
        ],
    },

    "SQL": {
        "Beginner": [
            {
                "q": "What is SQL mainly used for in BI?",
                "options": [
                    "Querying and analyzing data",
                    "Designing logos",
                    "Editing videos",
                    "Changing fonts"
                ],
                "answer_index": 0,
                "explanation": "SQL is used to retrieve, filter, aggregate, and analyze data.",
                "tags": ["sql", "querying", "analysis"]
            },
            {
                "q": "Which SQL clause is used to filter rows?",
                "options": [
                    "WHERE",
                    "GROUP BY",
                    "ORDER BY",
                    "FROM"
                ],
                "answer_index": 0,
                "explanation": "WHERE filters rows based on conditions.",
                "tags": ["where", "filter"]
            },
            {
                "q": "Which clause groups rows for aggregation?",
                "options": [
                    "GROUP BY",
                    "ORDER BY",
                    "JOIN",
                    "SELECT BY"
                ],
                "answer_index": 0,
                "explanation": "GROUP BY is used when summarizing data with functions like SUM or COUNT.",
                "tags": ["group by", "aggregation"]
            },
            {
                "q": "What does SUM(quantity) do?",
                "options": [
                    "Adds all quantity values together",
                    "Counts rows only",
                    "Sorts the table",
                    "Deletes quantities"
                ],
                "answer_index": 0,
                "explanation": "SUM adds the numeric values in the specified column.",
                "tags": ["sum", "aggregation", "quantity"]
            },
            {
                "q": "In retail BI, SQL can help answer which question?",
                "options": [
                    "Which category generated the highest revenue?",
                    "What color is the dashboard theme?",
                    "Which font is installed?",
                    "How old is the laptop battery?"
                ],
                "answer_index": 0,
                "explanation": "SQL is used to answer analytical business questions from retail data.",
                "tags": ["retail", "revenue", "analysis"]
            },
        ],
        "Intermediate": [
            {
                "q": "Why is GROUP BY useful in retail BI?",
                "options": [
                    "It allows aggregation by store, region, or category",
                    "It deletes rows",
                    "It replaces joins",
                    "It creates dashboards"
                ],
                "answer_index": 0,
                "explanation": "GROUP BY supports summarized analysis across key business dimensions.",
                "tags": ["group by", "store", "region", "category"]
            },
            {
                "q": "What is the purpose of a JOIN in SQL?",
                "options": [
                    "To combine related data from different tables",
                    "To sort only",
                    "To delete duplicates automatically",
                    "To remove columns"
                ],
                "answer_index": 0,
                "explanation": "JOIN connects related tables, such as fact and dimension tables.",
                "tags": ["join", "tables", "dimensions", "facts"]
            },
            {
                "q": "Which SQL query pattern best supports category revenue analysis?",
                "options": [
                    "SUM sales grouped by category",
                    "DELETE FROM sales",
                    "SELECT one random row",
                    "UPDATE all categories"
                ],
                "answer_index": 0,
                "explanation": "Category revenue analysis needs grouped aggregation by category.",
                "tags": ["category", "revenue", "sum", "group by"]
            },
            {
                "q": "Why is ORDER BY useful after aggregation?",
                "options": [
                    "It sorts results such as top-selling categories",
                    "It creates tables",
                    "It removes nulls",
                    "It loads data"
                ],
                "answer_index": 0,
                "explanation": "ORDER BY helps rank and present analytical results clearly.",
                "tags": ["order by", "ranking", "top categories"]
            },
            {
                "q": "What does COUNT(DISTINCT order_id) measure?",
                "options": [
                    "Number of unique orders",
                    "Total quantity sold",
                    "Average price",
                    "Number of stores"
                ],
                "answer_index": 0,
                "explanation": "COUNT DISTINCT counts unique values only.",
                "tags": ["count distinct", "orders"]
            },
        ],
        "Advanced": [
            {
                "q": "Why are window functions useful in BI SQL?",
                "options": [
                    "They allow calculations across related rows without collapsing detail",
                    "They replace all joins",
                    "They delete history",
                    "They prevent aggregation"
                ],
                "answer_index": 0,
                "explanation": "Window functions support ranking, running totals, and comparisons while preserving row detail.",
                "tags": ["window functions", "running total", "ranking"]
            },
            {
                "q": "When is a LEFT JOIN useful in BI?",
                "options": [
                    "When you want all rows from the left table even if there is no match",
                    "When you only want matching rows",
                    "When you want to sort descending",
                    "When you want to delete dimensions"
                ],
                "answer_index": 0,
                "explanation": "LEFT JOIN preserves all left-side rows, useful for missing-match analysis.",
                "tags": ["left join", "missing matches"]
            },
            {
                "q": "Which analytical task can ROW_NUMBER() help with?",
                "options": [
                    "Ranking products within each category",
                    "Deleting duplicates only",
                    "Changing column names",
                    "Creating indexes"
                ],
                "answer_index": 0,
                "explanation": "ROW_NUMBER is commonly used for ranking within partitions such as categories or regions.",
                "tags": ["row_number", "ranking", "category"]
            },
            {
                "q": "Why is NULL handling important in BI SQL?",
                "options": [
                    "Missing values can distort aggregations and logic",
                    "NULLs are always equal to zero",
                    "NULLs replace keys",
                    "NULLs improve chart colors"
                ],
                "answer_index": 0,
                "explanation": "Missing values can affect calculations and must be handled carefully.",
                "tags": ["null", "missing values", "aggregation"]
            },
            {
                "q": "What is a benefit of reusable SQL views in BI?",
                "options": [
                    "They improve consistency and simplify repeated analysis",
                    "They remove source systems",
                    "They replace ETL",
                    "They eliminate dashboards"
                ],
                "answer_index": 0,
                "explanation": "Views standardize logic and make analysis more reusable and maintainable.",
                "tags": ["views", "reusable sql", "consistency"]
            },
        ],
    },

    "Dashboards": {
        "Beginner": [
            {
                "q": "What is a dashboard in BI?",
                "options": [
                    "A visual display of important business information",
                    "A warehouse table",
                    "A programming language",
                    "A barcode"
                ],
                "answer_index": 0,
                "explanation": "Dashboards present important business metrics visually for decision-making.",
                "tags": ["dashboard", "visuals", "business information"]
            },
            {
                "q": "Which chart is best for showing sales trend over time?",
                "options": [
                    "Line chart",
                    "Pie chart",
                    "Gauge",
                    "Tree diagram"
                ],
                "answer_index": 0,
                "explanation": "Line charts are well suited for showing trends over time.",
                "tags": ["line chart", "trend", "time"]
            },
            {
                "q": "What is a KPI card used for?",
                "options": [
                    "Showing a key number clearly",
                    "Joining tables",
                    "Loading data",
                    "Deleting records"
                ],
                "answer_index": 0,
                "explanation": "KPI cards highlight important summary values such as revenue or AOV.",
                "tags": ["kpi card", "kpi", "dashboard"]
            },
            {
                "q": "Why should dashboards avoid too many visuals?",
                "options": [
                    "Because clutter makes them harder to understand",
                    "Because visuals are unnecessary",
                    "Because dashboards should use only text",
                    "Because color is not allowed"
                ],
                "answer_index": 0,
                "explanation": "Too many visuals can overwhelm users and reduce clarity.",
                "tags": ["clutter", "dashboard design", "visuals"]
            },
            {
                "q": "Which chart is useful for comparing store performance?",
                "options": [
                    "Bar chart",
                    "Audio chart",
                    "Wallpaper chart",
                    "Login chart"
                ],
                "answer_index": 0,
                "explanation": "Bar charts are useful for comparing values across categories such as stores.",
                "tags": ["bar chart", "store comparison"]
            },
        ],
        "Intermediate": [
            {
                "q": "Why should dashboard design depend on audience?",
                "options": [
                    "Executives and analysts need different levels of detail",
                    "All users need identical views",
                    "Dashboards should avoid detail entirely",
                    "Audience does not matter"
                ],
                "answer_index": 0,
                "explanation": "Different users need different levels of detail and interaction.",
                "tags": ["audience", "executive", "analyst"]
            },
            {
                "q": "Which visual is suitable for top categories by revenue?",
                "options": [
                    "Bar chart",
                    "Line chart",
                    "Gauge",
                    "Map"
                ],
                "answer_index": 0,
                "explanation": "Bar charts are ideal for comparing ranked category performance.",
                "tags": ["bar chart", "top categories", "revenue"]
            },
            {
                "q": "What is a common dashboard design mistake?",
                "options": [
                    "Using inconsistent scales and too many colors",
                    "Using meaningful labels",
                    "Showing key metrics clearly",
                    "Grouping related visuals"
                ],
                "answer_index": 0,
                "explanation": "Inconsistent scales and excessive colors confuse interpretation.",
                "tags": ["dashboard mistakes", "colors", "scales"]
            },
            {
                "q": "Why are filters useful on dashboards?",
                "options": [
                    "They let users explore subsets like time or region",
                    "They replace ETL",
                    "They remove KPIs",
                    "They prevent analysis"
                ],
                "answer_index": 0,
                "explanation": "Filters help users focus on the dimensions most relevant to their analysis.",
                "tags": ["filters", "time", "region", "dashboard"]
            },
            {
                "q": "Which layout is most useful for a retail dashboard?",
                "options": [
                    "Top KPIs first, then trends and breakdowns",
                    "Random charts in no order",
                    "Only long text paragraphs",
                    "No titles or labels"
                ],
                "answer_index": 0,
                "explanation": "A clear top-down structure improves readability and interpretation.",
                "tags": ["layout", "kpis", "trends", "dashboard"]
            },
        ],
        "Advanced": [
            {
                "q": "Why is visual hierarchy important in dashboard design?",
                "options": [
                    "It guides attention to the most important information first",
                    "It replaces metrics",
                    "It removes filtering",
                    "It stores raw data"
                ],
                "answer_index": 0,
                "explanation": "Visual hierarchy helps users quickly focus on what matters most.",
                "tags": ["visual hierarchy", "dashboard design"]
            },
            {
                "q": "What is the benefit of drill-down capability in a dashboard?",
                "options": [
                    "It allows moving from summary to detail",
                    "It hides all detail permanently",
                    "It removes trends",
                    "It disables interaction"
                ],
                "answer_index": 0,
                "explanation": "Drill-down lets users investigate the reasons behind high-level results.",
                "tags": ["drill-down", "detail", "summary"]
            },
            {
                "q": "Why should dashboard metrics be connected to decisions?",
                "options": [
                    "So the dashboard supports action, not just display",
                    "So it replaces ETL",
                    "So it hides analysis",
                    "So it reduces interactivity"
                ],
                "answer_index": 0,
                "explanation": "Dashboards are most valuable when they inform decisions and actions.",
                "tags": ["decisions", "actionable", "dashboard"]
            },
            {
                "q": "What is a limitation of using too many gauges on a dashboard?",
                "options": [
                    "They often consume space without communicating efficiently",
                    "They always improve accuracy",
                    "They replace line charts",
                    "They remove KPIs"
                ],
                "answer_index": 0,
                "explanation": "Gauges can use space inefficiently compared to more informative chart types.",
                "tags": ["gauges", "dashboard", "space"]
            },
            {
                "q": "What increases trust in dashboard insights?",
                "options": [
                    "Clear metric definitions and consistent calculations",
                    "Changing KPI formulas often",
                    "Removing labels",
                    "Hiding filters"
                ],
                "answer_index": 0,
                "explanation": "Trust increases when users understand how metrics are defined and calculated.",
                "tags": ["trust", "metric definitions", "consistency"]
            },
        ],
    },

    "Predictive Analytics": {
        "Beginner": [
            {
                "q": "What is predictive analytics?",
                "options": [
                    "Using historical data to estimate future outcomes",
                    "Only describing past data",
                    "Deleting records",
                    "Designing dashboards"
                ],
                "answer_index": 0,
                "explanation": "Predictive analytics uses historical patterns to forecast likely future outcomes.",
                "tags": ["predictive analytics", "future", "historical data"]
            },
            {
                "q": "Which is a retail use case for predictive analytics?",
                "options": [
                    "Forecasting product demand",
                    "Changing chart colors",
                    "Deleting stores",
                    "Renaming columns"
                ],
                "answer_index": 0,
                "explanation": "Demand forecasting is a common retail predictive use case.",
                "tags": ["forecasting", "demand", "retail"]
            },
            {
                "q": "What is a target variable?",
                "options": [
                    "The value the model tries to predict",
                    "A dashboard title",
                    "A filter name",
                    "A warehouse key"
                ],
                "answer_index": 0,
                "explanation": "The target variable is the output the model is designed to estimate.",
                "tags": ["target variable", "prediction"]
            },
            {
                "q": "Which is a useful feature for retail demand forecasting?",
                "options": [
                    "Past sales data",
                    "Wallpaper color",
                    "Keyboard layout",
                    "Chart font"
                ],
                "answer_index": 0,
                "explanation": "Historical sales data is a common and useful predictive feature.",
                "tags": ["features", "sales history", "forecasting"]
            },
            {
                "q": "Why is predictive analytics useful in retail?",
                "options": [
                    "It helps improve planning and decision-making",
                    "It eliminates uncertainty completely",
                    "It replaces KPIs",
                    "It removes data quality issues"
                ],
                "answer_index": 0,
                "explanation": "Predictive analytics supports planning by estimating likely future behavior.",
                "tags": ["planning", "decision-making", "retail"]
            },
        ],
        "Intermediate": [
            {
                "q": "Which metric is commonly used for forecasting continuous values like sales?",
                "options": [
                    "RMSE",
                    "AUC",
                    "Precision",
                    "F1-score"
                ],
                "answer_index": 0,
                "explanation": "RMSE is commonly used to evaluate forecast error for continuous targets.",
                "tags": ["rmse", "forecasting", "metrics"]
            },
            {
                "q": "Why is train/test splitting important?",
                "options": [
                    "It evaluates model performance on unseen data",
                    "It makes models perfect",
                    "It removes the need for features",
                    "It replaces ETL"
                ],
                "answer_index": 0,
                "explanation": "Train/test splitting helps assess how well the model generalizes.",
                "tags": ["train test split", "evaluation", "generalization"]
            },
            {
                "q": "Which feature could improve retail demand forecasting?",
                "options": [
                    "Promotion flag",
                    "Browser tab color",
                    "Keyboard count",
                    "Logo shape"
                ],
                "answer_index": 0,
                "explanation": "Promotions often influence sales demand and improve prediction quality.",
                "tags": ["promotion", "features", "forecasting"]
            },
            {
                "q": "What is overfitting?",
                "options": [
                    "When a model learns training data too closely and performs poorly on new data",
                    "When a dashboard has too many filters",
                    "When ETL loads duplicates",
                    "When SQL uses GROUP BY"
                ],
                "answer_index": 0,
                "explanation": "Overfitting reduces a model’s ability to generalize to new data.",
                "tags": ["overfitting", "generalization"]
            },
            {
                "q": "Why might weather be a useful predictive feature in retail?",
                "options": [
                    "It can influence product demand",
                    "It changes SQL syntax",
                    "It replaces warehouse design",
                    "It removes metrics"
                ],
                "answer_index": 0,
                "explanation": "Weather can affect demand for many retail products such as beverages or seasonal goods.",
                "tags": ["weather", "features", "demand"]
            },
        ],
        "Advanced": [
            {
                "q": "Why is feature selection important in predictive analytics?",
                "options": [
                    "It helps improve model relevance and reduce noise",
                    "It replaces evaluation metrics",
                    "It guarantees zero error",
                    "It removes training data"
                ],
                "answer_index": 0,
                "explanation": "Choosing relevant features improves model quality and interpretability.",
                "tags": ["feature selection", "noise", "model quality"]
            },
            {
                "q": "What is concept drift?",
                "options": [
                    "When relationships in the data change over time",
                    "When charts change colors",
                    "When SQL stops running",
                    "When dimensions lose keys"
                ],
                "answer_index": 0,
                "explanation": "Concept drift occurs when the underlying data patterns change, reducing model accuracy.",
                "tags": ["concept drift", "changing patterns"]
            },
            {
                "q": "Why should predictive outputs be connected to BI dashboards?",
                "options": [
                    "To support decisions with forward-looking insight",
                    "To hide predictions",
                    "To reduce usability",
                    "To replace ETL"
                ],
                "answer_index": 0,
                "explanation": "Dashboards become more valuable when they combine historical and forward-looking insights.",
                "tags": ["dashboards", "predictions", "decision-making"]
            },
            {
                "q": "What is a major risk of poor-quality training data?",
                "options": [
                    "Unreliable predictions",
                    "Automatic model improvement",
                    "Faster dashboards",
                    "Smaller tables"
                ],
                "answer_index": 0,
                "explanation": "Poor-quality data weakens predictive model performance.",
                "tags": ["training data", "data quality", "predictions"]
            },
            {
                "q": "Why is MAE sometimes preferred over RMSE?",
                "options": [
                    "It is easier to interpret and less sensitive to large errors",
                    "It only works for classification",
                    "It ignores prediction error",
                    "It replaces the target variable"
                ],
                "answer_index": 0,
                "explanation": "MAE is often easier to explain and is less sensitive to large outliers than RMSE.",
                "tags": ["mae", "rmse", "metrics"]
            },
        ],
    },
}


def _tokenize(text: str) -> List[str]:
    text = text.lower()
    return re.findall(r"[a-zA-Z0-9\-]+", text)


def _score_question(question: Dict[str, Any], tokens: List[str]) -> int:
    tags = [t.lower() for t in question.get("tags", [])]
    q_text = question.get("q", "").lower()
    score = 0

    for token in tokens:
        if token in tags:
            score += 3
        if token in q_text:
            score += 1

    return score


def generate_quiz(topic: str, difficulty: str, student_text: Optional[str] = None) -> Dict[str, Any]:
    if topic not in QUIZ_BANK:
        raise ValueError(f"No quiz available for topic: {topic}")

    if difficulty not in QUIZ_BANK[topic]:
        raise ValueError(f"No quiz available for difficulty: {difficulty}")

    questions = QUIZ_BANK[topic][difficulty][:]

    if student_text:
        tokens = _tokenize(student_text)
        questions.sort(key=lambda q: _score_question(q, tokens), reverse=True)

    selected = questions[:5]

    cleaned = []
    for q in selected:
        cleaned.append({
            "q": q["q"],
            "options": q["options"],
            "answer_index": q["answer_index"],
            "explanation": q["explanation"],
        })

    return {
        "topic": topic,
        "difficulty": difficulty,
        "questions": cleaned
    }