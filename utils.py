import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import requests
import base64
import streamlit as st
IMAGE_NAME = "spectogram.png"
MAIN_LABELS = ["Alzheimer's Disease", "Cognitive Normal"]

# Function to convert the audio waveform to spectrogram
def audio_to_spectrogram(audio_file_path: str):
    try:
        # Load the audio file
        y, sr = librosa.load(audio_file_path)
        # Generate a spectrogram
        spectrogram = librosa.feature.melspectrogram(y = y, sr = sr)
        # Convert to decibels
        log_spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
        # Plot the spectrogram
        plt.figure(figsize=(10, 6))
        plt.axis('off')
        librosa.display.specshow(log_spectrogram, sr=sr)
        plt.tight_layout()
        plt.savefig(IMAGE_NAME)
        plt.close()
        return True
    except Exception as error:
        print(str(error))
        return False
        
def image_to_convert(image_path:str):
    with open(image_path, "rb") as image:
        payload = base64.b64encode(image.read())
        return payload

def get_prediction(image_data):
    r = requests.post(URL, data=image_data)
    response = r.json()['predicted_label']
    # ['predicted_label']
    print(response)
    label = MAIN_LABELS[int(response)]
    return label