import streamlit as st
from quiz_generator import generate_quiz
from database import save_data
from audio import text_to_audio
from pdf_reader import read_pdf

st.title("AI Educational Content Generator")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# OR text input
user_input = st.text_area("Or enter your topic/text")

if st.button("Generate Quiz"):

    if uploaded_file is not None:
        text = read_pdf(uploaded_file)

    elif user_input.strip() != "":
        text = user_input

    else:
        st.warning("Upload PDF or enter text")
        st.stop()

    # Generate quiz
    quiz = generate_quiz(text[:2000])  # limit text

    # Save
    save_data(text, quiz)

    # Audio
    audio_file = text_to_audio(quiz)

    # Output
    st.subheader("Quiz")
    st.write(quiz)

    st.subheader("Audio")
    st.audio(audio_file)
