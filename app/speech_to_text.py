import speech_recognition as sr
from io import BytesIO

def transcribe_audio(audio_bytes):
    """
    Convert recorded WAV audio into text.
    """
    recognizer = sr.Recognizer()

    try:
        audio_file = sr.AudioFile(BytesIO(audio_bytes))

        with audio_file as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(
            audio_data,
            language="en-IN"
        )

        return text

    except sr.UnknownValueError:
        return "ERROR: Could not understand the audio."

    except sr.RequestError as error:
        return f"ERROR: Speech recognition service unavailable: {error}"

    except Exception as error:
        return f"ERROR: {error}"
