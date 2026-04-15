import json
from typing import List, Dict, Any
from datetime import date, timedelta, datetime
from groq import Groq
import streamlit as st

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
MODEL_NAME = "llama-3.3-70b-versatile"

client = Groq(api_key=GROQ_API_KEY)


def format_date(date_str: str) -> str:
    try:
        d = datetime.fromisoformat(date_str).date()
        return d.strftime("%d %b %Y")
    except Exception:
        return date_str


def generate_study_plan(tasks: List[Dict[str, Any]], days_ahead: int = 7) -> str:
    if not tasks:
        return "You have no tasks yet. Add some tasks first so I can create a study plan."

    task_lines = []
    for t in tasks:
        raw_deadline = t.get("deadline", "N/A")
        pretty_deadline = format_date(raw_deadline) if raw_deadline != "N/A" else "N/A"
        line = (
            f"- {t.get('title', '(no title)')} "
            f"(due {pretty_deadline}, "
            f"priority {t.get('priority', 'N/A')}, "
            f"status {t.get('status', 'N/A')}, "
            f"estimated {t.get('estimated_time', 'N/A')})"
        )
        task_lines.append(line)

    tasks_text = "\n".join(task_lines)

    today = date.today()
    plan_dates = [today + timedelta(days=i) for i in range(days_ahead)]
    plan_dates_text = "\n".join(
        f"- {d.strftime('%d %b %Y')} ({d.strftime('%a')})" for d in plan_dates
    )

    prompt = f"""You are an AI study coach.
Today's date is {today.strftime('%d %b %Y')}.

The student has the following tasks:
{tasks_text}

Create a clear study plan that:
- uses these specific dates for the next {days_ahead} days (one section per date):
{plan_dates_text}
- for each date, lists which tasks to work on and roughly how many hours,
- focuses on earlier deadlines, aiming to finish tasks a day before the deadline,
- is written as bullet points grouped by the actual date (e.g. "10 Apr 2026 (Fri)").

Do NOT use generic labels like "Day 1" or "Day 2". Always use the real calendar dates above.
"""

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful AI study coach."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=1024,
        )

        content = completion.choices[0].message.content
        if not content:
            return "The model returned an empty response."

        return content.strip()

    except Exception as e:
        return f"Error talking to Groq API: {e}"


def generate_subtasks_with_llm(
    title: str,
    description: str,
    sessions: int = 5,
) -> List[str]:
    """
    Ask the LLM to propose a small list of subtask names for an assignment.
    Returns a list of short labels, length <= sessions.
    """
    if sessions <= 0:
        return []

    prompt = f"""You are an AI study coach helping a student break down one assignment.

Assignment title: "{title}"
Assignment description:
{description or "(no description provided)"}

Create a list of {sessions} short, concrete subtasks that the student can schedule on different days.
Each subtask should be a brief phrase like "Research sources", "Draft introduction", "Edit and proofread".

Return ONLY valid JSON: an array of strings, e.g.
["Research topic", "Plan outline", "Draft first version", "Revise", "Final checks"]"""

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful AI study coach."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_completion_tokens=256,
        )

        content = completion.choices[0].message.content
        if not content:
            return []

        subtasks = json.loads(content)
        if isinstance(subtasks, list):
            subtasks = [str(s).strip() for s in subtasks if str(s).strip()]
            if len(subtasks) > sessions:
                subtasks = subtasks[:sessions]
            return subtasks
        return []
    except Exception:
        return []