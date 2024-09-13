from utils import audio_to_spectrogram, IMAGE_NAME

AUDIO_FILE_NAME = "uploaded_audio.wav"
st.title('Alzscreen')
# upload the audio file
audio_file = st.file_uploader("Upload an audio file", type = ["wav", "mp3"], help = "Upload the audio file of the patient.")

if audio_file:
    # Save the uploaded file
    with open(AUDIO_FILE_NAME, "wb") as f:
        f.write(audio_file.getbuffer())
        st.toast("Audio Reading Successful", icon = "✔")

    # generate the spectorgram
    spec_results = audio_to_spectrogram(AUDIO_FILE_NAME)
    if not spec_results:
        st.error("Spectrogram Saving Failed", icon = "X")
    else:
        st.toast("Spectrogram Saving Successful", icon = "✔")
        # display the audio and spectorgram
        with st.sidebar:
            st.title("Alzheimer's Detection")
            # display the audio
            st.header("Uploaded Audio")
            st.audio(AUDIO_FILE_NAME)
            # display the spectorgram
            st.header("Generated Spectrogram")
            st.image(IMAGE_NAME)
    