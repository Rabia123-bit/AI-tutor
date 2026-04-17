import os
from typing import Any, Dict
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a Business Intelligence tutor analyzing retail business data.

Your task is to explain practical BI results in a clear, structured, topic-aware way.

Follow this exact structure:

1. Summary
- Clearly state what was analyzed and the main result.

2. Business Meaning
- Explain what the result means in business terms.

3. Topic-Based Interpretation
- Relate the result to the selected BI topic:
  - KPIs: explain metric meaning and business interpretation
  - SQL: explain what the query/result shows
  - Dashboards: explain what dashboard insight or visual design this supports
  - ETL: explain data quality / transformation relevance
  - Data Warehousing: explain fact/dimension or warehouse relevance
  - Predictive Analytics: explain trend/forecasting relevance

4. Recommended Dashboard or Analysis Output
- Suggest 2 to 4 useful visuals or analysis outputs.

5. Next Analytical Steps
- Suggest 1 or 2 next steps.

Important rules:
- Adjust explanation depth based on difficulty:
  - Beginner = simple, easy language
  - Intermediate = moderate detail
  - Advanced = deeper BI reasoning
- Be concise but complete.
- Do NOT ask follow-up questions.
- Do NOT say things like:
  - "If you want"
  - "Let me know"
  - "Provide the dataset"
  - "I can also"
- End cleanly after the final analytical step.
"""


def _safe_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _extract_text_from_response(resp: Any) -> str:
    """
    Extract text safely from OpenAI response objects.
    Supports multiple possible response shapes.
    """
    # Most common
    output_text = getattr(resp, "output_text", None)
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    parts = []

    output = getattr(resp, "output", None)
    if output:
        for item in output:
            # item.content may be a list of content blocks
            content = getattr(item, "content", None)
            if content:
                for c in content:
                    # Some SDK objects expose c.text as string
                    text_val = getattr(c, "text", None)
                    if isinstance(text_val, str) and text_val.strip():
                        parts.append(text_val.strip())
                    else:
                        # Some expose nested text object/value
                        nested_text = getattr(text_val, "value", None) if text_val is not None else None
                        if isinstance(nested_text, str) and nested_text.strip():
                            parts.append(nested_text.strip())

            # Some response items may expose text directly
            item_text = getattr(item, "text", None)
            if isinstance(item_text, str) and item_text.strip():
                parts.append(item_text.strip())

    combined = "\n".join(p for p in parts if p).strip()
    if combined:
        return combined

    # Last fallback: string representation
    fallback = _safe_text(resp)
    return fallback if fallback else ""


def _clean_output(text: str) -> str:
    if not text:
        return ""

    # Remove unwanted trailing assistant phrases
    cut_markers = [
        "If you want",
        "If you would like",
        "Let me know",
        "Provide the dataset",
        "I can also",
        "I can help",
    ]

    cleaned = text.strip()

    for marker in cut_markers:
        idx = cleaned.find(marker)
        if idx != -1:
            cleaned = cleaned[:idx].strip()

    # Remove repeated blank lines
    lines = [line.rstrip() for line in cleaned.splitlines()]
    collapsed = []
    previous_blank = False

    for line in lines:
        is_blank = not line.strip()
        if is_blank and previous_blank:
            continue
        collapsed.append(line)
        previous_blank = is_blank

    return "\n".join(collapsed).strip()


def _format_user_input(
    student_question: str,
    result: Dict[str, Any],
    topic: str,
    difficulty: str,
    action_label: str,
) -> str:
    return f"""
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
""".strip()


def explain_practical_result(
    student_question: str,
    result: Dict[str, Any],
    topic: str,
    difficulty: str,
    action_label: str,
) -> str:
    """
    Generate a robust practical BI explanation from the computed result.
    """

    # Safe defaults
    student_question = _safe_text(student_question) or "Explain the result in business terms."
    topic = _safe_text(topic) or "Practical BI"
    difficulty = _safe_text(difficulty) or "Beginner"
    action_label = _safe_text(action_label) or "Practical Analysis"
    result = result or {}

    user_input = _format_user_input(
        student_question=student_question,
        result=result,
        topic=topic,
        difficulty=difficulty,
        action_label=action_label,
    )

    try:
        resp = client.responses.create(
            model="gpt-5-mini",
            instructions=SYSTEM_PROMPT,
            input=user_input,
            max_output_tokens=1200,
        )

        text = _extract_text_from_response(resp)
        text = _clean_output(text)

        if text:
            return text

    except Exception as e:
        return f"Practical explanation could not be generated: {str(e)}"

    return (
        "Practical explanation could not be generated. "
        "The analysis result was computed successfully, but the explanatory response was empty."
    )
