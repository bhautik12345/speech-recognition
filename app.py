import streamlit as st
import io
import os
from groq import Client

os.environ['LANGCHAIN_API_KEY'] = st.secrets['LANGCHAIN_API_KEY']
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = 'Speech-Recognition'

languages = {
    "Afrikaans": "af",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Belarusian": "be",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Chinese": "zh",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Estonian": "et",
    "Finnish": "fi",
    "French": "fr",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Korean": "ko",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Macedonian": "mk",
    "Malay": "ms",
    "Marathi": "mr",
    "Maori": "mi",
    "Mongolian": "mn",
    "Nepali": "ne",
    "Norwegian": "no",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Romanian": "ro",
    "Russian": "ru",
    "Serbian": "sr",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Spanish": "es",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tagalog": "tl",
    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy"
}

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="🎙️ Speech Recognition",
    page_icon="🎧",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---- CUSTOM CSS ----
st.markdown("""
    <style>
        .main {
            background-color: #f4f6f8;
        }
        
        .block-container {
            padding-top: 2rem;
        }
        .stAudio {
            margin-bottom: 20px;
        }
        .stButton>button {
            background-color: #4a90e2;
            color: white;
            font-weight: bold;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.title("🎙️ AI Speech Recognition")
st.caption("Effortlessly transcribe audio in multiple languages with Whisper")

# ---- SIDEBAR ----
st.sidebar.title("⚙️ Settings")
groq_api_key = st.sidebar.text_input('🔐 Enter Your Groq API Key', type='password')
select_language = st.sidebar.selectbox(
    label="Select Language",
    index=None,
    placeholder='🌐 Choose Language...',
    options=list(languages.keys()),
    label_visibility='collapsed'
)

# ---- INPUT AREA ----
st.subheader("📥 Upload or Record Audio")
st.markdown("Record directly or upload an audio file to get started.")

st.markdown("#### 🎤 Record Audio")
audio_file = st.audio_input("Record your audio", label_visibility='collapsed')

st.markdown(---)

with st.expander("📁 Upload an Audio File"):
    uploaded_file = st.file_uploader(
        "Choose File",
        type=['flac', 'mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'ogg', 'wav', 'webm'],
        accept_multiple_files=False
    )


# ---- MAIN LOGIC ----
client = Client(api_key=groq_api_key)

if groq_api_key and select_language:
    if audio_file:
        st.spinner("Transcribing recorded audio...")
            audio_bytes = audio_file.getvalue()
            response = client.audio.transcriptions.create(
                file=('recorded_audio.wav', io.BytesIO(audio_bytes)),
                model='whisper-large-v3',
                response_format='text',
                language=languages[select_language]
            )
            st.success("📝 Transcription Complete")
            st.write(response)

    elif uploaded_file:
        st.spinner("Transcribing uploaded audio file...")
            audio_bytes = uploaded_file.read()
            response = client.audio.transcriptions.create(
                file=(uploaded_file.name, audio_bytes),
                model='whisper-large-v3',
                response_format='text',
                language=languages[select_language]
            )
            st.success("📝 Transcription Complete")
            st.write(response)

    else:
        st.warning("Please record or upload an audio file to continue.")
else:
    st.error("Please enter your API key and select a language.")
