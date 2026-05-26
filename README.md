# 🎓 Lumina AI Study Companion
### Dynamic Multi-Modal Learning Portal & Offline-Ready Synthesis Engine
*Engineered for university evaluation and elite academic deployment.*

---

## 📂 1. Advanced Architecture & File Ecosystem
To keep your workspace clean and professional, Lumina maintains a minimalist files footprint. Unnecessary files have been excluded. Below are the key files of your project:

```text
lumina-ai-study-assistant/   <-- YOUR WORKSPACE ROOT
├── server.ts                 # Express full-stack Node.js development & production server
├── package.json              # Client/Server dependencies & scripts execution pipeline
├── tsconfig.json             # TypeScript structural compiler specifications
├── vite.config.ts            # High-speed Vite client application assets builder
├── index.html                # Main SPA application viewport frame
├── app.py                    # Streamlit dynamic study workspace launcher (Python)
├── requirements.txt          # Python dependencies manifest for Streamlit
├── README.md                 # Professional documentation & step-by-step masterclass
└── src/
    ├── main.tsx              # React framework bootstrapping routine
    ├── index.css             # Tailwind layout specifications & styling properties
    └── App.tsx               # Primary Single-Page Interactive HUD & Dashboard (Self-contained!)
```

---

## ⚡ 2. Zero-Configuration Local Offline Fallback Protocol
A major challenge when submitting projects to teachers is that **they may not have an active Google Gemini API key configured**, which typically leads to errors or screen crashes on launch.

Lumina solves this with a **Graceful Local Parsing Fallback**:
* **How it works:** If you run the code without setting a `.env` API key, or if the API key is hit with quota limits, the servers (both `server.ts` and `app.py`) instantly route the uploaded PDF to an **offline-ready local parser**.
* **The output:** It scans the PDF sentences and extracts high-quality study keycards and dynamically generates multiple-choice practice questions directly from your material without sending a single byte of data to the cloud!
* **Success guarantee:** Your instructors or assessors can download your folder and immediately run PDFs locally with **zero error screens**.

---

## 🛠️ 3. How to Run & Connect Streamlit
We have written a highly optimized, responsive **Python Streamlit version** of your study companion inside `app.py`. This lets you deploy your app directly onto the free, high-performance Streamlit Community Cloud in just a couple of minutes!

### Step 1: Install Python Dependencies
Open your terminal inside the project root folder on Windows/MacOS and run:
```cmd
pip install -r requirements.txt
```

### Step 2: Run Streamlit Locally
Initiate the interactive Python application by typing:
```cmd
streamlit run app.py
```
This opens `http://localhost:8501` automatically in your browser where you can test the offline PDF study features!

---

## 📦 4. How to Run the Primary Full-Stack Node.js App
To run the ultimate React UI + Express backend stack locally:
1. Open your terminal in the root folder.
2. Install standard Node packages:
   ```cmd
   npm install
   ```
3. Run the development server:
   ```cmd
   npm run dev
   ```
4. Access the high-fidelity UI at `http://localhost:3000`!

---

## 🚀 5. Uploading Your Code to GitHub (Masterclass)

### Method 1: The Easiest Way — GitHub Desktop (Recommended!)
1. Open your browser, download and install [GitHub Desktop](https://desktop.github.com/).
2. Log in using your GitHub account.
3. Click **File &rarr; Add Local Repository...**
4. Select your **workspace root folder** (the folder containing `package.json`).
5. If prompt warning appears, click on **"create a repository"** link. Set the name as `lumina-ai-study-companion` and path pointing to your folder. Click **Create Repository**.
6. At the bottom-left summary box, type `feat: final release of Lumina AI study companion` and click the blue **Commit to main** button.
7. Click **Publish Repository** at the header list. Uncheck "Keep this code private" to make it public, and hit publish!

---

### Method 2: Command Line Git Terminal Guide
Click the Windows Start button, type `cmd` (Command Prompt), point it to your root project folder, and copy-paste these commands:

```cmd
# 1. Initialize empty repository setup
git init

# 2. Stage all files for tracking
git add .

# 3. Commit files locally
git commit -m "feat: final release of Lumina AI study companion"

# 4. Point repository up to the cloud URL
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/lumina-ai-study-companion.git

# 5. Push code cleanly to the branch
git push -u origin main
```

---

## 🔄 How to Push Future Updates
Whenever you make further modifications online or locally:
```cmd
git add .
git commit -m "update: enhanced core layout properties"
git push origin main
```
Your GitHub repository will update immediately!
