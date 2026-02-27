import streamlit as st
from datetime import date
from utils.supabase_client import supabase

st.title("Tasks")

# ---------- Data layer ----------

def get_task(student_id):
    response = (
        supabase
        .table("Task")
        .select("task_id","title", "description", "deadline", "priority","status", "estimated_time")
        .eq("student_id", student_id)
        .execute()
    )
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

def update_task(student_id, task_id):
    supabase.table("Task").update({
        "title": st.session_state.update_name,
        "description": st.session_state.update_description,
        "deadline": st.session_state.update_deadline.isoformat(),
        "priority": st.session_state.update_priority,
        "status": st.session_state.update_status,
        "estimated_time": st.session_state.update_estimated_time
    }).eq("student_id", student_id).eq("task_id", task_id).execute()
    st.success("Task updated successfully!")

def delete_task(student_id, task_id):
    supabase.table("Task").delete() \
        .eq("student_id", student_id) \
        .eq("task_id", task_id) \
        .execute()
    st.success("Task deleted successfully!")

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
            st.rerun()

# ---------- Update Task Dialog ----------

@st.dialog(title="Update Task") 
def update_task_dialog(task):
    with st.form("update_task_form"):
        st.text_input("Task Name", value=task["title"], key="update_name")
        st.text_area("Task Description", value=task["description"], key="update_description")
        st.date_input("Due Date", value=date.fromisoformat(task["deadline"]), key="update_deadline")
        st.selectbox(
            "Priority",
            options=["Low", "Medium", "High"],
            index=["Low", "Medium", "High"].index(task["priority"]),
            key="update_priority",
        )
        st.selectbox(
            "Status",
            options=["To Do", "In Progress", "Completed"],
            index=["To Do", "In Progress", "Completed"].index(task["status"]),
            key="update_status",
        )
        st.text_input("Estimated Time", value=task["estimated_time"], key="update_estimated_time")

        c1, c2 = st.columns(2)
        with c1:
            submitted = st.form_submit_button("Update Task", type="primary", use_container_width=True)
        with c2:
            cancel = st.form_submit_button("Cancel", use_container_width=True)

        if submitted:
            student_id = st.session_state.student_id
            update_task(student_id, task["task_id"])
            st.rerun() 

        if cancel:
            st.rerun() 

# ---------- Main layout ----------

student_id = st.session_state.student_id
tasks = get_task(student_id)

st.subheader("All Tasks")
if not tasks:
    st.info("No tasks yet. Add your first task below.")
else:
    for t in tasks:
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 1.5, 1], width="stretch")
            with c1:
                st.markdown(f"**{t['title']}**")
                st.caption(t["description"] or "No description")
                st.caption(f"Estimated: {t['estimated_time'] or 'N/A'}")
            with c2:
                st.markdown(f"**{t['status']}**")
                st.caption(f"Due: {t['deadline']}")
                st.caption(f"Priority: {t['priority']}")
            with c3:
                if st.button("Edit", key=f"edit_{t['task_id']}", use_container_width=True):
                    update_task_dialog(t)   
                if st.button("Delete", key=f"delete_{t['task_id']}", type="secondary", use_container_width=True):
                    delete_task(student_id, t["task_id"])
                    st.rerun()

st.markdown("---")
st.subheader("Add New Task")
add_task_form()
