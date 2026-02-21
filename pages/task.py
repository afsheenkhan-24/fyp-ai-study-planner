import streamlit as st
from datetime import date
from utils.supabase_client import supabase

st.title("Tasks")

# ---------- Data layer ----------

def get_task(student_id):
    response = supabase.table("Task").select("task_id","title", "description", "deadline", "priority","status", "estimated_time").eq("student_id", student_id).execute()
    return response.data

def add_task(student_id):
    supabase.table("Task").insert({
        "student_id": student_id,
        "title": st.session_state.name,
        "description": st.session_state.description,
        "deadline": st.session_state.deadline.isoformat(),
        "priority": st.session_state.priority,
        "status": st.session_state.status,
        "estimated_time": st.session_state.estimated_time
    }).execute()

    st.success("Task added successfully!")

# ---------- Add task form ----------

def add_task_form():
    with st.form("add_task_form"):
        st.text_input("Task Name", key="name")
        st.text_area("Task Description", key="description")
        st.date_input("Due Date", key="deadline")
        st.selectbox("Priority", options=["Low", "Medium", "High"], key="priority")
        st.selectbox("Status", options=["To Do", "In Progress", "Completed"], key="status")
        st.text_input("Estimated Time", key="estimated_time")

        submitted = st.form_submit_button("Add Task", type="primary", use_container_width=True)

        if submitted:
            student_id = st.session_state.student_id
            add_task(student_id)

# ---------- Main layout ----------

student_id = st.session_state.student_id
tasks = get_task(student_id)

# Task list cards
st.subheader("All Tasks")
for t in tasks:
    with st.container(border=True):
            # first row: title and status
            c1, c2 = st.columns([3, 1],width="stretch")
            with c1:
                st.markdown(f"**{t['title']}**")
                st.caption(t["description"] or "No description")
            with c2:                
                st.markdown(f"**{t['status']}**")
                st.caption(f"Due: {t['deadline']}")
            
st.markdown("---")
add_task_form()



