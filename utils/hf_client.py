import requests
import streamlit as st
from datetime import date, timedelta, datetime


HF_API_TOKEN = st.secrets["HF_API_TOKEN"]
MODEL_NAME   = "Qwen/Qwen2.5-1.5B-Instruct"  
HF_API_URL   = f"https://api-inference.huggingface.co/models/{MODEL_NAME}/v1/chat/completions"


def format_date(date_str: str) -> str:
    try:
        d = datetime.fromisoformat(date_str).date()
        return d.strftime("%d %b %Y")
    except Exception:
        return date_str


def generate_study_plan(tasks, days_ahead=7):
    if not tasks:
        return "You have no tasks yet. Add some tasks first so I can create a study plan."

    task_lines = []
    for t in tasks:
        raw_deadline  = t.get("deadline", "N/A")
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

    today      = date.today()
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

Do NOT use generic labels like "Day 1" or "Day 2". Always use the real calendar dates above."""

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type":  "application/json",
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful AI study coach."},
            {"role": "user",   "content": prompt},
        ],
        "max_tokens": 1024,
        "temperature": 0.5,
    }

    try:
        resp = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)

        # If the model is loading (cold start), HF returns 503 with an estimated_time field
        if resp.status_code == 503:
            data = resp.json()
            wait = data.get("estimated_time", "unknown")
            return f"Model is loading on Hugging Face servers (estimated wait: {wait}s). Please retry in a moment."

        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()

    except requests.exceptions.HTTPError as e:
        return f"HTTP error from Hugging Face API: {e} — {resp.text}"
    except Exception as e:
        return f"Error talking to Hugging Face API: {e}"