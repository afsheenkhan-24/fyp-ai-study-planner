import streamlit as st
from datetime import date, datetime, timedelta
from utils.supabase_client import supabase

st.title("Calendar")

# ---- Data layer ----

def get_tasks(student_id: int):
    response = (
        supabase
        .table("Task")
        .select(
            "task_id, title, description, deadline, priority, status, "
            "estimated_time, assignment_id"
        )
        .eq("student_id", student_id)
        .execute()
    )
    return response.data or []


def parse_deadline(d):
    try:
        return datetime.fromisoformat(d).date()
    except Exception:
        return None


# ---- Main layout ----

student_id = st.session_state.get("student_id", 1)
tasks = get_tasks(student_id)

if not tasks:
    st.info("No tasks yet. Generate tasks from your assignments first.")
    st.stop()

today = date.today()

# Filter upcoming tasks only
upcoming_tasks = []
for t in tasks:
    d = parse_deadline(t.get("deadline"))
    if not d:
        continue
    if d >= today:
        upcoming_tasks.append((d, t))

if not upcoming_tasks:
    st.info("No upcoming tasks. You are currently up to date.")
    st.stop()

st.subheader("Select summary range")

view_type = st.radio(
    "Summary type",
    options=["Weekly (next 7 days)", "Monthly (next 30 days)"],
    horizontal=True,
)

if view_type.startswith("Weekly"):
    end_date = today + timedelta(days=7)
else:
    end_date = today + timedelta(days=30)

st.caption(f"Showing tasks from {today.isoformat()} to {end_date.isoformat()}.")

# Group by date within range
grouped = {}
for d, t in upcoming_tasks:
    if d > end_date:
        continue
    grouped.setdefault(d, []).append(t)

# ---- Summary view ----

if not grouped:
    st.info("No upcoming tasks in the selected range.")
else:
    for d in sorted(grouped.keys()):
        with st.expander(f"{d.isoformat()} – {len(grouped[d])} task(s)"):
            for t in grouped[d]:
                st.markdown(f"- **{t['title']}** ({t['status']}, priority {t['priority']}, due {t['deadline']})")

# ---- Export to CSV ----

st.markdown("---")
st.subheader("Export upcoming tasks")

export_rows = []
for d in sorted(grouped.keys()):
    for t in grouped[d]:
        export_rows.append({
            "date": d.isoformat(),
            "title": t["title"],
            "description": t.get("description") or "",
            "deadline": t["deadline"],
            "priority": t["priority"],
            "status": t["status"],
            "estimated_time": t.get("estimated_time", ""),
        })

if not export_rows:
    st.caption("Nothing to export for the selected range.")
else:
    import pandas as pd

    df = pd.DataFrame(export_rows)
    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download summary as CSV",
        data=csv_data,
        file_name="study_planner_summary.csv",
        mime="text/csv",
        use_container_width=True,
    )