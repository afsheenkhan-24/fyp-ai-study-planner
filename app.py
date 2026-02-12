import streamlit as st
from utils.supabase_client import supabase

def main():
    st.title("AI Study Planner") 

    data = supabase.table("Student").select("*").execute() 
    st.write(data) 

if __name__ == "__main__":
    main()
