# backend/tutor/services/theory_tutor.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TOPICS = {
    "Data Warehousing": "Explain data warehousing in BI for retail.",
    "ETL": "Explain ETL (Extract, Transform, Load) in BI for retail.",
    "KPIs": "Explain KPIs in BI for retail.",
    "SQL": "Explain the role of SQL in BI for retail.",
    "Dashboards": "Explain dashboards in BI for retail.",
    "Predictive Analytics": "Explain predictive analytics in BI for retail.",
}

SYSTEM_PROMPT = """
You are a Business Intelligence tutor focused on the retail industry.

IMPORTANT:
- Explain ONLY the topic selected by the student.
- Do NOT include content from other BI topics unless explicitly requested.
- Do NOT ask any follow-up questions.

Structure your answer as follows:
1) Brief definition (1–2 sentences).
2) Step-by-step explanation in simple language.
3) One clear retail example.
4) ONE small practical example relevant ONLY to the selected topic:
   - Data Warehousing: describe a simple star schema (fact + 2 dimensions).
   - ETL: outline a simple ETL pipeline and include 2 data quality checks.
   - KPIs: provide 2–3 KPI formulas and explain interpretation.
   - SQL: provide one short SQL query and explain it.
   - Dashboards: suggest 3–5 visuals and why.
   - Predictive Analytics: target variable + example features + one evaluation metric.

Keep it clear, structured, and COMPLETE.
Be concise: prefer bullet points over long paragraphs or add tables where appropriate.
If space is limited, shorten earlier parts but still finish all sections.
"""

# Increase caps: ETL Intermediate often needs more room
CAP_BY_DIFFICULTY = {
    "Beginner": 900,
    "Intermediate": 1800,
    "Advanced": 2400,
}

# Continuation cap per extra call (keeps costs predictable)
CONTINUATION_CAP = 900
MAX_CONTINUATIONS = 2  # total calls <= 3


def _extract_text(resp) -> str:
    """Robust text extraction across SDK variations."""
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


def _is_truncated(resp, text: str) -> bool:
    """
    Detect truncation using finish/status signals when available + heuristics.
    """
    # SDK-level status
    if getattr(resp, "status", None) in ("incomplete", "length"):
        return True

    # Output item-level status / finish_reason
    for item in (getattr(resp, "output", []) or []):
        status = getattr(item, "status", None) or getattr(item, "finish_reason", None)
        if status in ("incomplete", "length"):
            return True

    # Heuristic: cut mid-thought (common when token capped)
    if not text:
        return False

    last_char = text[-1]
    if last_char in (":", "(", ",") or text.endswith("..."):
        return True

    # Another heuristic: ends without sentence punctuation and last line seems unfinished
    if last_char not in (".", "!", "?", ")", "]", "}", "\"", "'"):
        # if last line is short-ish, it might be cut mid-sentence
        last_line = text.strip().splitlines()[-1].strip()
        if 0 < len(last_line) < 120:
            return True

    return False


def generate_theory_response(topic: str, difficulty: str = "Beginner") -> str:
    topic = (topic or "").strip()
    difficulty = (difficulty or "Beginner").strip()

    if topic not in TOPICS:
        return "Invalid topic selected."

    cap = CAP_BY_DIFFICULTY.get(difficulty, 1400)

    base_input = f"""
Topic: {topic}
Difficulty: {difficulty}

Task:
{TOPICS[topic]}
"""

    # 1) First call
    resp = client.responses.create(
        model="gpt-5-mini",
        instructions=SYSTEM_PROMPT,
        input=base_input,
        max_output_tokens=cap,
    )
    text = _extract_text(resp)
    if not text:
        return "No text returned by the model. Please try again."

    # 2) Continue up to MAX_CONTINUATIONS times if truncated
    continuations_used = 0
    while continuations_used < MAX_CONTINUATIONS and _is_truncated(resp, text):
        continuations_used += 1

        # Ask to finish remaining sections; avoid repeating; keep concise
        continuation_prompt = (
            "Your previous answer was cut off. Continue from exactly where you stopped. "
            "Do NOT repeat earlier content. "
            "Finish any incomplete sections of the required structure and then stop. "
            "Keep it concise.\n\n"
            f"START OF PREVIOUS TEXT:\n{text}\nEND OF PREVIOUS TEXT"
        )

        resp = client.responses.create(
            model="gpt-5-mini",
            instructions=SYSTEM_PROMPT,
            input=continuation_prompt,
            max_output_tokens=CONTINUATION_CAP,
        )
        more = _extract_text(resp)
        if not more:
            break
        text = (text + "\n\n" + more).strip()

    return text