#This is entry point for Streamlit app

import streamlit as st

st.title("Ruturaj's Chatbot")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    pg = st.navigation([st.Page("chatbot.py", url_path="/chatbot", default=False)], position="top")
else:
    pg = st.navigation([st.Page("auth.py")])
pg.run()