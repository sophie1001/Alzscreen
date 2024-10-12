from utils import audio_to_spectrogram, image_to_convert, get_prediction
import streamlit as st
from PIL import Image

# Constants
AUDIO_FILE_NAME = "uploaded_audio.wav"

# # Streamlit App Title
# st.title('Alzscreen')
# Streamlit App Title (Center-Aligned)
st.markdown("<h1 style='text-align: center;'>Alzscreen</h1>", unsafe_allow_html=True)

# Initialize session state for storing history
if 'history' not in st.session_state:
    st.session_state.history = []
if 'i' not in st.session_state:
    st.session_state.i = 0

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

# Main app function to upload, process audio, and display results
def main_app():
    # Display the image from the images 
    folder image = Image.open('ALZSCREEN.png') 

    # Using relative path 
    st.image(image, caption='logo', use_column_width=True)
    # File uploader to upload an audio file
    audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"], help="Upload the audio file of the patient.")
    
    if audio_file:
        # Save the uploaded audio file to local storage
        with open(AUDIO_FILE_NAME, "wb") as f:
            f.write(audio_file.getbuffer())
            st.toast("Audio Reading Successful", icon="✔")
        
        # Generate the spectrogram from the uploaded audio
        unique_image_name = audio_to_spectrogram(AUDIO_FILE_NAME)
        if not unique_image_name:
            st.error("Spectrogram Saving Failed", icon="X")
        else:
            st.toast("Spectrogram Saving Successful", icon="✔")
            
            # Display the audio file and the generated spectrogram
            with st.sidebar:
                st.title("Alzheimer's Detection")
                
                # Display the uploaded audio
                st.header("Uploaded Audio")
                st.audio(AUDIO_FILE_NAME)
                
                # Display the spectrogram image
                st.header("Generated Spectrogram")
                st.image(unique_image_name)
            
            # Convert the spectrogram image to base64 for API prediction
            base64_string = image_to_convert(unique_image_name)
            if base64_string:
                # Get the prediction from the API
                predicted_label = get_prediction(base64_string)
                st.subheader(f"Condition: {predicted_label}")
                
                # Save the current spectrogram and prediction in session state history
                st.session_state.i += 1
                st.session_state.history.append((unique_image_name, predicted_label))

                # Limit the history to the last two entries
                if len(st.session_state.history) > 2:
                    st.session_state.history = st.session_state.history[-2:]
                
                # Display prediction history in two columns
                st.header("Prediction History")
                if st.session_state.history:
                    cols = st.columns(len(st.session_state.history))
                    for idx, (spec_image, label) in enumerate(st.session_state.history):
                        with cols[idx]:
                            st.image(spec_image, caption=f"Prediction {idx+1}")
                            st.text(f"Condition: {label}")
            else:
                st.error("Error in converting the spectrogram image to base64.")
    else:
        st.warning("Please upload an audio file to proceed.")

# Main Streamlit app flow
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    login_page()