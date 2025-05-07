import streamlit as st
import io
import os
from groq import Client

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

st.set_page_config(page_title='Speech Recognition')
st.title('Speech Recognition')
st.subheader("Let's Play With Audio")

st.sidebar.title('Settings')
groq_api_key = st.sidebar.text_input('Put Your Groq API key',type='password')
select_language = st.sidebar.selectbox(label="language",index=None,placeholder='Select Language..',options=list(languages.keys()),label_visibility='collapsed')

audio_file = st.audio_input('Records',label_visibility='collapsed')
uploaded_file = st.file_uploader('Choose An Audio file From Browse',type=['flac', 'mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'ogg', 'wav', 'webm'],accept_multiple_files=False)

client = Client(api_key=groq_api_key)

if groq_api_key and select_language:
    if audio_file:
        st.audio(audio_file)

        audio_bytes = audio_file.getvalue()

        response = client.audio.transcriptions.create(
            file=('recorded_audio.wav',io.BytesIO(audio_bytes)),
            model='whisper-large-v3',
            response_format='text',
            language=languages[select_language]
        )

        st.write(response)

    elif uploaded_file:
        audio_bytes = uploaded_file.read()

        response = client.audio.transcriptions.create(
            file=(uploaded_file.name,audio_bytes),
            model='whisper-large-v3',
            response_format='text',
            language=languages[select_language]
        )
        st.write(response)

else:
    st.error('Please Provide All The Information')
        

