import streamlit as st
from google import genai
import PyPDF2
import json

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="📊",
    layout="wide",  # Utilizing the full screen width
    initial_sidebar_state="expanded"
)

# --- SIDEBAR (INPUT CONTROLS) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135673.png", width=80)
    st.title("Settings & Upload")
    st.markdown("Configure your scanner settings below.")
    
    # 1. API Key Setup
    api_key = None
    try:
        if "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
    except Exception:
        pass

    if not api_key:
        api_key = st.text_input("Gemini API Key", type="password", help="Input your Google Gemini API Key here.")
    
    st.divider()
    
    # 2. File Upload in Sidebar
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    
    st.divider()
    st.markdown("💡 *Tip: Resumes with clean, single-column formats usually score higher in modern ATS systems.*")

# --- MAIN PAGE HEADER ---
st.title("💼 AI ATS Resume Intelligence Dashboard")
st.markdown("Analyze resumes against algorithmic filters and instantly unlock strategic feedback.")

# --- HELPERS ---
def read_resume(uploaded_file):
    text = ""
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    except Exception as e:
        st.sidebar.error(f"Error reading PDF: {e}")
    return text

def analyze_resume(text, api_key):
    client = genai.Client(api_key=api_key)
    prompt = f"""
    You are an ATS resume analyzer.

    Analyze the resume below and return ATS score and feedback.

    Resume:
    {text}

    Return in JSON format with exactly these keys:
    - ats_score (0-100)
    - summary
    - strengths (list of strings)
    - weaknesses (list of strings)

    Rules:
    - Output ONLY valid, raw JSON. 
    - Do not wrap the JSON in ```json markdown code blocks.
    - No extra conversational text before or after.
    """
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
        )
        raw_text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(raw_text)
    except Exception as e:
        st.error(f"Error calling Gemini API: {e}")
        return None

# --- MAIN APP ROUTING ---
if not api_key:
    st.warning("⚠️ Please provide a Gemini API Key in the sidebar to unlock the dashboard.")
    st.stop()

if uploaded_file is None:
    # Beautiful landing placeholder
    st.info("👈 Get started by dragging & dropping your PDF resume into the sidebar uploader!")
    
    # Showcase of what the dashboard looks like (Mockup Cards)
    st.subheader("What you'll get:")
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("ATS Compatibility", "85%", "Target is > 80%", border=True)
    m_col2.metric("Formatting Score", "Excellent", "No tables detected", border=True)
    m_col3.metric("Key Missing Words", "4 detected", "Fix suggested", border=True)

else:
    # We have a file! Let's process it.
    resume_text = read_resume(uploaded_file)
    
    if resume_text:
        st.success("🎉 Resume successfully parsed! Click the button below to start the AI analysis.")
        
        # Center-aligned premium action button
        col_btn, _ = st.columns([1, 3])
        with col_btn:
            start_analysis = st.button("🚀 Run ATS Diagnosis", type="primary", use_container_width=True)
            
        if start_analysis:
            with st.spinner("Decoding formatting and checking keyword matches..."):
                result = analyze_resume(resume_text, api_key)
            
            if result:
                st.balloons()
                st.markdown("## 📊 Scan Report")
                
                # --- SECTION 1: KEY PERFORMANCE INDICATORS ---
                score = int(result.get("ats_score", 0))
                
                kpi1, kpi2, kpi3 = st.columns(3)
                
                # Card 1: Main ATS Score
                with kpi1:
                    st.metric(label="Overall ATS Score", value=f"{score}/100", border=True)
                
                # Card 2: Readability Rating
                with kpi2:
                    if score >= 80:
                        rating, delta_val = "Interview Ready", "Optimal"
                    elif score >= 50:
                        rating, delta_val = "Needs Tweaks", "Moderate"
                    else:
                        rating, delta_val = "Rewrite Required", "Low Match"
                    st.metric(label="Portfolio Status", value=rating, delta=delta_val, border=True)
                
                # Card 3: File Check
                with kpi3:
                    st.metric(label="File Integrity", value="Verified PDF", delta="Parser Readable", border=True)
                
                # Visual Score Bar
                st.markdown("**ATS Benchmarking Progress**")
                if score >= 80:
                    st.progress(score / 100, "High ATS Compatibility Match")
                elif score >= 50:
                    st.progress(score / 100, "Moderate ATS Compatibility Match")
                else:
                    st.progress(score / 100, "Action Required: Critical Issues Detected")
                
                st.divider()
                
                # --- SECTION 2: TABS FOR DEEPER ANALYSIS ---
                tab_overview, tab_strengths, tab_fixes = st.tabs([
                    "📝 Executive Summary", 
                    "✅ Strengths & Highlights", 
                    "🛠️ Actionable Adjustments"
                ])
                
                with tab_overview:
                    st.subheader("AI Executive Assessment")
                    st.write(result.get("summary", "No summary feedback available."))
                    
                with tab_strengths:
                    st.subheader("Highlighting What Worked")
                    st.markdown("These elements are beautifully structured and will pass modern parser logic:")
                    strengths = result.get("strengths", [])
                    if isinstance(strengths, list) and len(strengths) > 0:
                        for item in strengths:
                            st.markdown(f"⭐ **{item}**")