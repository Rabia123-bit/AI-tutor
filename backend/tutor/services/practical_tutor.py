import os
from typing import Any, Dict
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a Business Intelligence tutor analyzing retail business data.

Your task is to explain practical BI results in a clear, complete, topic-aware educational style.

Write the response using exactly these sections and finish all sections completely:

1. Summary
2. Business Meaning
3. Topic-Based Interpretation
4. Recommended Dashboard or Analysis Output
5. Next Analytical Steps

Rules:
- Keep the answer complete but concise.
- Do not stop midway.
- Do not ask follow-up questions.
- Do not say:
  "If you want"
  "Let me know"
  "I can also"
  "Provide the dataset"
- End cleanly after the final analytical step.
- Adjust explanation depth by difficulty:
  - Beginner: simple language
  - Intermediate: moderate detail
  - Advanced: deeper BI reasoning
"""


def get_max_tokens(difficulty: str) -> int:
    difficulty = (difficulty or "").strip().lower()

    if difficulty == "beginner":
        return 1000
    elif difficulty == "intermediate":
        return 1500
    elif difficulty == "advanced":
        return 1900
    return 1000


def _safe_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _extract_text_from_response(resp: Any) -> str:
    output_text = getattr(resp, "output_text", None)
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    parts = []
    output = getattr(resp, "output", None)

    if output:
        for item in output:
            content = getattr(item, "content", None)
            if content:
                for c in content:
                    text_val = getattr(c, "text", None)

                    if isinstance(text_val, str) and text_val.strip():
                        parts.append(text_val.strip())
                    else:
                        nested_value = getattr(text_val, "value", None) if text_val is not None else None
                        if isinstance(nested_value, str) and nested_value.strip():
                            parts.append(nested_value.strip())

            item_text = getattr(item, "text", None)
            if isinstance(item_text, str) and item_text.strip():
                parts.append(item_text.strip())

    return "\n".join(p for p in parts if p).strip()


def _clean_output(text: str) -> str:
    if not text:
        return ""

    cut_markers = [
        "If you want",
        "If you would like",
        "Let me know",
        "I can also",
        "Provide the dataset",
        "I can help",
    ]

    cleaned = text.strip()

    for marker in cut_markers:
        idx = cleaned.find(marker)
        if idx != -1:
            cleaned = cleaned[:idx].strip()

    lines = [line.rstrip() for line in cleaned.splitlines()]
    final_lines = []
    previous_blank = False

    for line in lines:
        is_blank = not line.strip()
        if is_blank and previous_blank:
            continue
        final_lines.append(line)
        previous_blank = is_blank

    return "\n".join(final_lines).strip()


def _fallback_explanation(result: Dict[str, Any], topic: str, difficulty: str, action_label: str) -> str:
    return f"""1. Summary
- The selected practical analysis was "{action_label}" under the BI topic "{topic}" at {difficulty} level.
- The system computed the result successfully and returned structured business data.

2. Business Meaning
- The computed output represents a business-oriented analytical result from the retail dataset.
- This result helps the learner connect BI concepts to decision-making, KPI tracking, or operational analysis.

3. Topic-Based Interpretation
- For the topic "{topic}", the result should be interpreted in relation to how BI tools organize, analyze, and present business data.
- The output can support understanding of performance measurement, reporting, data analysis, or decision support depending on the selected topic.

4. Recommended Dashboard or Analysis Output
- KPI card for the main value
- Bar chart for category or store comparisons
- Trend line for time-based changes
- Table view for detailed inspection

5. Next Analytical Steps
- Compare this result across another business dimension such as store, region, or category.
- Use the result to identify patterns, exceptions, or possible business actions."""


def explain_practical_result(
    student_question: str,
    result: Dict[str, Any],
    topic: str,
    difficulty: str,
    action_label: str,
) -> str:
    student_question = _safe_text(student_question) or "Explain the result in business terms."
    topic = _safe_text(topic) or "Practical BI"
    difficulty = _safe_text(difficulty) or "Beginner"
    action_label = _safe_text(action_label) or "Practical Analysis"
    result = result or {}

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

Important:
Complete all 5 sections fully and do not stop early.
""".strip()

    try:
        resp = client.responses.create(
            model="gpt-5-mini",
            instructions=SYSTEM_PROMPT,
            input=user_input,
            max_output_tokens=get_max_tokens(difficulty),
        )

        text = _extract_text_from_response(resp)
        text = _clean_output(text)

        if not text or len(text) < 250:
            return _fallback_explanation(result, topic, difficulty, action_label)

        required_sections = [
            "1. Summary",
            "2. Business Meaning",
            "3. Topic-Based Interpretation",
            "4. Recommended Dashboard or Analysis Output",
            "5. Next Analytical Steps",
        ]

        missing = [section for section in required_sections if section not in text]
        if missing:
            text += "\n\n" + _fallback_explanation(result, topic, difficulty, action_label)

        return text

    except Exception as e:
        return f"Practical explanation could not be generated: {str(e)}"
