import streamlit as st
from utils.auth import run_auth, sign_out

st.set_page_config(page_title="AI Study Planner", layout="wide")

st.logo(
    "images/logo.png",  
    icon_image="images/logo.png",  
)

if "user" not in st.session_state:
    st.session_state["user"] = None

if "profile" not in st.session_state:
    st.session_state["profile"] = {}

authenticated = run_auth()

if authenticated:
    st.sidebar.success(
        f"Logged in as {st.session_state['profile'].get('full_name') or st.session_state['user'].email}"
    )

    if st.sidebar.button("Sign out", use_container_width=True):
        sign_out()

    pg = st.navigation([
        st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True),
        st.Page("pages/assignment.py", title="Assignments", icon=":material/school:"),
        st.Page("pages/task.py", title="Tasks", icon=":material/assignment:"),
        st.Page("pages/planner.py", title="Planner", icon=":material/book:"),
        st.Page("pages/calendar.py", title="Calendar", icon=":material/calendar_month:"),
        st.Page("pages/profile.py", title="Profile", icon=":material/person:"),
    ])
    pg.run()