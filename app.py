import streamlit as st
from utils.supabase_client import supabase

pg = st.navigation([
    st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True),
    st.Page("pages/planner.py", title="Planner", icon=":material/book:", default=False)
])
pg.run()