import streamlit as st
st.title('Alzscreen')
# upload the audio file
audio_file = st.file_uploader("Upload an audio file", type = ["wav", "mp3"], help = "Upload the audio file of the patient.")