import streamlit as st
from streamlit_calendar_input import calendar_input
import datetime

st.title("Calendar")

st.date_input("Select a date")


available_dates = [
    datetime.date(2025, 6, 20),
    datetime.date(2025, 6, 25),
    datetime.date(2025, 7, 2),
]

# Call the calendar input
selected_date = calendar_input(available_dates)

# Display the selected date
if selected_date:
    st.success(f"You selected: {selected_date}")