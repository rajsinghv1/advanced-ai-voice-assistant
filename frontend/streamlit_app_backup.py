import sys
import uuid
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import requests

from app.speech_to_text import transcribe_audio
from app.text_to_speech import generate_speech

# ---------------- CONFIGURATION ----------------

st.set_page_config(
    page_title="Advanced AI Voice Assistant",
    page_icon="🎙️",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

# ---------------- SESSION STATE ----------------

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "speak_responses" not in st.session_state:
    st.session_state.speak_responses = True

# ---------------- HEADER ----------------

st.title("🎙️ Advanced AI Voice Assistant")
st.caption(
    "Powered by LangChain | Google Gemini | FastAPI | Streamlit"
)

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.header("⚙️ Assistant Settings")

    st.session_state.speak_responses = st.checkbox(
        "🔊 Enable AI Voice Output",
        value=st.session_state.speak_responses
    )

    st.divider()

    st.write("**LLM:** Google Gemini")
    st.write("**Framework:** LangChain")
    st.write("**Backend:** FastAPI")
    st.write("**Speech-to-Text:** Google")
    st.write("**Text-to-Speech:** gTTS")

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        try:
            response = requests.post(
                f"{API_URL}/clear-memory",
                json={"session_id": st.session_state.session_id},
                timeout=15
            )
            response.raise_for_status()

            st.session_state.messages = []
            st.success("Conversation and memory cleared.")
            st.rerun()

        except requests.exceptions.RequestException as error:
            st.error(f"Could not clear backend memory: {error}")

# ---------------- BACKEND ----------------

def ask_ai(message):

    response = requests.post(
        f"{API_URL}/chat",
        json={
            "message": message,
            "session_id": st.session_state.session_id
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()
    answer = data.get("response", data.get("answer", ""))

    if isinstance(answer, list):
        answer = " ".join(
            item.get("text", "")
            for item in answer
            if isinstance(item, dict)
        )

    if isinstance(answer, dict):
        answer = answer.get("text", str(answer))

    return str(answer) if answer else "No response received."

# ---------------- CHAT HISTORY ----------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- MESSAGE PROCESSING ----------------

def process_message(user_message):

    if not user_message.strip():
        return

    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):

        with st.spinner("🤖 Gemini is thinking..."):

            try:
                answer = ask_ai(user_message)

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                if st.session_state.speak_responses:

                    with st.spinner("🔊 Generating AI voice..."):
                        audio_bytes = generate_speech(answer)

                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/mp3")
                    else:
                        st.warning("Could not generate voice output.")

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to FastAPI backend.")

            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again.")

            except requests.exceptions.HTTPError as error:
                st.error(f"Backend HTTP error: {error}")

            except Exception as error:
                st.error(f"Something went wrong: {error}")

# ---------------- TEXT INPUT ----------------

st.divider()
st.subheader("💬 Chat with AI")

user_input = st.chat_input("Ask your AI assistant anything...")

if user_input:
    process_message(user_input)

# ---------------- MICROPHONE INPUT ----------------

st.divider()
st.subheader("🎙️ Talk to Your AI Assistant")

audio_value = st.audio_input(
    "Record your voice",
    sample_rate=16000
)

if audio_value is not None:

    if st.button("🚀 Convert Voice & Ask AI", type="primary"):

        with st.spinner("🎧 Converting speech to text..."):

            recognized_text = transcribe_audio(
                audio_value.getvalue()
            )

        if recognized_text.startswith("ERROR:"):
            st.error(recognized_text)

        else:
            st.success("Speech converted successfully!")
            st.write("**Recognized text:**", recognized_text)

            process_message(recognized_text)

# ---------------- FOOTER ----------------

st.divider()
st.caption(
    "🚀 Advanced AI Voice Assistant | LangChain + Gemini + STT + TTS"
)
