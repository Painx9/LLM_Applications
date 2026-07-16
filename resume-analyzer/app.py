import streamlit as st
import PyPDF2
import json
from google import genai
from pydantic import BaseModel, Field
from typing import List

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI ATS Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

# --- GOOGLE GENAI SCHEMA DEFINITIONS ---
class DetailedATSAnalysis(BaseModel):
    ats_score: int = Field(..., description="An overall ATS compliance score from 0 to 100.")
    summary: str = Field(..., description="A deep analysis of the candidate's professional level and domain fit.")
    strengths: List[str] = Field(..., description="List of 3-5 major highlights or solid sections of the resume.")
    weaknesses: List[str] = Field(..., description="Crucial elements this resume is lacking or needs to optimize.")

# --- SIDEBAR CONFIGURATION ---
st.sidebar.title("🔑 API Configuration")
user_api_key = st.sidebar.text_input(
    "Enter Gemini API Key",
    type="password",
    placeholder="AIzaSy...",
    help="Grab a free API key from Google AI Studio to run this tool."
)

if user_api_key:
    st.session_state["GOOGLE_API_KEY"] = user_api_key
else:
    st.session_state["GOOGLE_API_KEY"] = None
    st.sidebar.warning("⚠️ Enter your API key to activate the analyzer.")

# --- PDF Extractor ---
def read_resume(uploaded_file):
    text = ""
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    except Exception as e:
        st.error(f"Error parsing PDF file: {e}")
    return text

# --- Gemini ATS Analysis Pipeline ---
def analyze_resume(text, api_key) -> DetailedATSAnalysis:
    client = genai.Client(api_key=api_key)
    prompt = f"""
You are an expert ATS resume analyzer. 

Analyze the resume below and structure your feedback matching the requested schema.

Resume Content:
{text}
"""
    # Changed model identifier to gemini-3.1-flash-lite
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite", 
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": DetailedATSAnalysis,
        }
    )
    return response.parsed

# --- Dashboard Layout ---
st.title("📄 AI ATS Resume Analyzer")
st.write("Analyze formatting, structural layouts, and content gaps using custom ATS metrics.")

uploaded_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])

if uploaded_file is not None:
    st.success("Resume received!")
    
    if st.button("🚀 Run Analyzer", use_container_width=True):
        if not st.session_state.get("GOOGLE_API_KEY"):
            st.warning("Please enter your Gemini API Key in the sidebar to proceed.")
        else:
            with st.spinner("Analyzing resume content..."):
                raw_text = read_resume(uploaded_file)
                
                if not raw_text.strip():
                    st.error("Could not extract text. Please confirm this PDF is not a flat image.")
                else:
                    try:
                        analysis_result = analyze_resume(raw_text, st.session_state["GOOGLE_API_KEY"])
                        
                        st.markdown("---")
                        st.header("📊 ATS Performance Analysis")
                        
                        # ATS Metric Score Display
                        score = analysis_result.ats_score
                        if score >= 80:
                            st.metric("ATS Score", f"{score}/100", delta="Excellent Match")
                        elif score >= 50:
                            st.metric("ATS Score", f"{score}/100", delta="Needs Improvement", delta_color="off")
                        else:
                            st.metric("ATS Score", f"{score}/100", delta="Weak Match", delta_color="inverse")
                        
                        st.subheader("💡 Analysis Summary")
                        st.info(analysis_result.summary)
                        
                        # Columns layout for Strengths & Weaknesses
                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("✅ Identified Strengths")
                            for item in analysis_result.strengths:
                                st.write(f"✔️ {item}")
                        with col2:
                            st.subheader("❌ Areas to Improve")
                            for item in analysis_result.weaknesses:
                                st.write(f"🔍 {item}")
                                
                    except Exception as e:
                        st.error(f"Failed to parse or run the analysis. Error: {e}")
