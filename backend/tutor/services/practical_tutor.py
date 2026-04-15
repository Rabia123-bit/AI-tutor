import os
from typing import Dict, Any
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a Business Intelligence tutor analyzing retail business data.

Your job is to explain computed results in a topic-aware educational style.

Use exactly this structure:

1. Summary
- State clearly what was analyzed.

2. Business Meaning
- Explain what the result means in business terms.

3. Topic-Based Interpretation
- Relate the result to the selected BI topic.
- For KPI topics: explain the metric meaning and interpretation.
- For SQL topics: explain what the query/result shows.
- For Dashboard topics: explain what visuals should be built and why.
- For ETL topics: explain what the result means for data quality or transformation.
- For Data Warehousing topics: explain how the result relates to fact/dimension structure.
- For Predictive Analytics topics: explain what the result means for forecasting or trend analysis.

4. Recommended Dashboard or Analysis Output
- Suggest 2 to 4 useful visuals or analytical views.

5. Next Analytical Steps
- Suggest 1 or 2 next steps.

IMPORTANT:
- Adjust depth based on difficulty:
  Beginner = simple language
  Intermediate = moderate detail
  Advanced = deeper BI reasoning
- Do NOT ask follow-up questions.
- Do NOT use phrases like "If you want" or "Let me know".
- If space is limited, shorten earlier parts but still finish all sections.
- End after the analytical recommendations.
"""

def _extract_text(resp) -> str:
    text = getattr(resp, "output_text", None)
    if isinstance(text, str) and text.strip():
        return text.strip()

    parts = []
    output = getattr(resp, "output", []) or []
    for item in output:
        content = getattr(item, "content", []) or []
        for c in content:
            t = getattr(c, "text", None)
            if isinstance(t, str) and t.strip():
                parts.append(t.strip())

    return "\n".join(parts).strip()


def explain_practical_result(
    student_question: str,
    result: Dict[str, Any],
    topic: str,
    difficulty: str,
    action_label: str,
) -> str:
    user_input = f"""
Topic:
{topic}

Difficulty:
{difficulty}

Practical analysis selected:
{action_label}

Student request:
{student_question}

Computed result:
{result}
"""

    resp = client.responses.create(
        model="gpt-5-mini",
        instructions=SYSTEM_PROMPT,
        input=user_input,
        max_output_tokens=1200,
    )

    text = _extract_text(resp) or "No explanation generated."

    cut_markers = [
        "If you want",
        "If you would like",
        "Let me know",
        "Provide the dataset",
    ]

    for marker in cut_markers:
        if marker in text:
            text = text.split(marker)[0].strip()

    return text