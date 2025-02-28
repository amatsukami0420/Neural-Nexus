import streamlit as st
import speech_recognition as sr
from pathlib import Path
import logging
import os
from utils.api_handler import GeminiHandler, WeatherHandler
from utils.context_manager import ConversationManager
from config import (
    GEMINI_API_KEY, 
    WEATHER_API_KEY, 
    ALLOWED_FILE_TYPES,
    TEMP_UPLOAD_DIR
)
import asyncio
from concurrent.futures import ThreadPoolExecutor
import tempfile
import wave
import numpy as np

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_manager" not in st.session_state:
        st.session_state.conversation_manager = ConversationManager()

def handle_file_upload(uploaded_file):
    if uploaded_file:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                return tmp_file.name
        except Exception as e:
            logger.error(f"File upload error: {str(e)}")
            st.error("Error processing the uploaded file")
    return None

def handle_voice_input():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("Listening... Speak now.")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=5, phrase_time_limit=15)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                with wave.open(tmp_file.name, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(44100)
                    wf.writeframes(audio.get_wav_data())
                
            text = r.recognize_google(audio)
            return text, tmp_file.name
    except Exception as e:
        logger.error(f"Voice input error: {str(e)}")
        st.error("Error processing voice input")
    return None, None

async def process_message(user_input: str, file_path: str, gemini_handler: GeminiHandler, weather_handler: WeatherHandler):
    try:
        context = st.session_state.conversation_manager.get_context()
        
        # Check for weather-related queries
        if any(word in user_input.lower() for word in ['weather', 'temperature', 'forecast']):
            response = weather_handler.get_weather_info(user_input)
        else:
            response = await gemini_handler.generate_response(user_input, file_path, context)
            
        if not response:  # Fallback to Gemini if weather handler fails
            response = await gemini_handler.generate_response(user_input, file_path, context)
            
        return response
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return f"An error occurred: {str(e)}"

def validate_api_keys():
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in .env file")
    if not WEATHER_API_KEY:
        raise ValueError("WEATHER_API_KEY is not set in .env file")

def main():
    # Add custom CSS for chat UI
    st.markdown("""
        <style>
        .stTextInput > div > div > input {
            border-color: #28a745 !important;
        }
        .stTextInput > div > div > input:focus {
            box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25) !important;
        }
        div.stChatMessage {
            border-color: #28a745 !important;
        }
        div.stChatMessage:hover {
            border-color: #218838 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("Multimodal AI Assistant")
    
    try:
        validate_api_keys()
    except ValueError as e:
        st.error(str(e))
        st.stop()
        return
        
    init_session_state()
    
    # Initialize API handlers
    gemini_handler = GeminiHandler(GEMINI_API_KEY)
    weather_handler = WeatherHandler(WEATHER_API_KEY)
    
    # Sidebar controls
    st.sidebar.title("Input Options")
    input_mode = st.sidebar.radio("Choose Input Mode", ["Text", "Voice", "File"])
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle different input modes
    user_input = None
    file_path = None
    
    if input_mode == "Text":
        user_input = st.chat_input("Type your message here...")
    elif input_mode == "Voice":
        if st.button("Start Voice Input"):
            user_input, file_path = handle_voice_input()
    else:  # File upload mode
        uploaded_file = st.file_uploader("Upload a file", type=ALLOWED_FILE_TYPES)
        if uploaded_file:
            file_path = handle_file_upload(uploaded_file)
            if file_path:
                user_input = "Please analyze this file and provide insights."

    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            if file_path and file_path.lower().endswith(('png', 'jpg', 'jpeg')):
                st.image(file_path)

        # Process input and generate response
        with st.spinner("Processing..."):
            try:
                response = asyncio.run(process_message(user_input, file_path, gemini_handler, weather_handler))
                
                # Update conversation context
                st.session_state.conversation_manager.add_to_context(user_input, response)
                
                # Display bot response
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(response)
                    
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                st.error("An error occurred while processing your request")

        # Cleanup temporary files
        if file_path and os.path.exists(file_path):
            os.unlink(file_path)

if __name__ == "__main__":
    main()
