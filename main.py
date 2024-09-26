from utils import audio_to_spectrogram, image_to_convert, get_prediction
import streamlit as st
from utils import IMAGE_NAME

AUDIO_FILE_NAME = "uploaded_audio.wav"
st.title('Alzscreen')
# upload the audio file
# Initialize session state for storing history
if 'history' not in st.session_state:
    st.session_state.history = []

# Define usernames and passwords
user_data = {
    "sophie": "12345",
    "user2": "password2",
    "admin": "adminpass"
}

# Create a login function
def login(username, password):
    if username in user_data and user_data[username] == password:
        return True
    return False

# Streamlit login UI
def login_page():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if login(username, password):
            st.success(f"Welcome {username}!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
        else:
            st.error("Invalid username or password")

# Create a main app function
def main_app():
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

        base64_string = image_to_convert(IMAGE_NAME)
        predicted_label = get_prediction(base64_string)
        print(predicted_label)

                # Save the current spectrogram and prediction in session state history
        st.session_state.history.append((IMAGE_NAME, predicted_label))

        # Limit the history to the last two entries
        if len(st.session_state.history) > 2:
            st.session_state.history = st.session_state.history[-2:]

        st.subheader("Condition: {}".format(predicted_label))
        # Display the history of spectrograms and predictions
        st.header("Prediction History")
        for idx, (spec_image, label) in enumerate(reversed(st.session_state.history)):
            st.subheader(f"Prediction {idx+1}")
            st.image(spec_image, caption=f"Condition: {label}")
# Main Streamlit app flow
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    login_page()