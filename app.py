import os
import re
import json
import random
import streamlit as st
import streamlit.components.v1 as components

# Set Streamlit Page Layout Config
st.set_page_config(
    page_title="Lumina AI Study Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Theme and High-Fidelity Styling Injector
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,600;1,400;1,500&family=JetBrains+Mono:wght@400;500;700&display=swap');

    /* Force pitch-black and deep carbon obsidian colors everywhere */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background-color: #050505 !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    
    /* Make the sidebar look like carbon obsidian with neat border */
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div {
        background-color: #090909 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Style headers and main container layout spacing */
    [data-testid="stHeader"] {
        background-color: #050505 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }

    /* Style the tabs to look ultra professional */
    div[data-baseweb="tab-list"] {
        background-color: #0b0b0b !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        padding: 6px !important;
        border-radius: 14px !important;
        gap: 6px !important;
        margin-bottom: 30px !important;
    }
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        color: rgba(255,255,255,0.4) !important;
        border-radius: 10px !important;
        padding: 10px 22px !important;
        border: none !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    button[aria-selected="true"] {
        background-color: #10b981 !important;
        color: #000000 !important;
        box-shadow: 0 0 15px rgba(16,185,129,0.35) !important;
    }

    /* Drag and drop file uploader customization default */
    div[data-testid="stFileUploader"] {
        background-color: rgba(255, 255, 255, 0.01) !important;
        border-radius: 16px !important;
        border: 1px dashed rgba(255, 255, 255, 0.08) !important;
        transition: all 0.3s !important;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: #10b981 !important;
        background-color: rgba(16, 185, 129, 0.02) !important;
    }

    /* Radio button / MCQ styling override as elegant custom card lists */
    div[data-testid="stRadio"] > div {
        gap: 12px !important;
        width: 100% !important;
    }
    div[data-testid="stRadio"] label {
        background-color: #0d0d0d !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        border-radius: 14px !important;
        padding: 16px 20px !important;
        color: rgba(255,255,255,0.75) !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        cursor: pointer !important;
        display: block !important;
        width: 100% !important;
    }
    div[data-testid="stRadio"] label:hover {
        border-color: rgba(16, 185, 129, 0.3) !important;
        background-color: rgba(16, 185, 129, 0.03) !important;
        color: #ffffff !important;
    }
    div[data-testid="stRadio"] label[data-checked="true"] {
        border-color: #10b981 !important;
        background-color: rgba(16, 185, 129, 0.08) !important;
        color: #ffffff !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.05) !important;
    }
    
    /* Standard buttons override */
    .stButton>button {
        background-color: #10b981 !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 24px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        font-size: 11px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    .stButton>button:hover {
        background-color: #059669 !important;
        box-shadow: 0 0 20px rgba(16,185,129,0.45) !important;
        transform: translateY(-1px) !important;
    }

    /* Info, Success, Alerts styling custom match */
    div.stAlert {
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        background-color: #0e0e0e !important;
        padding: 15px 20px !important;
    }

    /* Hide default decoration */
    div.stDecoration {
        display: none !important;
    }
    
    /* Custom container and overlay for Source Acquisition empty state */
    .source-acquisition-container {
        max-width: 650px !important;
        height: 380px !important;
        background-color: #0b0b0b !important;
        border: 1px dashed rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        padding: 40px !important;
        margin: 40px auto !important;
        box-shadow: 0 30px 70px rgba(0, 0, 0, 0.7) !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        position: relative !important;
    }

    .source-acquisition-icon {
        width: 64px !important;
        height: 64px !important;
        background-color: #10b981 !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.3) !important;
        margin-bottom: 24px !important;
        transition: all 0.4s ease !important;
    }

    /* Using parent has hover selectors to highlight source-acquisition-container when uploader is hovered */
    div[data-testid="stVerticalBlock"]:has(div[data-testid="stFileUploader"]:hover) .source-acquisition-container {
        border-color: #10b981 !important;
        box-shadow: 0 0 45px rgba(16, 185, 129, 0.18) !important;
        background-color: #0d0d0d !important;
    }
    div[data-testid="stVerticalBlock"]:has(div[data-testid="stFileUploader"]:hover) .source-acquisition-icon {
        transform: scale(1.05) !important;
        box-shadow: 0 0 35px rgba(16, 185, 129, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# Generate custom head navigation matching the React header
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; padding: 12px 5px; border-bottom: 1px solid rgba(255,255,255,0.06); margin-bottom: 35px; margin-top: -30px;">
    <div style="display: flex; align-items: center; gap: 14px;">
        <div style="width: 38px; height: 38px; background-color: #10b981; border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 20px rgba(16,185,129,0.35);">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="black" stroke-width="2.5" style="width: 20px; height: 20px;">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 18a3.75 3.75 0 00.495-7.467 5.99 5.99 0 00-1.925 3.546 5.974 5.974 0 01-2.133-1A3.75 3.75 0 0012 18z"/>
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zM12.75 6a.75.75 0 00-1.5 0v3.75a.75.75 0 001.5 0V6z"/>
            </svg>
        </div>
        <h1 style="font-size: 22px; font-weight: 600; color: white; margin: 0; font-family: 'Inter', sans-serif; letter-spacing: -0.5px;">
            Lumina<span style="color: #10b981; font-style: italic; font-family: 'Playfair Display', serif; font-weight: 500;">AI</span> Study
        </h1>
    </div>
    <div style="display: flex; align-items: center; gap: 12px;">
        <div style="display: flex; align-items: center; gap: 6px; border: 1px solid rgba(16,185,129,0.25); background-color: rgba(16,185,129,0.06); padding: 5px 12px; border-radius: 30px; box-shadow: 0 0 10px rgba(16,185,129,0.08);">
            <span style="font-size: 11px; line-height: 1;">🏆</span>
            <span style="font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: #10b981; font-weight: 700; font-family: 'Inter', sans-serif;">
                Study Dashboard
            </span>
        </div>
        <div style="width: 32px; height: 32px; background-color: #0f0f0f; border: 1px solid rgba(255,255,255,0.08); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: 'Playfair Display', serif; font-style: italic; font-size: 12px; font-weight: bold; color: rgba(255,255,255,0.6); box-shadow: 0 2px 10px rgba(0,0,0,0.3);">
            AI
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

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
    
    # Pre-select themed fallbacks for backup
    is_physics = "phys" in filename_lower or "quantum" in filename_lower or "mechanic" in filename_lower or "phys" in text_lower or "quantum" in text_lower
    is_bio_chem = "chem" in filename_lower or "bio" in filename_lower or "dna" in filename_lower or "cell" in filename_lower or "chem" in text_lower or "bio" in text_lower or "cell" in text_lower
    is_cs = "comp" in filename_lower or "code" in filename_lower or "program" in filename_lower or "typescript" in filename_lower or "web" in filename_lower or "vite" in text_lower or "react" in text_lower or "code" in text_lower

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

    # --- ADVANCED SENTENCE EXTRACTION FROM RAW TEXT ---
    extracted_sentences = []
    if pdf_text and len(pdf_text.strip()) > 100:
        # Normalize text spacing to merge split lines
        normalized = re.sub(r'\s+', ' ', pdf_text).strip()
        
        # Remove common academic PDF noise
        junk_patterns = [
            r"downloaded\s+from",
            r"ncertbooks",
            r"class\s+\d+",
            r"chapter\s+\d+",
            r"syllabus",
            r"not\s+to\s+be\s+republished",
            r"www\.[a-zA-Z0-9.\-_/]+"
        ]
        for pattern in junk_patterns:
            normalized = re.sub(pattern, "", normalized, flags=re.IGNORECASE)
            
        # Split into sentences using a robust lookbehind that respects standard ending punctuation
        raw_sentences = re.split(r'(?<=[.!?])\s+', normalized)
        
        seen = set()
        for s in raw_sentences:
            s_clean = s.strip()
            # Must meet the requirements of a high-quality educational fact card:
            # - Length between 45 and 250 characters
            # - Starts with an uppercase letter
            # - Ends with punctuation
            # - Has at least 6 words
            # - Does not contain long "dot chains" like TOCs "....."
            if (len(s_clean) >= 45 and len(s_clean) <= 250 and
                s_clean[0].isupper() and
                s_clean[-1] in ('.', '!', '?') and
                len(s_clean.split()) >= 6 and
                "...." not in s_clean and ". . ." not in s_clean):
                
                # Check for other numeric sequences indicating page listings
                if re.match(r'^\s*[0-9\s\-./]+\s*$', s_clean):
                    continue
                    
                s_lower = s_clean.lower()
                if s_lower not in seen:
                    seen.add(s_lower)
                    extracted_sentences.append(s_clean)

    # 2. Build final pool of up to 12 cards
    final_sentences = extracted_sentences[:]
    if len(final_sentences) < 12:
        needed = 12 - len(final_sentences)
        for i in range(needed):
            candidate = default_cards[i % len(default_cards)]
            if candidate not in final_sentences:
                final_sentences.append(candidate)
                
    final_sentences = final_sentences[:12]
    
    # 3. Create Keycards metadata
    keycards = []
    for i, text_val in enumerate(final_sentences):
        keycards.append({
            "id": f"local-card-{i+1}",
            "text": text_val
        })
        
    # 4. Create premium context-aware MCQs with authentic options
    mcqs = []
    for idx, card in enumerate(keycards):
        text_val = card["text"]
        words = text_val.split()
        
        # Extract a premium contextual subject header from the text
        if len(words) > 3:
            subject = " ".join(words[:4]).strip(",.:;()\"' ")
        else:
            subject = "This key concept"
            
        # Place correct answer deterministically inside option slots
        correct_ans = idx % 4
        
        # Use other extracted card facts as natural distractors
        other_choices = [c["text"] for c in keycards if c["text"] != text_val]
        
        # Pull 3 highly educational distractors from our current active card pool
        random.seed(1337 + idx)
        if len(other_choices) >= 3:
            distractors = random.sample(other_choices, 3)
        else:
            distractors = other_choices[:]
            # If we don't have enough other choices, fill from the default pool
            for candidate in default_cards:
                if len(distractors) >= 3:
                    break
                if candidate != text_val and candidate not in distractors:
                    distractors.append(candidate)
                    
        # Mix distractors with correct option
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
            "question": f"Based on the processed study material, which of the following statements offers the most accurate formulation regarding the concept of '{subject}'?",
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

# Helper to find active Google Gemini API key cleanly from multiple places
def get_companion_api_key():
    if "api_key_input" in st.session_state and st.session_state.api_key_input.strip():
        return st.session_state.api_key_input.strip()
    env_val = os.environ.get("GEMINI_API_KEY", "").strip()
    if env_val:
        return env_val
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"].strip()
    except Exception:
        pass
    return ""

# --- Sidebar UI Layout ---
with st.sidebar:
    st.markdown("### 🎓 Companion HUD")
    st.markdown("---")
    st.info("💡 **Local Offline Ready:** If your Gemini API Key is missing, the system automatically redirects to our offline synthesis parsing fallback.")
    
    # Store API Key in session state key directly to prevent loss across reruns
    api_key_input = st.text_input(
        "Google Gemini API Key (Optional)",
        value=get_companion_api_key(),
        type="password",
        key="api_key_input",
        help="If left blank, Lumina runs smoothly in 100% Offline Local Mode without calling any network integrations!"
    )
    
    st.markdown("---")
    st.markdown("#### 🚀 Deployment References")
    st.markdown("• Run app locally: `streamlit run app.py`  \n• Link to your personal GitHub repo  \n• Deploy to Streamlit Cloud with one click!")

# --- Main App Core Title Panel ---
st.markdown("<h4 style='margin-top:0; color: rgba(255,255,255,0.4); font-size:12px; text-transform:uppercase; letter-spacing:2px;'>Active Workspace Protocol & Academic Document Synthesis</h4>", unsafe_allow_html=True)

tab_workspace, tab_info = st.tabs(["📊 Workspace HUD", "🛠️ Windows & GitHub Guide"])

with tab_workspace:
    # Check if a file has been actively registered
    if not st.session_state.get("current_file"):
        # Render the static beautiful card matching React Design with native styling
        st.markdown("""
        <div class="source-acquisition-container" style="max-width: 650px; margin: 30px auto 15px auto; padding: 40px; background-color: #0b0b0b; border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.6); display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative;">
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%;">
                <div class="source-acquisition-icon" style="width: 58px; height: 58px; background-color: #10b981; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 20px rgba(16,185,129,0.3); margin-bottom: 20px;">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="black" stroke-width="2.5" style="width: 24px; height: 24px;">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5"/>
                    </svg>
                </div>
                <h2 style="font-family: 'Playfair Display', serif; font-size: 30px; font-weight: 400; font-style: italic; color: #ffffff; margin-top: 0; margin-bottom: 12px; text-align: center; letter-spacing: -0.5px;">
                    Source Acquisition
                </h2>
                <p style="color: rgba(255, 255, 255, 0.5); font-size: 14px; text-align: center; max-width: 440px; line-height: 1.6; margin: 0 auto; font-family: 'Inter', sans-serif; font-weight: 300;">
                    Upload your PDF document below to initiate high-fidelity extraction, keycards study, and practice quiz generation under extreme hardware acceleration.
                </p>
                <div style="display: flex; align-items: center; width: 100%; margin-top: 30px; padding: 0 20px;">
                    <div style="flex-grow: 1; height: 1px; background: linear-gradient(to right, transparent, rgba(255,255,255,0.08), transparent);"></div>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #10b981; padding: 0 15px; letter-spacing: 3px; font-weight: 700; text-transform: uppercase;">Ready to Deploy</span>
                    <div style="flex-grow: 1; height: 1px; background: linear-gradient(to right, transparent, rgba(255,255,255,0.08), transparent);"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Style the native file uploader elegantly
        st.markdown("""
        <style>
            div[data-testid="stFileUploader"] {
                max-width: 650px !important;
                margin: 0 auto 40px auto !important;
            }
            div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] {
                background-color: #0d0d0d !important;
                border: 1px dashed rgba(16, 185, 129, 0.25) !important;
                border-radius: 14px !important;
                padding: 24px !important;
                transition: all 0.3s ease;
            }
            div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"]:hover {
                border-color: #10b981 !important;
                background-color: rgba(16, 185, 129, 0.03) !important;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        # File is active! Render compact normal style CSS to reset uploader layout beautifully
        st.markdown("""
        <style>
            div[data-testid="stFileUploader"] {
                max-width: 100% !important;
                margin: 0 auto 25px auto !important;
            }
            div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] {
                padding: 14px !important;
                background-color: rgba(255, 255, 255, 0.02) !important;
                border: 1px dashed rgba(255,255,255,0.08) !important;
            }
        </style>
        """, unsafe_allow_html=True)

    # Render a single uploader widget safely!
    uploaded_file = st.file_uploader("", type=["pdf"], key="pdf_source_uploader", label_visibility="collapsed")
    
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
                            # Only skip TOC helper pages if PDF is extremely huge (e.g. >30 pages), otherwise respect outline text.
                            if num_pages > 30 and i < 4:
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
                api_key_to_use = get_companion_api_key()
                
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
                            "You are an expert academic tutor. Analyze the provided content.\n"
                            "1. Extract 10-15 high-quality, dense study keycards (facts/definitions).\n"
                            "   - CRITICAL: Each keycard must contain a clear topic heading followed by a thorough, detailed, and rigorous academic definition/explanation "
                            "     (e.g., 'Quantum Superposition | Superposition is a fundamental principle of quantum mechanics where...').\n"
                            "   - If the uploaded document is just a Table of Contents, outline, index, or syllabus of topics, you MUST NOT just copy-paste the sparse titles. "
                            "     Instead, use your vast internal academic knowledge base to reconstruct and write deep, high-quality, full-length study card explanations/notes "
                            "     for each of those listed topics.\n"
                            "2. Generate 10-15 multiple-choice questions (MCQs) targeting these exact study concepts.\n"
                            "   - Each MCQ must have exactly 4 realistic, distinct options, with one clearly correct answer (correctAnswer index 0-3).\n"
                            "Your response MUST be an exact JSON structure containing 'keycards' and 'mcqs'."
                        )
                        
                        contents_payload = [prompt]
                        if pdf_text and len(pdf_text.strip()) > 100:
                            contents_payload.append(f"Document Text Content:\n{pdf_text[:120000]}")
                        else:
                            # Direct PDF bytes passing ensures perfect parsing even if text extraction is small/scanned
                            pdf_bytes = uploaded_file.getvalue()
                            try:
                                contents_payload.append(
                                    types.Part.from_bytes(
                                        data=pdf_bytes,
                                        mime_type="application/pdf"
                                    )
                                )
                            except Exception:
                                contents_payload.append(f"Document Text Content:\n{pdf_text[:120000]}")
                        
                        config_args = {
                            "response_mime_type": "application/json"
                        }
                        if pydantic_available:
                            config_args["response_schema"] = StudySchema

                        response = client.models.generate_content(
                            model="gemini-3.5-flash",
                            contents=contents_payload,
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
                
                card_html_template = """
                <!DOCTYPE html>
                <html>
                <head>
                    <link rel="preconnect" href="https://fonts.googleapis.com">
                    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:ital,wght@1,400;1,500&display=swap" rel="stylesheet">
                    <style>
                        html, body {
                            margin: 0;
                            padding: 0;
                            background-color: transparent;
                            font-family: 'Inter', -apple-system, sans-serif;
                            color: #ffffff;
                            overflow: hidden;
                            height: 100%;
                        }
                        .card {
                            background-color: #121212;
                            border: 1px solid rgba(255, 255, 255, 0.06);
                            padding: 18px 20px;
                            border-radius: 14px;
                            position: relative;
                            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
                            box-sizing: border-box;
                            height: calc(100% - 10px);
                            display: flex;
                            flex-direction: column;
                            justify-content: space-between;
                            transition: all 0.3s ease;
                        }
                        .card:hover {
                            border-color: rgba(16, 185, 129, 0.3);
                            box-shadow: 0 4px 20px rgba(16, 185, 129, 0.05);
                        }
                        .idx {
                            position: absolute;
                            top: 12px;
                            right: 16px;
                            font-size: 28px;
                            font-family: 'Playfair Display', serif;
                            font-style: italic;
                            color: rgba(16, 185, 129, 0.08);
                            user-select: none;
                        }
                        .lbl {
                            color: #10b981;
                            font-family: monospace;
                            font-size: 10px;
                            margin: 0 0 6px 0;
                            text-transform: uppercase;
                            letter-spacing: 2px;
                            font-weight: bold;
                        }
                        .text {
                            color: rgba(255, 255, 255, 0.92);
                            font-size: 14px;
                            line-height: 1.5;
                            font-weight: 300;
                            margin: 0 0 12px 0;
                            padding-right: 12px;
                        }
                        .btn {
                            background-color: rgba(255, 255, 255, 0.04);
                            border: 1px solid rgba(255, 255, 255, 0.08);
                            color: rgba(255, 255, 255, 0.7);
                            padding: 6px 14px;
                            border-radius: 9999px;
                            font-size: 11px;
                            font-weight: 600;
                            cursor: pointer;
                            display: inline-flex;
                            align-items: center;
                            gap: 6px;
                            font-family: 'Inter', sans-serif;
                            transition: all 0.2s ease;
                            outline: none;
                        }
                        .btn:hover {
                            background-color: rgba(16, 185, 129, 0.12);
                            border-color: rgba(16, 185, 129, 0.4);
                            color: #10b981;
                            transform: translateY(-1px);
                        }
                        .btn:active {
                            transform: translateY(0);
                        }
                    </style>
                </head>
                <body>
                    <div class="card">
                        <div>
                            <span class="idx">__PADDED_IDX__</span>
                            <div class="lbl">Foundation Fact</div>
                            <div class="text">__CARD_TEXT__</div>
                        </div>
                        <div>
                            <button class="btn" onclick="speakText()">
                                🔊 Listen to Insight
                            </button>
                        </div>
                    </div>
                    <script>
                        function speakText() {
                            if (!window.speechSynthesis) {
                                alert("Speech synthesis not supported in your browser.");
                                    return;
                            }
                            window.speechSynthesis.cancel();
                            
                            let text = __JS_SAFE_TEXT__;
                            let utterance = new SpeechSynthesisUtterance(text);
                            utterance.lang = "en-US";
                            utterance.rate = 0.95;
                            utterance.pitch = 1.0;
                            
                            window.speechSynthesis.speak(utterance);
                        }
                    </script>
                </body>
                </html>
                """

                for idx, card in enumerate(cards):
                    card_text = card.get("text", "")
                    padded_idx = str(idx + 1).zfill(2)
                    js_safe_text_json = json.dumps(card_text)
                    
                    card_html_instance = card_html_template\
                        .replace("__PADDED_IDX__", padded_idx)\
                        .replace("__CARD_TEXT__", card_text)\
                        .replace("__JS_SAFE_TEXT__", js_safe_text_json)
                    
                    components.html(card_html_instance, height=195)
                        
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
                            st.error(f"Incorrect. Correct statement is:\n\n{options[correct_idx]}")
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
        # No file is currently uploaded, clean active memory caches
        st.session_state.current_file = None
        st.session_state.study_data = None
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False

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

# Permanent elegant carbon footer matching React UI bottom bar exactly
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; padding-top: 40px; margin-top: 80px; border-top: 1px solid rgba(255,255,255,0.05); color: rgba(255,255,255,0.25); font-family: 'JetBrains Mono', monospace; font-size: 9px; letter-spacing: 1.5px; width: 100%;">
    <div style="display: flex; align-items: center; gap: 8px;">
        <span style="color: #10b981; font-size: 8px; animation: pulse 2.5s infinite;">●</span> SECURE PDF PIPELINE &nbsp;|&nbsp; EXTRACTION VER 1.5.24
    </div>
    <div>
        © 2026 LUMEN SYSTEMS · HIGH FIDELITY REASONING ENGINE
    </div>
</div>
<style>
@keyframes pulse {
    0% { opacity: 0.35; }
    50% { opacity: 1; }
    100% { opacity: 0.35; }
}
</style>
""", unsafe_allow_html=True)
