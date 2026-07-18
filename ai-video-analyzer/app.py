import streamlit as st
from google import genai

# Page configuration
st.set_page_config(
    page_title="AI YouTube Video Analyzer",
    page_icon="🎥",
    layout="wide"
)

# App Header
st.title("🎥 AI YouTube Video Analyzer")
st.markdown("Extract insights, summaries, and ask questions directly from any YouTube video using Gemini.")

# Sidebar Configuration for API Key
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Google API Key:", type="password", help="Your Gemini API key.")

# Initialize Gemini Client if API key is provided
client = None
if api_key:
    client = genai.Client(api_key=api_key)
else:
    st.sidebar.warning("Please enter your Google API Key to proceed.")

# Analysis Function using Gemini's Native Video Support
def analyze_video(url):
    prompt = f"""
    Analyze this YouTube video and provide:

    1. Summary (short)
    2. Detailed explanation
    3. Key points (bullet list)
    4. Important insights
    5. 5 Questions & Answers
    """
    
    # Pass the URL directly as a part of the contents list
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",  # Configured to use your requested model variant
        contents=[url, prompt]
    )
    return response.text

# Chat Model Function
def ask_question(url, question):
    prompt = f"""
    Answer the following question based strictly on this video:
    
    Question: {question}
    """
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",  # Configured to use your requested model variant
        contents=[url, prompt]
    )
    return response.text

# Initialize session state for holding video URL & initial analysis
if "current_url" not in st.session_state:
    st.session_state.current_url = None
if "analysis" not in st.session_state:
    st.session_state.analysis = None

# Main Dashboard Layout
video_url = st.text_input("Enter YouTube Video URL:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Analyze Video", type="primary"):
    if not client:
        st.error("Please configure your Google API Key in the sidebar first.")
    elif not video_url:
        st.warning("Please provide a valid YouTube link.")
    else:
        with st.spinner("Gemini is analyzing the video directly..."):
            try:
                st.session_state.current_url = video_url
                st.session_state.analysis = analyze_video(video_url)
                st.success("Analysis Complete!")
            except Exception as e:
                st.error(f"Error analyzing video: {e}")

# Display Results UI if Data Exists
if st.session_state.analysis:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 Video Insights & Summary")
        st.markdown(st.session_state.analysis)
        
    with col2:
        st.subheader("💬 Ask Questions About the Video")
        user_query = st.text_input("What do you want to know about this video?")
        
        if st.button("Ask AI"):
            if user_query:
                with st.spinner("Finding answer..."):
                    try:
                        answer = ask_question(st.session_state.current_url, user_query)
                        st.markdown("### 🤖 Answer:")
                        st.info(answer)
                    except Exception as e:
                        st.error(f"Error generating answer: {e}")
            else:
                st.warning("Please enter a question first.")
