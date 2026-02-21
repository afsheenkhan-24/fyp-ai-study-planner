import streamlit as st
from utils.supabase_client import supabase

st.title("Tasks")

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

def get_task(student_id):
    response = supabase.table("Task").select("title", "description", "deadline", "priority","status", "estimated_time").eq("student_id", student_id).execute()
    return response.data

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

with st.container():
    tasks = get_task(st.session_state.student_id)
    st.dataframe(tasks)
    add_task_form()
    


