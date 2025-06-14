

# accent_detector/utils/transcriber.py 
import whisper
import torch

# Load model without Streamlit dependency
model = None

def load_transcription_model():
    global model
    if model is None:
        model = whisper.load_model("base")
    return model

def transcribe_audio(audio_path):
    model = load_transcription_model()
    result = model.transcribe(audio_path)
    return result["text"]

