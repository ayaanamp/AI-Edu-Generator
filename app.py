import os
import re
import json
import random
import streamlit as st

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Lumina AI Study Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- CUSTOM CSS ----------------

CUSTOM_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>

/* Hide Streamlit UI */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stToolbar"] {
    display: none;
}

/* App Background */
.stApp {
    background-color: #050816;
    color: white;
}

/* Global Font */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main Container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 100%;
}

/* Main Title */
.main-title {
    font-size: 3.2rem;
    font-weight: 700;
    color: white;
    margin-bottom: 0.3rem;
}

/* Subtitle */
.subtitle {
    color: #94a3b8;
    font-size: 1rem;
    margin-bottom: 2rem;
}

/* File Upload */
[data-testid="stFileUploader"] {
    background-color: #111827;
    border: 1px solid #1f2937;
    border-radius: 16px;
    padding: 1rem;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid #10b981;
    background-color: #111827;
    color: white;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background-color: #10b981;
    color: black;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0b1120;
}

/* Expanders */
.streamlit-expanderHeader {
    background-color: #111827;
    border-radius: 12px;
    color: white;
}

/* Radio Buttons */
div[role="radiogroup"] {
    background-color: #111827;
    padding: 12px;
    border-radius: 12px;
}

/* Success Box */
.stSuccess {
    border-radius: 12px;
}

/* Error Box */
.stError {
    border-radius: 12px;
}

/* Info Box */
.stInfo {
    border-radius: 12px;
}

</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------- PDF SUPPORT ----------------

try:
    from pypdf import PdfReader
    pdf_parsing_available = True
except ImportError:
    pdf_parsing_available = False

# ---------------- GEMINI SUPPORT ----------------

try:
    from google import genai
    from google.genai import types
    gemini_sdk_available = True
except ImportError:
    gemini_sdk_available = False

# ---------------- FALLBACK GENERATOR ----------------

def generate_local_fallbacks(pdf_text, filename):

    sentences = []

    raw_sentences = re.split(r'(?<=[.!?])\s+', pdf_text)

    for s in raw_sentences:
        s = s.strip()

        if len(s) > 40 and len(s) < 400:
            sentences.append(s)

    if len(sentences) < 10:
        sentences.extend([
            "Active Recall improves memory retention through retrieval practice.",
            "Spaced Repetition optimizes long-term memory consolidation.",
            "Machine Learning enables systems to learn patterns from data.",
            "React improves frontend rendering using a virtual DOM.",
            "Streamlit simplifies Python dashboard development.",
            "Quantum mechanics studies matter at atomic scales.",
            "DNA carries hereditary information in biological systems.",
            "Photosynthesis converts light into chemical energy.",
            "Algorithms define computational problem-solving steps.",
            "APIs enable communication between software systems."
        ])

    keycards = []

    for i, text in enumerate(sentences[:10]):
        keycards.append({
            "id": f"card-{i+1}",
            "text": text
        })

    mcqs = []

    for i, card in enumerate(keycards):

        correct = card["text"]

        distractors = random.sample(
            [c["text"] for c in keycards if c["text"] != correct],
            3
        )

        options = distractors + [correct]
        random.shuffle(options)

        mcqs.append({
            "id": f"mcq-{i+1}",
            "question": f"What best describes this concept?",
            "options": options,
            "correctAnswer": options.index(correct)
        })

    return {
        "keycards": keycards,
        "mcqs": mcqs
    }

# ---------------- SESSION STATE ----------------

if "study_data" not in st.session_state:
    st.session_state.study_data = None

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("## 🎓 Lumina Companion")

    st.markdown("---")

    api_key_input = st.text_input(
        "Gemini API Key",
        value=os.environ.get("GEMINI_API_KEY", ""),
        type="password"
    )

    st.markdown("---")

    st.info(
        "Upload PDFs to generate study keycards and MCQ quizzes."
    )

# ---------------- HEADER ----------------

st.markdown(
    '<div class="main-title">🎓 Lumina Study Companion</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI Academic Workspace & Cognitive Study System</div>',
    unsafe_allow_html=True
)

# ---------------- TABS ----------------

tab1, tab2 = st.tabs([
    "📚 Workspace",
    "🛠️ Deployment Guide"
])

# ---------------- WORKSPACE TAB ----------------

with tab1:

    uploaded_file = st.file_uploader(
        "Upload your academic PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        with st.spinner("Analyzing PDF document..."):

            pdf_text = ""

            if pdf_parsing_available:

                try:
                    reader = PdfReader(uploaded_file)

                    for page in reader.pages:
                        page_text = page.extract_text()

                        if page_text:
                            pdf_text += page_text + "\n"

                except Exception as e:
                    st.error(f"PDF parsing failed: {e}")

            else:
                pdf_text = "Fallback study content."

            api_key = api_key_input or os.environ.get("GEMINI_API_KEY", "")

            if api_key and gemini_sdk_available:

                try:

                    client = genai.Client(api_key=api_key)

                    prompt = f'''
                    Generate:
                    1. 10 key study flashcards
                    2. 10 MCQs with 4 options

                    Return valid JSON only.

                    Text:
                    {pdf_text[:50000]}
                    '''

                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=prompt
                    )

                    study_data = json.loads(response.text)

                    st.session_state.study_data = study_data

                except Exception as e:

                    st.warning(f"Gemini failed: {e}")

                    st.session_state.study_data = generate_local_fallbacks(
                        pdf_text,
                        uploaded_file.name
                    )

            else:

                st.session_state.study_data = generate_local_fallbacks(
                    pdf_text,
                    uploaded_file.name
                )

    # ---------------- SHOW RESULTS ----------------

    if st.session_state.study_data:

        st.success("Study materials generated successfully.")

        col1, col2 = st.columns(2)

        # ---------------- KEYCARDS ----------------

        with col1:

            st.subheader("📘 Study Keycards")

            for idx, card in enumerate(
                st.session_state.study_data["keycards"]
            ):

                with st.expander(
                    f"Keycard {idx+1}",
                    expanded=(idx == 0)
                ):

                    st.write(card["text"])

        # ---------------- MCQS ----------------

        with col2:

            st.subheader("📝 MCQ Quiz")

            score = 0

            for idx, mcq in enumerate(
                st.session_state.study_data["mcqs"]
            ):

                st.markdown(f"### Q{idx+1}")

                st.write(mcq["question"])

                answer = st.radio(
                    "Choose answer",
                    mcq["options"],
                    key=f"mcq_{idx}"
                )

                selected_index = mcq["options"].index(answer)

                if st.session_state.quiz_submitted:

                    if selected_index == mcq["correctAnswer"]:
                        st.success("Correct")
                        score += 1
                    else:
                        st.error(
                            f"Correct Answer: {mcq['options'][mcq['correctAnswer']]}"
                        )

                st.markdown("---")

            if not st.session_state.quiz_submitted:

                if st.button("Submit Quiz"):
                    st.session_state.quiz_submitted = True
                    st.rerun()

            else:

                st.markdown(
                    f"## 🎯 Final Score: {score}/{len(st.session_state.study_data['mcqs'])}"
                )

                if st.button("Retake Quiz"):
                    st.session_state.quiz_submitted = False
                    st.rerun()

    else:

        st.info(
            "📁 Upload an academic PDF to begin generating study materials."
        )

# ---------------- GUIDE TAB ----------------

with tab2:

    st.markdown("""
    ## 🚀 Deployment Guide

    ### Run Locally

    ```bash
    pip install streamlit google-genai pypdf
    streamlit run app.py
    ```

    ### Deploy to Streamlit Cloud

    1. Push project to GitHub
    2. Visit Streamlit Cloud
    3. Create New App
    4. Select repository
    5. Select `app.py`
    6. Deploy

    ### Add Gemini API Key

    Streamlit Settings → Secrets

    ```toml
    GEMINI_API_KEY="your_key"
    ```
    """)
