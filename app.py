import streamlit as st
from utils.supabase_client import supabase

pg = st.navigation([
    st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True),
    st.Page("pages/planner.py", title="Planner", icon=":material/book:", default=False),
    st.Page("pages/task.py", title="Tasks", icon=":material/assignment:", default=False),
    st.Page("pages/calendar.py", title="Calendar", icon=":material/calendar_month:", default=False)
])
pg.run()