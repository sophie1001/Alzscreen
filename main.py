import streamlit as st
AUDIO_FILE_NAME = "uploaded_audio.wav"
st.title('Alzscreen')
# upload the audio file
audio_file = st.file_uploader("Upload an audio file", type = ["wav", "mp3"], help = "Upload the audio file of the patient.")

if audio_file:
    # Save the uploaded file
    with open(AUDIO_FILE_NAME, "wb") as f:
        f.write(audio_file.getbuffer())
        st.toast("Audio Reading Successful", icon = "✔")

# Function to convert the audio waveform to spectrogram
def audio_to_spectrogram(y, sr):
    # Generate a spectrogram
    spectrogram = librosa.feature.melspectrogram(y = y, sr = sr)

    # Convert to decibels
    log_spectrogram = librosa.power_to_db(spectrogram, ref=np.max)

    # Plot the spectrogram
    plt.figure(figsize=(10, 6))
    plt.axis('off')
    librosa.display.specshow(log_spectrogram, sr=sr)

    # Save the spectrogram if a save_path is provided
    plt.tight_layout()
    plt.savefig("test.png")
    plt.show()
    
y, sr = librosa.load(audio_path)
audio_to_spectrogram(y, sr)
spectrogram = "test.png"