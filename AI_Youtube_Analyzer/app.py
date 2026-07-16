import streamlit as st
import re
import json
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from google.genai.errors import ServerError
from pydantic import BaseModel, Field
from typing import List

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI YouTube Video Summarizer",
    page_icon="🎥",
    layout="wide"
)

# --- GOOGLE GENAI SCHEMA FOR STRUCTURED SUMMARY ---
class QAPair(BaseModel):
    question: str
    answer: str

class VideoAnalysis(BaseModel):
    summary: str = Field(..., description="A short, engaging 2-3 sentence summary of the video.")
    detailed_explanation: str = Field(..., description="A comprehensive multi-paragraph breakdown of the video's core concepts.")
    key_points: List[str] = Field(..., description="List of 5-8 bulleted key takeaways.")
    important_insights: List[str] = Field(..., description="List of high-level revelations or meta-trends discussed.")
    suggested_qna: List[QAPair] = Field(..., description="Generates 5 logical Questions and Answers based directly on the video.")

# --- HELPER FUNCTIONS ---
def extract_video_id(url: str) -> str:
    """Extracts the 11-character YouTube video ID from various URL formats."""
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_video_transcript(video_id: str) -> str:
    """Retrieves and compiles the transcript of a YouTube video."""
    try:
        # Corrected method call
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([item['text'] for item in transcript])
        return text
    except Exception as e:
        st.error(f"Could not retrieve transcript: {e}. (Note: Some videos have disabled transcripts or require region-specific verification.)")
        return None

def analyze_video_data(transcript: str, api_key: str) -> VideoAnalysis:
    """Invokes Gemini to analyze the transcript into a structured schema."""
    client = genai.Client(api_key=api_key)
    prompt = f"Analyze this YouTube video transcript and structure the feedback.\n\nTranscript:\n{transcript}"
    
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": VideoAnalysis,
            }
        )
        return VideoAnalysis(**json.loads(response.text))
    except ServerError as e:
        if e.status_code == 503: # Safe 503 Fallback
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": VideoAnalysis,
                }
            )
            return VideoAnalysis(**json.loads(response.text))
        else:
            raise e

def answer_user_query(transcript: str, question: str, api_key: str) -> str:
    """Provides a targeted answer to a custom user question using the transcript."""
    client = genai.Client(api_key=api_key)
    prompt = (
        f"Answer the question thoroughly and accurately based solely on this video transcript.\n\n"
        f"Transcript:\n{transcript}\n\n"
        f"Question: {question}"
    )
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )
    return response.text

# --- UI DESIGN ---
st.title("🎥 AI YouTube Video Summarizer & Q&A")
st.write("Extract transcripts, generate deep-dive analyses, and ask custom questions about any YouTube video instantly.")

# 1. Sidebar Config
with st.sidebar:
    st.header("🔑 Configuration")
    user_api_key = st.text_input("Enter Gemini API Key", type="password")
    st.markdown("[Get a free API Key from Google AI Studio](https://aistudio.google.com/)")

# Initialize Session State to persist data across page re-runs
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "analysis" not in st.session_state:
    st.session_state.analysis = None

# 2. Main Video URL Input
video_url = st.text_input("Enter YouTube Video URL:", placeholder="https://www.youtube.com/watch?v=...")

if video_url:
    video_id = extract_video_id(video_url)
    if not video_id:
        st.error("Invalid YouTube URL. Please provide a valid watch link.")
    else:
        # Split layout into two columns: Video Frame & Action Panel
        col_vid, col_action = st.columns([1, 1])
        
        with col_vid:
            st.video(video_url)
            
        with col_action:
            st.info("Video detected successfully! Click the button below to process.")
            if st.button("🚀 Analyze Video", use_container_width=True):
                if not user_api_key:
                    st.warning("Please provide your Gemini API Key in the sidebar.")
                else:
                    with st.spinner("Extracting transcript and generating report..."):
                        transcript_text = get_video_transcript(video_id)
                        if transcript_text:
                            st.session_state.transcript = transcript_text
                            st.session_state.analysis = analyze_video_data(transcript_text, user_api_key)
                            st.success("Analysis complete!")

# 3. Render Results Tabs
if st.session_state.analysis is not None:
    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary & Insights", "📖 Detailed Breakdown", "❓ Recommended Q&A", "💬 Chat with Video"])
    
    with tab1:
        st.subheader("💡 TL;DR Summary")
        st.info(st.session_state.analysis.summary)
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📌 Key Takeaways")
            for pt in st.session_state.analysis.key_points:
                st.write(f"- {pt}")
        with c2:
            st.subheader("⚡ Meta Insights")
            for ins in st.session_state.analysis.important_insights:
                st.write(f"- {ins}")
                
    with tab2:
        st.subheader("Detailed Breakdown")
        st.write(st.session_state.analysis.detailed_explanation)
        
    with tab3:
        st.subheader("AI-Generated Questions & Answers")
        for item in st.session_state.analysis.suggested_qna:
            with st.container():
                st.markdown(f"**Q: {item.question}**")
                st.write(f"A: {item.answer}")
                st.markdown("---")
                
    with tab4:
        st.subheader("Ask a Custom Question")
        user_query = st.text_input("Ask anything about what was said in this video:", placeholder="e.g., What was the code example at the end?")
        if user_query:
            with st.spinner("Searching transcript for answers..."):
                answer = answer_user_query(st.session_state.transcript, user_query, user_api_key)
                st.markdown("#### **Answer:**")
                st.write(answer)
