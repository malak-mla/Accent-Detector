# accent_detector/utils/classifier.py
import torch
import torchaudio
from speechbrain.pretrained import EncoderClassifier
import numpy as np

# Accent mapping
ACCENT_MAP = {
    "us": "American",
    "england": "British",
    "australia": "Australian",
    "canada": "Canadian",
    "indian": "Indian",
    "african": "African"
}

# Load model without Streamlit dependency
classifier = None

def load_classification_model():
    global classifier
    if classifier is None:
        classifier = EncoderClassifier.from_hparams(
            source="speechbrain/lang-id-commonlanguage_ecapa",
            savedir="pretrained_models/lang-id-commonlanguage_ecapa"
        )
    return classifier

def classify_accent(audio_path):
    classifier = load_classification_model()
    
    # Classify the audio file
    out_prob, score, index, text_lab = classifier.classify_file(audio_path)
    
    # Get top prediction
    top_label = text_lab[0]
    top_score = torch.softmax(out_prob, dim=1)[0, index[0]].item()
    
    # Get all scores
    probabilities = torch.softmax(out_prob, dim=1).squeeze()
    all_scores = {}
    
    for i, label in enumerate(text_lab):
        label_str = label.replace('language:', '')
        human_label = ACCENT_MAP.get(label_str.lower(), label_str.title())
        all_scores[human_label] = probabilities[i].item()
    
    # Normalize confidence score (0-100%)
    confidence = min(100, max(0, top_score * 100))
    
    # Get human-readable accent label
    accent_label = ACCENT_MAP.get(top_label.replace('language:', '').lower(), "Unknown")
    
    return {
        "accent": accent_label,
        "confidence": confidence,
        "all_scores": all_scores
    }