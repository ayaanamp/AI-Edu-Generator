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

/* Buttons */
.stButton > button {
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

/* File Upload */
[data-testid="stFileUploader"] {
    background-color: #111827;
    border-radius: 16px;
    border: 1px solid #1f2937;
    padding: 1rem;
}

/* Expanders */
.streamlit-expanderHeader {
    background-color: #111827;
    border-radius: 10px;
}

/* Radio Buttons */
div[role="radiogroup"] {
    background-color: #111827;
    padding: 10px;
    border-radius: 12px;
}

</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

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
    filename_lower = filename.lower()
    text_lower = pdf_text.lower()
    
    # 1. Clean the PDF lines, skipping watermarks, pure headers, and Table of Contents entries
    lines = pdf_text.split('\n')
    filtered_sentences = []
    
    junk_patterns = [
        r"(?i)downloaded\s+from",
        r"(?i)ncertbooks",
        r"(?i)ncert",
        r"(?i)not\s+to\s+be\s+republished",
        r"(?i)www\.",
        r"(?i)http",
        r"(?i)\.com",
        r"(?i)page\s+\d+",
        r"(?i)class\s+\d+",
        r"(?i)chapter\s+\d+",
        r"(?i)syllabus",
        r"^\s*[0-9\s\-\.\/]+\s*$"
    ]
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        # Skip if matching junk watermark patterns
        if any(re.search(pat, line_stripped) for pat in junk_patterns):
            continue
        # Skip potential Table of Contents lines (containing dot leader chains like "....." or very short sections)
        if "...." in line_stripped or ". . ." in line_stripped:
            continue
        # Skip potential chapter and toc title lines starting with numbers and of short length
        if re.match(r"^\d+", line_stripped) and len(line_stripped.split()) < 10:
            continue
        # Skip headers / lines not ending with standard sentence terminators unless they are long
        if len(line_stripped) < 70 and not line_stripped.endswith(('.', '!', '?')):
            continue
            
        # Clean extra spacing and merge into raw candidate lists
        s_clean = re.sub(r'\s+', ' ', line_stripped).strip()
        if len(s_clean) >= 35:
            filtered_sentences.append(s_clean)

    # De-duplicate
    seen = set()
    unique_sentences = []
    for s in filtered_sentences:
        s_lower = s.lower()
        if s_lower not in seen:
            seen.add(s_lower)
            if len(s) > 300:
                unique_sentences.append(s[:297] + "...")
            else:
                unique_sentences.append(s)

    # 2. Determine thematic domain
    is_physics = "phys" in filename_lower or "quantum" in filename_lower or "mechanic" in filename_lower or "phys" in text_lower or "quantum" in text_lower
    is_bio_chem = "chem" in filename_lower or "bio" in filename_lower or "dna" in filename_lower or "cell" in filename_lower or "chem" in text_lower or "bio" in text_lower or "cell" in text_lower
    is_cs = "comp" in filename_lower or "code" in filename_lower or "program" in filename_lower or "typescript" in filename_lower or "web" in filename_lower or "vite" in text_lower or "react" in text_lower or "code" in text_lower

    # Choose themed fallback pool
    if is_physics:
        default_cards = [
            "Wave-Particle Duality states that every quantum entity may be described as either a particle or a wave physical construct.",
            "Heisenberg's Uncertainty Principle asserts a fundamental limit to the precision with which position and momentum can be known simultaneously.",
            "Schrödinger's Equation is a linear partial differential equation that governs the wave function of a quantum system.",
            "Quantum Entanglement is a phenomenon where physical particles remain interconnected, such that actions on one instantly affect the other.",
            "Planck's Constant relates the energy of a photon to its electromagnetic frequency, serving as a fundamental constant in quantum mechanics.",
            "Superposition is the ability of a quantum physical system to be in multiple states simultaneously until a measurement collapses it.",
            "The Photoelectric Effect is the emission of electrons when electromagnetic radiation (such as light) hits a material surface.",
            "The Copenhagen Interpretation suggests that physical systems do not have definite physical properties prior to being measured.",
            "Quantum Tunneling is a quantum mechanical phenomenon where a particle transition occurs directly through a potential energy barrier.",
            "Blackbody Radiation refers to the stable spectrum of light emitted by an idealized opaque object in thermal equilibrium.",
            "The Zeeman Effect is the splitting of a spectral line into several distinct components in the presence of a static magnetic field.",
            "De Broglie Wave theory proposes that all moving matter exhibits wave-like characteristics, relating momentum to wavelength."
        ]
    elif is_bio_chem:
        default_cards = [
            "Mitochondria are double-membraned cellular organelles responsible for generating most of the chemical energy (ATP) needed by the cell.",
            "Photosynthesis is the metabolic cellular process by which green plants utilize sunlight to synthesize nutrients from carbon dioxide and water.",
            "DNA (Deoxyribonucleic Acid) is a double-helix molecule that carries the genetic instructions used in the growth and reproduction of all organisms.",
            "Enzymes are protein macromolecules that act as highly selective catalysts, accelerating chemical reactions within biological systems.",
            "Mitosis is the segment of the cell cycle where replicated chromosomes are separated into two new nuclei, leading to identical cells.",
            "Active Transport is the movement of ions or molecules across a cell membrane into a region of higher concentration, requiring ATP energy.",
            "Homeostasis is the state of steady internal physical and chemical conditions maintained in active biological systems.",
            "Ribosomes are specialized molecular machines that serve as the site of biological protein synthesis, translating mRNA lines.",
            "The Golgi Apparatus is a cellular organelle that packages and sorts proteins for secretion, playing a key role in the endomembrane system.",
            "Cellular Respiration is a set of metabolic reactions that convert biochemical energy from nutrients into adenosine triphosphate.",
            "Transcription is the first step of gene expression, where a particular segment of DNA is copied into RNA by the enzyme RNA polymerase.",
            "Ecosystem Ecology studies the flow of energy and organic matter through living organisms and surrounding non-living environments."
        ]
    elif is_cs:
        default_cards = [
            "TypeScript is a strongly typed superset of JavaScript that compiles down to highly compatible browser script.",
            "Vite serves workspace code with native ES module structures, ensuring near-instant hot reloads during client side testing.",
            "React relies on a Virtual DOM structure to perform high-efficiency responsive rendering, bypassing slower browser DOM actions.",
            "Full-Stack Web Servers secure confidential secrets, like Gemini API keys, in server-side memory away from browser inspect tools.",
            "Streamlit is a lightweight open-source Python framework that serves interactive data dashboards with minimal front-end coding.",
            "Git Branches allow academic or engineering collaborators to build features independently and merge safely into the main code tree.",
            "Relational Databases organize structured tables using primary and foreign keys, supporting standard SQL query structures.",
            "Caching is the process of storing copies of files or data streams in temporary storage locations for faster request resolutions.",
            "REST APIs establish standard stateless communication between client apps and backend servers using HTTP GET, POST, PUT, and DELETE.",
            "Object-Oriented Programming (OOP) organizes software design around data objects rather than functions or logic blocks.",
            "Recursion is a programming technique where a method calls itself to solve smaller sub-instances of the same problem.",
            "Computational Complexity (Big O) characterizes the execution time or space requirements of an algorithm as input scales."
        ]
    else:
        default_cards = [
            "Metacognition is defined as 'thinking about thinking', allowing learners to monitor and adjust their own cognitive strategies.",
            "Active Recall involves testing your memory by actively retrieving information rather than educationally passive re-reading.",
            "Spaced Repetition leverages the psychological spacing effect, reviewing study cards at optimal intervals to halt the forgetting curve.",
            "The Feynman Technique is a mental model where you master a concept by explaining it in simple, jargon-free terms to a child.",
            "Cognitive Load Theory suggests that working memory has a finite capacity, meaning learning materials should minimize unnecessary noise.",
            "Interleaving is a study technique where you mix different topics or practices, improving the brain's ability to distinguish concepts.",
            "Dual Coding theory states that combining visual aids with textual information creates separate cognitive paths, enhancing keycard retrieval.",
            "Sleep plays a critical role in memory consolidation, transferring short-term learning into stable long-term brain synaptic pathways.",
            "Dual-Store Theory suggests that memory begins in the sensory register, is processed in short-term storage, and is moved to long-term memory.",
            "Elaborative Rehearsal is a learning strategy that involves thinking about the meaning of a term rather than just repeating it.",
            "The Testing Effect shows that long-term memory is increased when part of the learning period is devoted to retrieving information.",
            "Self-Explanation is a constructive study technique where learners explain difficult passages out loud to clarify content relationships."
        ]

    # Merge extracted sentences with fallback presets if extracted sentences are too few
    final_sentences = unique_sentences[:]
    if len(final_sentences) < 8:
        needed = 12 - len(final_sentences)
        for i in range(needed):
            final_sentences.append(default_cards[i % len(default_cards)])
            
    # Cap to exactly 12 cards
    final_sentences = final_sentences[:12]
    
    keycards = []
    for i, text in enumerate(final_sentences):
        keycards.append({
            "id": f"local-card-{i+1}",
            "text": text
        })
        
    mcqs = []
    for idx, card in enumerate(keycards):
        text_val = card["text"]
        words = text_val.split()
        subject = " ".join(words[:3]).replace(',', '').replace('.', '') if len(words) > 2 else "This concept theme"
        
        # Position correct answer deterministically based on card index
        correct_ans = idx % 4
        
        # Setup distractors from other sentences in this themed pool
        other_cards = [c["text"] for c in keycards if c["text"] != text_val]
        
        # Deterministic pseudorandom sampler for consistency in fallbacks
        random.seed(42 + idx)
        distractors = random.sample(other_cards, min(len(other_cards), 3)) if len(other_cards) >= 3 else []
        
        # Backup fillers if not enough distractors
        while len(distractors) < 3:
            candidate = default_cards[random.randint(0, len(default_cards) - 1)]
            if candidate != text_val and candidate not in distractors:
                distractors.append(candidate)
                
        options = [""] * 4
        dist_idx = 0
        for o in range(4):
            if o == correct_ans:
                options[o] = text_val
            else:
                options[o] = distractors[dist_idx]
                dist_idx += 1
                
        mcqs.append({
            "id": f"local-mcq-{idx+1}",
            "question": f"Which statement best formalizes the academic description or definition for section '{subject}'?",
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
                        num_pages = len(reader.pages)
                        extracted_pages = []
                        for i, page in enumerate(reader.pages):
                            page_text = page.extract_text() or ""
                            # Skip the first few pages if we have a lot of pages and they contain TOC metadata
                            if num_pages > 5 and i < 4:
                                text_lower = page_text.lower()
                                if "contents" in text_lower or "preface" in text_lower or "index" in text_lower or "table of contents" in text_lower:
                                    continue
                            if page_text.strip():
                                extracted_pages.append(page_text)
                        
                        pdf_text = "\n\n--- Page --- \n\n".join(extracted_pages)
                        # If we skipped too much or ended up empty, fallback to reading all page text
                        if not pdf_text.strip():
                            pdf_text = ""
                            for page in reader.pages:
                                pdf_text += page.extract_text() or ""
                    except Exception as e:
                        st.error(f"Failed parsing PDF stream locally: {e}")
                else:
                    pdf_text = "Standard fallback layout text. Install pypdf to parse active PDF files."
                
                # Verify if we should use Gemini API or Local Engine
                api_key_to_use = api_key_input or os.environ.get("GEMINI_API_KEY", "")
                
                # Try loading Pydantic classes for strict schema validation
                pydantic_available = False
                try:
                    from pydantic import BaseModel, Field
                    from typing import List

                    class KeycardSchema(BaseModel):
                        id: str = Field(description="Concept id like card-1, card-2, etc.")
                        text: str = Field(description="Detailed academic concept definition, fact or study flashcard text")

                    class MCQSchema(BaseModel):
                        id: str = Field(description="MCQ question ID like mcq-1, mcq-2, etc.")
                        question: str = Field(description="Expert structured multiple choice question targeting key concepts")
                        options: List[str] = Field(description="Exactly 4 realistic and contextually distinct options")
                        correctAnswer: int = Field(description="Index inside the options list from 0 to 3 showing correct option")

                    class StudySchema(BaseModel):
                        keycards: List[KeycardSchema]
                        mcqs: List[MCQSchema]

                    pydantic_available = True
                except Exception:
                    pydantic_available = False

                if api_key_to_use and gemini_sdk_available:
                    try:
                        client = genai.Client(api_key=api_key_to_use)
                        prompt = (
                            "Extract 10-15 high-quality, dense keycards (facts/definitions) and "
                            "generate 10-15 multiple-choice questions (MCQs) with 4 options each (correctAnswer index 0-3) based on the text. "
                            "Do NOT use page headers, chapter listing indices, or table of contents lines to formulate facts or questions. "
                            "Focus strictly on core conceptual theories, facts, explanations and definitions."
                        )
                        # Send a beautiful, robust chunk of the pdf content (up to 120,000 characters!)
                        combined_input = f"{prompt}\n\nDocument Text Content:\n{pdf_text[:120000]}"
                        
                        config_args = {
                            "response_mime_type": "application/json"
                        }
                        if pydantic_available:
                            config_args["response_schema"] = StudySchema

                        response = client.models.generate_content(
                            model="gemini-3.5-flash",
                            contents=combined_input,
                            config=types.GenerateContentConfig(**config_args)
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
