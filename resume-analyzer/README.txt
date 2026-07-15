# 📄 AI ATS Resume Analyzer

An enterprise-grade applicant tracking system (ATS) simulator. This application parses PDF resumes, analyzes the text against algorithmic recruiting filters using the Google Gemini API, and renders a high-level dashboard featuring compatibility scores, executive summaries, and actionable structural improvements.

## 🚀 Live Demo
You can try the live, hosted version of this application here: 
👉 **[INSERT_YOUR_STREAMLIT_URL_HERE]** *(Note: Replace this with your actual .streamlit.app link!)*

## ✨ Features
* **PDF Parser:** Raw text extraction using `PyPDF2`.
* **ATS Benchmarking:** Real-time scoring (0-100) based on standard parsing algorithms.
* **Segmented Insights:** Interactive tabs splitting feedback into Strengths, Areas of Improvement, and Executive Summaries.
* **Secure API Configuration:** Built-in sidebar allowing users to securely execute calls using their personal Gemini API keys.

## 🛠️ Local Installation & Setup

To run this dashboard locally on your machine, follow these steps:

### 1. Clone the Repository
```bash
git clone [https://github.com/Painx9/LLM_Applications.git](https://github.com/Painx9/LLM_Applications.git)
cd LLM_Applications/resume-analyzer ```

2. Set Up a Virtual Environment

```Bash
python -m venv .venv
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Windows (CMD):
.venv\Scripts\activate.bat```

3. Install Dependencies

```Bash
pip install -r requirements.txt```

4. Run the Streamlit Application


```Bash
python -m streamlit run app.py
🧠 Model Details
This application leverages the Gemini 3.1 Flash Lite model (gemini-3.1-flash-lite) to execute rapid, cost-effective structural and semantic analyses on incoming text.```


---

### Push Your Documentation to GitHub
Once you have saved both README files, open your **PowerShell** window and push them to your repository



