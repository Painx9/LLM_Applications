import streamlit as st

st.set_page_config(page_title="My LLM Projects Hub", page_icon="🚀", layout="wide")

# --- Global API Key Configuration ---
st.sidebar.title("🔐 Configuration")
user_api_key = st.sidebar.text_input(
    "Enter Gemini API Key",
    type="password",
    placeholder="AIzaSy...",
    help="Provide your own Gemini API key."
)

if user_api_key:
    st.session_state["GOOGLE_API_KEY"] = user_api_key
else:
    st.session_state["GOOGLE_API_KEY"] = None
    st.sidebar.warning("⚠️ Please enter your API key to run the tools.")

# --- Define Your Pages (Updated to match your exact GitHub folders!) ---
pages = {
    "Welcome": [
        st.Page("main.py", title="Dashboard Home", icon="🏠")
    ],
    "My LLM Tools": [
        st.Page("ai-video-analyzer/app.py", title="YouTube Video Summarizer", icon="🎥"),
        st.Page("resume-analyzer/app.py", title="AI Resume Analyzer", icon="📄"),
    ]
}

pg = st.navigation(pages)
pg.run()

if pg.title == "Dashboard Home":
    st.title("Welcome to My LLM App Portfolio! 🚀")
    st.write("A unified hub hosting my generative AI utility applications.")
    st.markdown("""
    ---
    ### How to Get Started:
    1. Retrieve a free Gemini API key from [Google AI Studio](https://aistudio.google.com/).
    2. Paste it in the **Configuration** box on the left sidebar.
    3. Choose any application from the navigation sidebar and start analyzing!
    """)
