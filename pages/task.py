import streamlit as st

st.title("Tasks")

with st.form("add_task_form"):
    st.text_input("Task Name", key="task_name")
    st.text_area("Task Description", key="task_description")
    st.date_input("Due Date", key="due_date")
    st.selectbox("Priority", options=["Low", "Medium", "High"], key="priority")

    submitted = st.form_submit_button("Add Task", type="primary", use_container_width=True)