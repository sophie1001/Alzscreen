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