# AI ATS Resume Analyzer

An automated ATS (Applicant Tracking System) Resume Analyzer built to run seamlessly in Google Colab. This tool allows users to upload a PDF resume, automatically extracts the text, and leverages Google's Gemini generative AI model to score and provide structural feedback in a clean, structured JSON format.

## 🚀 Features

* **Direct PDF Extraction:** Uses `PyPDF2` to read and parse local PDF files.
* **AI-Powered Feedback:** Utilizes Google's state-of-the-art `gemini-3.1-flash-lite` model to analyze your professional profile.
* **Structured JSON Output:** Guarantees standard formatted feedback containing:
  * **ATS Score:** A rating from 0 to 100.
  * **Summary:** A high-level assessment of the profile.
  * **Strengths:** Key highlights and standout sections of the resume.
  * **Weaknesses:** Tailored feedback on keyword gaps, formatting issues, and improvements.
* **Google Colab Friendly:** Ready to run in any browser with quick file-uploader widgets and secure secret API management.

---

## 🛠️ Tech Stack & Dependencies

* **Language:** Python 3
* **PDF Parser:** `PyPDF2`
* **AI Model API:** `google-genai` (SDK)
* **Platform:** Google Colab

---

## ⚙️ How to Setup & Run

### 1. Prerequisite (Google Gemini API Key)
To run this analyzer, you need a free API Key from Google AI Studio. 
* Generate your key at [Google AI Studio](https://aistudio.google.com/).

### 2. Setup Google Colab Secrets
To protect your credentials:
1. Open your copy of the notebook in Google Colab.
2. Click on the **Key icon (Secrets)** in the left sidebar.
3. Add a new secret:
   * **Name:** `GOOGLE_API_KEY`
   * **Value:** *Paste your Gemini API key here*
4. Toggle on **Notebook access** for this secret.

### 3. Execution Steps
Once inside the notebook, run the cells sequentially:

* **Install Dependencies:** Installs the required document reading and Gemini client libraries.
```bash
pip install google-genai PyPDF2
Upload Resume: An interactive upload box will prompt you to select your PDF resume file from your local computer.

Analyze: The script parses the text and sends a structured prompt to the Gemini API.

Get Feedback: The terminal will print a structured JSON feedback payload.

📊 Expected Output Format
The analyzer returns a clean, structured JSON payload similar to the following:

JSON
{
  "ats_score": 85,
  "summary": "The candidate shows robust experience in full-stack Python development and cloud infrastructure, though some metric-driven accomplishments are missing.",
  "strengths": [
    "Clear project headings and standard font layouts",
    "Strong keyword density for 'Python', 'Docker', and 'AWS'",
    "Education and certifications are highly visible"
  ],
  "weaknesses": [
    "Work experience points are passive; use more action verbs",
    "Lacks quantitative metrics (e.g., 'improved performance by X%')",
    "Missing a dedicated portfolio/GitHub link in the header"
  ]
}

📜 License
This project is licensed under the MIT License - feel free to customize and use it for your own applications!

   
