import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import requests
import base64
import streamlit as st
import uuid  # For generating unique file names

# Default image name
IMAGE_NAME = "spectrogram.png"
MAIN_LABELS = ["Alzheimer's Disease", "Cognitive Normal"]
URL = "https://askai.aiclub.world/8badc90c-cbba-456c-aaf2-a1593c356f9b"

# Function to convert the audio waveform to a spectrogram
def audio_to_spectrogram(audio_file_path: str):
    try:
        # Load the audio file
        y, sr = librosa.load(audio_file_path)
        
        # Generate a spectrogram
        spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
        
        # Convert to decibels
        log_spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
        
        # Generate a unique file name for each spectrogram
        unique_image_name = f"spectrogram_{uuid.uuid4()}.png"
        
        # Plot the spectrogram and save it as an image
        plt.figure(figsize=(10, 6))
        plt.axis('off')
        librosa.display.specshow(log_spectrogram, sr=sr)
        plt.tight_layout()
        plt.savefig(unique_image_name)
        plt.close()
        
        return unique_image_name  # Return the unique image name
    except Exception as error:
        print(f"Error generating spectrogram: {str(error)}")
        return None

# Function to convert the spectrogram image to base64 for API request
def image_to_convert(image_path: str):
    try:
        with open(image_path, "rb") as image:
            payload = base64.b64encode(image.read())
            return payload
    except Exception as error:
        print(f"Error converting image to base64: {str(error)}")
        return None

# Function to send the spectrogram to the API and get the prediction
def get_prediction(image_data):
    try:
        r = requests.post(URL, data=image_data)
        if r.status_code == 200:
            response = r.json().get('predicted_label')
            if response is not None:
                label = MAIN_LABELS[int(response)]
                return label
            else:
                return "Unknown"
        else:
            print(f"API request failed with status code {r.status_code}")
            return "Error"
    except Exception as error:
        print(f"Error during prediction request: {str(error)}")
        return "Error"
