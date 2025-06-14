# app.py
import streamlit as st
from utils.transcriber import transcribe_audio
from utils.classifier import classify_accent
from downloader import download_models
import os
import tempfile

st.title("Accent Detection App")

# Download necessary models
with st.spinner("Setting up models..."):
    download_models()

uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.audio(tmp_path)

    st.write("Transcribing...")
    transcription = transcribe_audio(tmp_path)
    st.text_area("Transcription", transcription)

    st.write("Detecting Accent...")
    accent = classify_accent(tmp_path)
    st.success(f"Predicted Accent: {accent}")