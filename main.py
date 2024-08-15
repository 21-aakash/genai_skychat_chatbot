import os
import time
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai


# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="SkyChat",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

# Get the Google API key from the environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to send a message with retry logic
def send_message_with_retry(user_prompt, max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            return model.chat(user_prompt)  # Directly use chat() method for response
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                raise e  # Raise the exception if all retries fail

# Display the chatbot's title on the page
st.title("👽 SkyChat 0.0.0")

# Input field for user's message
user_prompt = st.chat_input("Ask SkyChat something...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    
    # Send user's message to Gemini-Pro with retry logic and get the response
    with st.spinner('Wait for it...'):
        try:
            gemini_response = send_message_with_retry(user_prompt)
        except Exception as e:
            st.error(f"Failed to get a response: {e}")
        else:
            # Display Gemini-Pro's response
            with st.chat_message("assistant"):
                st.markdown(gemini_response.text)
