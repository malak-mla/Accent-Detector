# Accent Detector

This app transcribes speech and classifies the speaker's accent using Whisper and SpeechBrain.

## Setup
```bash
python -m venv accentenv
source accentenv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## File Structure
- `app.py`: Main Streamlit UI
- `config.py`: Configuration settings
- `downloader.py`: Downloads models
- `utils/`: Contains transcription and classification modules
- `models/`: Model storage