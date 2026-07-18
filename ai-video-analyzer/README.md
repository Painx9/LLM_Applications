**🎥 AI YouTube Video Analyzer Dashboard**

A lightweight, production-ready Streamlit dashboard built to dynamically analyze, summarize, and interview YouTube videos using Google Gemini (gemini-3.1-flash-lite).  Unlike fragile scraping methods that get immediately blocked by YouTube's IP filters on cloud environments, this project uses an explicit structured media stream design (types.Part.from_uri) to leverage Google's native internal multimodal video parsing engine.

✨ FeaturesInstant Video Summarization: 

1. Generates a high-quality technical breakdown including summary, detailed explanation, core key points, and architectural insights.
2. Semantic Video Q&A: A contextual chat interface allowing users to ask deep questions directly about the video's content without needing to look through a transcript.
3. Cloud-Native Compliant: Built explicitly to bypass cloud provider IP bans (AWS, Google Cloud, Streamlit Cloud) by offloading processing to the official Google Gemini multimodal API backend.
4. Clean UI/UX Layout: Responsive twin-column dashboard split perfectly between static insights and live conversational elements.

🛠️ Repository File Structure
Ensure your ai-video-analyzer directory is organized as follows:
```
Plaintext
LLM_Applications/
└── ai-video-analyzer/
    ├── .gitignore.txt             # Protects environment keys & cache files
    ├── README.md                  # Project documentation (this file)
    ├── app.py                     # Main Streamlit web application dashboard
    ├── requirements.txt           # Verified pip dependencies
    └── AI_Youtube_Video_Summarizer.ipynb # Original prototyping notebook
```
 🚀 Quick Start Guide
1. Prerequisites
Make sure you have Python 3.10+ installed on your local machine.

2. Clone the Repository & Navigate
```Bash
git clone https://github.com/YOUR_USERNAME/LLM_Applications.git
cd LLM_Applications/ai-video-analyzer
```
3. Install Dependencies
Install the required packages using the optimized dependency file:

```Bash
pip install -r requirements.txt
```
4. Run the Streamlit Dashboard
```Bash
streamlit run app.py
```
This will open the dashboard in your default local web browser automatically at http://localhost:8501.

⚙️ Configuration & API Setup
1. Head over to Google AI Studio and grab a free API Key.
2. Open the dashboard in your browser.
3. Paste your API key directly into the secure masked password field inside the Left Sidebar Settings.

4. Paste any valid YouTube URL (e.g., [https://www.youtube.com/watch?v=](https://www.youtube.com/watch?v=)...) into the input box and click Analyze Video.

📦 Core Dependencies (requirements.txt)

The dashboard is built using the official modern Google GenAI SDK ecosystem:
```Plaintext
google-genai>=2.0.0
streamlit>=1.42.0
```
📜 How the Architecture Works Behind the Scenes

Standard text-based LLMs often attempt to read a YouTube URL string literally, leading to heavy hallucinations. This implementation wraps the video link in a structured payload that signals Google's media pipeline to ingest the data correctly:

```Python
# Force-feeds the video stream natively to the Gemini pipeline
video_part = types.Part.from_uri(
    file_uri=url,
    mime_type="video/mp4"
)

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=[video_part, prompt]
)
```
---
## 🎓 Acknowledgments

This project was built as a hands-on learning exercise based on an educational YouTube tutorial covering the Google GenAI SDK. The original notebook concept was re-engineered and upgraded here to support modern production deployment on Streamlit Cloud.

📄 License
Distributed under the MIT License. Feel free to modify and expand it for your own portfolio use cases!
