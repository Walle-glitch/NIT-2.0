# Internal_Modules/_Gemini_Handler.py

import os
import google.generativeai as genai
from dotenv import load_dotenv
from ._logging_setup import setup_logging

logger = setup_logging()

# --- NEW SETUP FUNCTION ---
def setup():
    """Initializes the Gemini Handler module by loading the API key and model."""
    global model
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Use the specific key name you created: 'Gemini_API'
    api_key = os.getenv('Gemini_API')
    
    if not api_key:
        logger.critical("Gemini API Key ('Gemini_API') not found in .env file.")
        model = None
        return

    try:
        genai.configure(api_key=api_key)
        # Initialize the generative model
        model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("Gemini module setup complete and model 'gemini-1.5-flash' initialized.")
    except Exception as e:
        logger.error(f"Failed to configure or initialize Gemini model: {e}")
        model = None

# This will be initialized by the setup() function
model = None

async def ask_gemini(prompt: str) -> str:
    """Sends a prompt to the Gemini API and returns the response."""
    if not model:
        return "Error: The Gemini model is not initialized. Please check the API key and server logs."

    try:
        # Generate content using the asynchronous API
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        logger.error(f"An error occurred while communicating with the Gemini API: {e}")
        return f"Sorry, an error occurred while processing your request."