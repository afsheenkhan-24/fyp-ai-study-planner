import streamlit as st
from supabase.client import supabase

def main():
    st.title("AI Study Planner") 

    data = supabase.table("students").select("*").execute() 
    st.write(data)

if __name__ == "__main__":
    main()
