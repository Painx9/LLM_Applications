import streamlit as st
import PyPDF2
import json
from google import genai

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI ATS Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

# --- SIDEBAR CONFIGURATION ---
st.sidebar.title("🔑 API Configuration")
user_api_key = st.sidebar.text_input(
    "Enter Gemini API Key",
    type="password",
    placeholder="AIzaSy...",
    help="Grab a free API key from Google AI Studio to run this tool."
)

# Securely save the key in session state
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
def analyze_resume(text, api_key):
    client = genai.Client(api_key=api_key)
    prompt = f"""
You are an ATS resume analyzer.

Analyze the resume below and return ATS score and feedback.

Resume:
{text}

Return in JSON format with:
- ats_score (0-100)
- summary
- strengths (list of strings)
- weaknesses (list of strings)

Rules:
- Output ONLY JSON
- No extra text, no markdown block wrappers (just raw JSON)
"""
    # Using 'gemini-2.5-flash' which is the standard, stable model in the Google GenAI SDK
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )
    return response.text

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
                    result_json_str = None # Initialize empty to prevent NameError if API fails
                    try:
                        result_json_str = analyze_resume(raw_text, st.session_state["GOOGLE_API_KEY"])
                        result_data = json.loads(result_json_str)
                        
                        st.markdown("---")
                        st.header("📊 ATS Performance Analysis")
                        
                        # ATS Metric Score Display
                        score = int(result_data.get("ats_score", 0))
                        if score >= 80:
                            st.metric("ATS Score", f"{score}/100", delta="Excellent Match")
                        elif score >= 50:
                            st.metric("ATS Score", f"{score}/100", delta="Needs Improvement", delta_color="off")
                        else:
                            st.metric("ATS Score", f"{score}/100", delta="Weak Match", delta_color="inverse")
                        
                        st.subheader("💡 Analysis Summary")
                        st.info(result_data.get("summary", "No summary generated."))
                        
                        # Columns layout for Strengths & Weaknesses
                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("✅ Identified Strengths")
                            strengths = result_data.get("strengths", [])
                            for item in strengths:
                                st.write(f"✔️ {item}")
                        with col2:
                            st.subheader("❌ Areas to Improve")
                            weaknesses = result_data.get("weaknesses", [])
                            for item in weaknesses:
                                st.write(f"🔍 {item}")
                                
                    except Exception as e:
                        st.error(f"Failed to parse or run the analysis. Error: {e}")
                        if result_json_str:
                            st.code(result_json_str)
