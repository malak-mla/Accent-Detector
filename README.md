
# 🌍 English Accent Analyzer

A tool to evaluate spoken English proficiency by analyzing accent characteristics.

## Features
- Accepts any public video URL (YouTube, Loom, direct MP4)
- Extracts audio from video
- Transcribes speech using OpenAI Whisper
- Classifies English accents with confidence scores
- Provides detailed analysis report


## Setup
```bash
python -m venv detectenv
source detectenv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## File Structure
- `app.py`: Main Streamlit UI
- `config.py`: Configuration settings
- `downloader.py`: Downloads models
- `utils/`: Contains transcription and classification modules
- `models/`: Model storage