import streamlit as st
import re
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai

# Page configuration
st.set_page_config(
    page_title="AI YouTube Video Analyzer",
    page_icon="🎥",
    layout="wide"
)

# App Header
st.title("🎥 AI YouTube Video Analyzer")
st.markdown("Extract insights, summaries, and ask questions directly from any YouTube video transcript.")

# Sidebar Configuration for API Key
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Google API Key:", type="password", help="Your gemini API key.")

# Initialize Gemini Client if API key is provided
client = None
if api_key:
    client = genai.Client(api_key=api_key)
else:
    st.sidebar.warning("Please enter your Google API Key to proceed.")

# Helper function to extract Video ID from various YouTube URL formats
def extract_video_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# Extract Transcript Function
# Extract Transcript Function
def get_transcript(video_id):
    try:
        # Instantiate the API client object directly to avoid class attribute errors
        srt = YouTubeTranscriptApi()
        
        # Use the shortcut fetch method on the instance to get data
        transcript = srt.fetch(video_id)
        
        # Reconstruct the transcript into a single continuous text string
        text = " ".join([item['text'] if isinstance(item, dict) else item.text for item in transcript])
        return text
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None

# Analysis Function
def analyze_video(transcript_text):
    prompt = f"""
    Analyze this YouTube video transcript and provide:

    1. Summary (short)
    2. Detailed explanation
    3. Key points (bullet list)
    4. Important insights
    5. 5 Questions & Answers

    Transcript:
    {transcript_text}
    """
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )
    return response.text

# Chat Model Function
def ask_question(transcript_text, question):
    prompt = f"""
    Answer the question based on this video transcript:

    Transcript:
    {transcript_text}

    Question:
    {question}
    """
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )
    return response.text

# Initialize session state for holding transcript & initial analysis
if "transcript" not in st.session_state:
    st.session_state.transcript = None
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
        video_id = extract_video_id(video_url)
        if not video_id:
            st.error("Could not parse Video ID from the provided URL.")
        else:
            with st.spinner("Fetching transcript and generating analysis..."):
                transcript = get_transcript(video_id)
                if transcript:
                    st.session_state.transcript = transcript
                    st.session_state.analysis = analyze_video(transcript)
                    st.success("Analysis Complete!")

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
                    answer = ask_question(st.session_state.transcript, user_query)
                    st.markdown("### 🤖 Answer:")
                    st.info(answer)
            else:
                st.warning("Please enter a question first.")
