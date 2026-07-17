Markdown
🚀 Production-Ready LLM Applications

Welcome to my central repository for Large Language Model (LLM) applications. This repository serves as a showcase of production-grade AI tools, agents, and pipelines built using state-of-the-art LLMs (including Google Gemini, OpenAI GPT, and open-source models).

Each project in this is fully functional, utilizing modern frontend interfaces (like Streamlit), robust error handling, and structured data extraction.

---

🛠️ Core Tech Stack & Skills Highlighted

* **LLM SDKs:** Google GenAI SDK, OpenAI API, LangChain
* **Frameworks & Frontends:** Streamlit, FastAPI
* **Data & Parsers:** PyPDF2, Pydantic (Structured Outputs), JSON schemas
* **Advanced AI Concepts:** Retrieval-Augmented Generation (RAG), Semantic Search, Function Calling, System Instructions, Robust Exception Fallbacks (503 handling)

---

📁 Project Directory

| Project Name | Description | Key Tech Used | Quick Link |
| :--- | :--- | :--- | :--- |
| **📄 AI ATS Resume Analyzer** | Uploads PDF resumes directly, parses formatting, and uses Gemini to output structured JSON ATS feedback and scores. | `google-genai`, `Streamlit`, `Pydantic` | [View Folder](resume-analyzer) |
| **🎥 AI YouTube Video Analyzer** | Extracts video transcripts, metadata, and performs deep-dive sentiment/topic analysis with semantic summarization. | `google-genai`, `Streamlit`, `YouTube Transcript API` | [View Folder](./AI_YouTube_Analyzer/) |


💡 **How to navigate:** Each project has its own sub-folder containing its dedicated codebase, local installation steps, and individual setup guides.

---

## ⚙️ Global Setup Guide

While individual projects may have specific requirements, you can set up the global environment for this entire suite of tools by following these steps:

### 1. Clone this Repository
```
bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/LLM_Applications.git](https://github.com/YOUR_GITHUB_USERNAME/LLM_Applications.git)
cd LLM_Applications
```
2. Configure Environment Variables
Most applications in this repository require API keys. Create a .env file in the root directory:
```
Code snippet
# Google Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# OpenAI API Configuration (If used)
OPENAI_API_KEY=your_openai_api_key_here
```
3. Install Common Dependencies
```
Bash
pip install -r requirements.txt
```
📈 System Design Philosophy
Across all these projects, I focus heavily on writing production-ready code. This means:

1. Bulletproof Error Handling: Implementing automatic model fallbacks (e.g., falling back to stable older models like Gemini 1.5 if a preview model throws a 503 Service Unavailable error).

2. Strict Type Safety: Forcing models to output structured, parseable JSON via Pydantic schemas instead of raw string parsing.

3. Optimized Token Budgets: Designing compact, context-focused system prompts to keep latency and costs low.

📜 License
This project is licensed under the MIT License. Feel free to use, modify, and build upon any of these code bases for your own applications!




  
