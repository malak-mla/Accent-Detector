# utils/classifier.py
import torchaudio
from speechbrain.pretrained import EncoderClassifier
from config import SPEECHBRAIN_MODEL_DIR

classifier = EncoderClassifier.from_hparams(source=SPEECHBRAIN_MODEL_DIR)

def classify_accent(audio_path):
    signal, fs = torchaudio.load(audio_path)
    prediction = classifier.classify_file(audio_path)
    return prediction[3][0]  # Returns the top predicted label
