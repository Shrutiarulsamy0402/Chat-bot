import streamlit as st
import google.generativeai as genai
import os

# --- Configuration ---
# Set the page title and icon for a polished look
st.set_page_config(page_title="ChaatGPT", page_icon="🌶️")

# --- API Key and Persona ---
# It's highly recommended to use st.secrets for your API key when deploying
# For local development, you can place it here.
# Replace "YOUR_API_KEY" with your actual key.
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "YOUR_API_KEY" # Fallback for local testing

genai.configure(api_key=API_KEY)

# The same persona prompt as before
CHAAT_BOT_PERSONA = """
You are "ChaatGPT", a cheerful and enthusiastic AI expert on Indian street food, especially chaat.
Your personality is friendly, a little informal, and you love using food-related puns and metaphors.
Your knowledge is vast:
- You know recipes for all types of chaat from Pani Puri to Dahi Vada, from all regions of India.
- You know the history and origin of these dishes.
- You can suggest variations (e.g., healthier versions, vegan versions).
- You can suggest drink pairings (like masala chai, nimbu pani, or lassi).
- You must refuse to answer questions that are not related to food, especially Indian food. If asked about something else, politely steer the conversation back to chaat. For example: "That's interesting, but my mind is focused on a delicious bhel puri right now! Can I get you a recipe?"
- Keep your answers concise but flavorful.
"""

# --- Model Initialization ---
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- Session State Initialization ---
# This is the core of making the chatbot stateful
if "chat_session" not in st.session_state:
    # Start a new chat session with the persona
    st.session_state.chat_session = model.start_chat(history=[
        {'role': 'user', 'parts': [CHAAT_BOT_PERSONA]},
        # We add a pre-canned "model" response to kick things off
        {'role': 'model', 'parts': ["Namaste! I'm ChaatGPT, your personal guide to the wonderfully tangy and spicy world of Indian chaat! 🌶️ What delicious dish is on your mind today?"]}
    ])

# --- UI and Interaction ---

# Display the title
st.title("🌶️ ChaatGPT - Your AI Chaat Expert")

# Display chat history from session state
for message in st.session_state.chat_session.history:
    # Use Streamlit's chat_message to display messages with roles
    # We skip the initial persona prompt from being displayed
    if message.role == 'user' and CHAAT_BOT_PERSONA in message.parts[0].text:
        continue
    with st.chat_message(name=message.role, avatar="🧑‍🍳" if message.role == "model" else "🙂"):
        st.markdown(message.parts[0].text)

# Get user input using Streamlit's chat_input widget
user_prompt = st.chat_input("Ask me about chaat...")

if user_prompt:
    # Add user's message to the UI
    with st.chat_message("user", avatar="🙂"):
        st.markdown(user_prompt)

    # Send the message to the Gemini model and get a streaming response
    try:
        response = st.session_state.chat_session.send_message(user_prompt)
        
        # Display the model's response in the UI
        with st.chat_message("model", avatar="🧑‍🍳"):
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"An error occurred: {e}")

