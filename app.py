import streamlit as st
from quiz_generator import generate_quiz

st.title("AI Quiz Generator")

user_input = st.text_area("Enter your topic or text")

if st.button("Generate Quiz"):
    result = generate_quiz(user_input)
    st.write(result)