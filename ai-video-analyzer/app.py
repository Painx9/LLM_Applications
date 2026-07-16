import streamlit as st
import re
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai

# --- Helpers ---
def extract_video_id(url):
    pattern = r'(?:v=|\/embed\/|\/14\/|\/v\/|youtu\.be\/|\/v=|^)([^#\&\?^\/]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.fetch(video_id)
        return " ".join([item['text'] for item in transcript])
    except Exception as e:
        st.error(f"Error fetching transcript: {str(e)}")
        return None

def analyze_video(client, transcript):
    prompt = f"""
    Analyze this YouTube video transcript and provide:
    1. Summary (short)
    2. Detailed explanation
    3. Key points (bullet list)
    4. Important insights
    5. 5 Questions & Answers

    Transcript:
    {transcript}
    """
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )
        return response.text
    except Exception as e:
        st.error(f"Error generating analysis: {str(e)}")
        return None

def ask_question(client, transcript, question):
    prompt = f"Answer the question based strictly on this video transcript:\n\nTranscript:\n{transcript}\n\nQuestion:\n{question}"
    try:
        response = client.models.generate_content(model="gemini-3.1-flash-lite", contents=prompt)
        return response.text
    except Exception as e:
        st.error(f"Error answering question: {str(e)}")
        return None

# --- UI ---
st.title("🎥 AI YouTube Video Summarizer")

api_key = st.session_state.get("GOOGLE_API_KEY")

if not api_key:
    st.info("👈 Please enter your Gemini API key in the sidebar configuration to unlock this app.")
else:
    client = genai.Client(api_key=api_key)
    video_url = st.text_input("Enter YouTube Video URL:")

    if video_url:
        video_id = extract_video_id(video_url)
        if video_id:
            st.video(video_url)
            
            if 'video_id' not in st.session_state or st.session_state.video_id != video_id:
                st.session_state.video_id = video_id
                st.session_state.transcript = None
                st.session_state.analysis = None

            if st.button("🚀 Analyze Video", use_container_width=True):
                with st.spinner("Extracting transcript..."):
                    st.session_state.transcript = get_transcript(video_id)
                if st.session_state.transcript:
                    with st.spinner("Analyzing..."):
                        st.session_state.analysis = analyze_video(client, st.session_state.transcript)

            if st.session_state.analysis:
                tab1, tab2 = st.tabs(["📊 Summary", "💬 Chat"])
                with tab1:
                    st.markdown(st.session_state.analysis)
                with tab2:
                    user_q = st.text_input("Ask a question about the video:")
                    if st.button("Ask AI") and user_q:
                        with st.spinner("Thinking..."):
                            ans = ask_question(client, st.session_state.transcript, user_q)
                            if ans:
                                st.write(ans)
