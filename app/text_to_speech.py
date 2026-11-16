from gtts import gTTS
from io import BytesIO

def generate_speech(text, language="en"):
    """
    Convert AI response text into MP3 audio.
    Returns MP3 bytes.
    """

    if not text or not text.strip():
        return None

    try:
        audio_buffer = BytesIO()

        tts = gTTS(
            text=text,
            lang=language,
            slow=False
        )

        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return audio_buffer.getvalue()

    except Exception as error:
        print(f"TTS Error: {error}")
        return None
