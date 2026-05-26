import os
import re
import json
import streamlit as st

# Set Streamlit Page Layout Config
st.set_page_config(
    page_title="Lumina AI Study Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Tailwind/Styling Injector
st.markdown("""
<style>
    .card-title {
        font-family: 'Times New Roman', serif;
        font-style: italic;
    }
    .stButton>button {
        border-radius: 12px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        border-color: #10b981 !important;
        color: #10b981 !important;
    }
</style>
""", unsafe_allow_name=True)

# Try loading PDF extraction library, provide native text box if library is not accessible
try:
    from pypdf import PdfReader
    pdf_parsing_available = True
except ImportError:
    pdf_parsing_available = False

# Try loading Google GenAI library smoothly
try:
    from google import genai
    from google.genai import types
    gemini_sdk_available = True
except ImportError:
    gemini_sdk_available = False

# --- Helper: Generate Offline Fallback Data ---
def generate_local_fallbacks(pdf_text: str, filename: str):
    # Clean up text and divide into list sentences
    cleaned_text = re.sub(r'\s+', ' ', pdf_text).strip()
    sentences = [s.strip() for s in re.split(r'[.!?]+', cleaned_text) if len(s.strip()) > 25]
    
    keycards = []
    mcqs = []
    
    # Filter sentences with definition or critical phrases
    candidates = [
        s for s in sentences if any(term in s.lower() for term in ["is", "are", "defined", "important", "process", "key", "main"])
    ]
    if not candidates:
        candidates = sentences

    cards_count = min(10, max(6, len(candidates)))
    if cards_count > 0:
        for i in range(cards_count):
            text = candidates[i % len(candidates)]
            keycards.append({
                "id": f"local-card-{i+1}",
                "text": text[:180] + ("..." if len(text) > 180 else "")
            })
            
    # Standard Academic Cards fallback if text was too small
    if len(keycards) < 4:
        default_academic_phrases = [
            "Artificial Intelligence (AI) simulates human cognitive procedures using complex modern computer systems.",
            "TypeScript is a strongly typed superset of JavaScript that compiles down to standard browser script.",
            "Vite serves code with native ES module structures, ensuring near-instant hot reloads during client development.",
            "Streamlit is a powerful open-source Python framework that serves data-driven dashboards with zero front-end coding.",
            "GitHub provides version control systems letting teams collaborate concurrently via branch pull requests and merges.",
            "Secure production server configurations mandate hosting sensitive environment keys separately from client files."
        ]
        for i, text in enumerate(default_academic_phrases):
            keycards.append({
                "id": f"sec-card-{i+1}",
                "text": text
            })

    # Generate synthetic MCQs
    for idx, card in enumerate(keycards):
        words = card["text"].split()
        subject = "This concept"
        if len(words) > 2:
            subject = " ".join(words[:3]).replace(',', '').replace('.', '')
            
        correct_ans = idx % 4
        options = ["Incorrect distractor description A", "Incorrect distractor description B", "Incorrect distractor description C", "Incorrect distractor description D"]
        options[correct_ans] = f"Correct definition matching details: {card['text'][:80]}..."
        
        mcqs.append({
            "id": f"local-mcq-{idx+1}",
            "question": f"Which statement best formalizes the academic theme for the section '{subject}'?",
            "options": options,
            "correctAnswer": correct_ans
        })
        
    return {"keycards": keycards, "mcqs": mcqs}

# --- State Management Initialization ---
if "study_data" not in st.session_state:
    st.session_state.study_data = None
if "current_file" not in st.session_state:
    st.session_state.current_file = None
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

# --- Sidebar UI Layout ---
with st.sidebar:
    st.markdown("### 🎓 Lumina Companion")
    st.markdown("---")
    st.info("💡 **Local Offline Ready:** If your Gemini API Key is missing, the system automatically redirects to our offline synthesis parsing fallback.")
    
    api_key_input = st.text_input(
        "Google Gemini API Key (Optional)",
        value=os.environ.get("GEMINI_API_KEY", ""),
        type="password",
        help="If left blank, Lumina runs smoothly in 100% Offline Local Mode without calling any network integrations!"
    )
    
    st.markdown("---")
    st.markdown("#### 🚀 Deployment References")
    st.markdown("• Run app locally: `streamlit run app.py`  \n• Link to your personal GitHub repo  \n• Deploy to Streamlit Cloud with one click!")

# --- Main App Core Title Panel ---
st.title("🎓 Lumina Study Companion")
st.caption("Active Workspace Protocol & Academic Document Synthesis")

tab_workspace, tab_info = st.tabs(["📊 Workspace HUD", "🛠️ Windows & GitHub Guide"])

with tab_workspace:
    # 1. File Upload section
    uploaded_file = st.file_uploader("Drop any research, notes, or syllabus PDF here", type=["pdf"])
    
    if uploaded_file is not None:
        if st.session_state.current_file != uploaded_file.name:
            st.session_state.current_file = uploaded_file.name
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            
            with st.spinner("Extracting documents text streams to local memory caches..."):
                pdf_text = ""
                if pdf_parsing_available:
                    try:
                        reader = PdfReader(uploaded_file)
                        for page in reader.pages:
                            pdf_text += page.extract_text() or ""
                    except Exception as e:
                        st.error(f"Failed parsing PDF stream locally: {e}")
                else:
                    pdf_text = "Standard fallback layout text. Install pypdf to parse active PDF files."
                
                # Verify if we should use Gemini API or Local Engine
                api_key_to_use = api_key_input or os.environ.get("GEMINI_API_KEY", "")
                
                if api_key_to_use and gemini_sdk_available:
                    try:
                        client = genai.Client(api_key=api_key_to_use)
                        prompt = (
                            "Extract 8-12 distinct keycards (facts/definitions) and "
                            "generate 8-12 MCQs with 4 options each (correctAnswer index 0-3). "
                            "Return raw JSON."
                        )
                        combined_input = f"{prompt}\n\nDocument Text Content:\n{pdf_text[:12000]}"
                        
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=combined_input,
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json",
                            )
                        )
                        parsed_json = json.loads(response.text)
                        st.session_state.study_data = parsed_json
                    except Exception as ex:
                        st.warning(f"Gemini API request error: {ex}. Engaging Local Offline Fallback.")
                        st.session_state.study_data = generate_local_fallbacks(pdf_text, uploaded_file.name)
                else:
                    st.session_state.study_data = generate_local_fallbacks(pdf_text, uploaded_file.name)
                    
        # 2. Render synthesized materials
        if st.session_state.study_data:
            st.success(f"Successfully synthesized document: **{st.session_state.current_file}**")
            
            col_cards, col_quiz = st.columns([1, 1], gap="large")
            
            with col_cards:
                st.subheader("📚 Cognitive Study Keycards")
                cards = st.session_state.study_data.get("keycards", [])
                
                for idx, card in enumerate(cards):
                    with st.expander(f"Key Concept {idx+1}: {card.get('text', '')[:40]}...", expanded=(idx == 0)):
                        st.markdown(f"**Concept Definition:**")
                        st.info(card.get("text", ""))
                        
            with col_quiz:
                st.subheader("📝 Diagnostic MCQ Practice Quiz")
                questions = st.session_state.study_data.get("mcqs", [])
                
                quiz_score = 0
                
                for idx, q in enumerate(questions):
                    st.markdown(f"**Q{idx+1}: {q.get('question')}**")
                    options = q.get("options", ["Option A", "Option B", "Option C", "Option D"])
                    
                    correct_idx = q.get("correctAnswer", 0)
                    
                    # Track selections inside Streamlit session states
                    answer_key = f"q_{idx}"
                    selected_val = st.radio(
                        f"Select answer for Question {idx+1}:",
                        options=options,
                        key=answer_key,
                        label_visibility="collapsed"
                    )
                    
                    selected_idx = options.index(selected_val)
                    st.session_state.quiz_answers[idx] = selected_idx
                    
                    # Highlight corrected/wrong answers if submitted
                    if st.session_state.quiz_submitted:
                        if selected_idx == correct_idx:
                            st.success("Correct!")
                            quiz_score += 1
                        else:
                            st.error(f"Incorret. Correct statement is: {options[correct_idx]}")
                    st.markdown("---")
                    
                if questions:
                    if not st.session_state.quiz_submitted:
                        if st.button("Submit Quiz Answers", help="Click to score your practice evaluation"):
                            st.session_state.quiz_submitted = True
                            st.rerun()
                    else:
                        st.markdown(f"### 🎉 Practice Score: **{quiz_score} / {len(questions)}**")
                        if st.button("Retake Practice Quiz"):
                            st.session_state.quiz_submitted = False
                            st.session_state.quiz_answers = {}
                            st.rerun()
                            
    else:
        st.info("📁 Upload an academic file or study guide PDF in the area above to dynamically extract materials!")

with tab_info:
    st.markdown("""
    ## 🛠️ Step-by-Step Guide for Streamlit & GitHub Deployment

    ### 1. Running Streamlit Locally (On Windows)
    Open your command prompt (`cmd`) in your extracted folder and deploy utilizing:
    ```cmd
    # Install dependencies
    pip install streamlit google-genai pypdf
    
    # Fire up the Streamlit interface
    streamlit run app.py
    ```

    ### 2. Connect Your Folder to a GitHub Repo
    1. Download [GitHub Desktop](https://desktop.github.com/) on your Windows machine and sign in.
    2. Go to **File &rarr; Add Local Repository...** and pick your project root folder (containing `package.json`).
    3. If requested, click **Create Repository**.
    4. Write `feat: initial release` in summary, commit to `main`, and click **Publish Repository** at the header list.

    ### 3. Deploy Python version to Streamlit Community Cloud
    1. Visit [share.streamlit.io](https://share.streamlit.io) and log in using your GitHub account credentials.
    2. Click **New app**.
    3. Select your repository `lumina-ai-study-companion` and set the main file path of your deployment to `app.py`.
    4. Click **Deploy!** Your app is now active for assessors and teachers worldwide to run safely with zero setups!
    """)
