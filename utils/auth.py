import streamlit as st
from utils.supabase_client import supabase

st.title("Welcome! Please log in or sign up to continue.")

if "user" not in st.session_state:
    st.session_state.user = None
if "student_id" not in st.session_state:
    st.session_state.student_id = None

tab_login, tab_signup = st.tabs(["Login", "Sign up"])

with tab_login:
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", type="primary", use_container_width=True)

    if submitted:
        if not email or not password:
            st.error("Please enter both email and password.")
        else:
            try:
                res = supabase.auth.sign_in_with_password(
                    {"email": email, "password": password}
                )
                if res.user:
                    st.session_state.user = res.user
                    # Use auth user id as student_id
                    st.session_state.student_id = res.user.id
                    st.success("Logged in successfully.")
                    st.rerun()
                else:
                    st.error("Login failed. Check your credentials.")
            except Exception as e:
                st.error(f"Error during login: {e}")

with tab_signup:
    with st.form("signup_form"):
        email_s = st.text_input("Email", key="signup_email")
        password_s = st.text_input("Password", type="password", key="signup_password")
        submitted_s = st.form_submit_button("Sign up", type="primary", use_container_width=True)

    if submitted_s:
        if not email_s or not password_s:
            st.error("Please enter both email and password.")
        else:
            try:
                res = supabase.auth.sign_up({"email": email_s, "password": password_s})
                if res.user:
                    st.success("Sign up successful. Please confirm your email, then log in.")
                else:
                    st.error("Sign up failed.")
            except Exception as e:
                st.error(f"Error during sign up: {e}")

if st.session_state.user:
    st.info(f"Logged in as {st.session_state.user.email}")
    if st.button("Log out", use_container_width=True):
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
        st.session_state.user = None
        st.session_state.student_id = None
        st.success("Logged out.")
        st.rerun()