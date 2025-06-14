# downloader.py
import os
import torchaudio
import zipfile
import requests
from config import SPEECHBRAIN_MODEL_URL, SPEECHBRAIN_MODEL_DIR


def download_models():
    os.makedirs(SPEECHBRAIN_MODEL_DIR, exist_ok=True)
    brain_file = os.path.join(SPEECHBRAIN_MODEL_DIR, "brain.tar.gz")
    if not os.path.exists(brain_file):
        print("Downloading SpeechBrain model...")
        r = requests.get(SPEECHBRAIN_MODEL_URL, stream=True)
        with open(brain_file, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        torchaudio.utils.extract_archive(brain_file, out_path=SPEECHBRAIN_MODEL_DIR)
