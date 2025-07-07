# Internal_Modules/_Gemini_Handler.py

import os
import google.generativeai as genai
from dotenv import load_dotenv
from _logging_setup import setup_logging

logger = setup_logging()

# We will only configure the API key at startup.
# The model itself will be loaded on the first use.
model = None

def setup():
    """Initializes the Gemini Handler module by loading and configuring the API key."""
    # Load environment variables from the project's .env file
    load_dotenv()

    api_key = os.getenv('Gemini_API')

    if not api_key:
        logger.critical("Gemini API Key ('Gemini_API') was not found in the .env file.")
        return

    try:
        genai.configure(api_key=api_key)
        logger.info("Gemini module setup complete. API key configured.")
    except Exception as e:
        logger.error(f"Failed to configure Gemini API key: {e}")

async def get_or_create_model():
    """
    A helper function to get the existing model or create it if it doesn't exist.
    This is known as 'lazy initialization'.
    """
    global model
    if model is None:
        try:
            logger.info("Initializing Gemini model for the first time...")
            model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("Gemini model 'gemini-1.5-flash' has been initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model on first use: {e}")
            return None
    return model

async def ask_gemini(prompt: str) -> str:
    """Sends a prompt to the Gemini API and returns the response."""
    
    # Get the model, creating it if it's the first time.
    active_model = await get_or_create_model()

    if not active_model:
        return "Error: The Gemini model could not be initialized. Please check the server logs."

    try:
        # Generate content using the asynchronous API
        response = await active_model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        logger.error(f"An error occurred while communicating with the Gemini API: {e}")
        return "Sorry, an error occurred while processing your request."