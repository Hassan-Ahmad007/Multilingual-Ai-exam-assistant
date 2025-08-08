# Import necessary libraries
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from translate import Translator
import os
from dotenv import load_dotenv
import time
import re
import base64
import requests

# Load environment variables from .env file (like GEMINI_API_KEY)
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit request size to 16 MB

# Configure Gemini API with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel(
    "gemini-1.5-flash",  # Model name
    generation_config={
        "temperature": 0.9,         # Creativity level (higher = more creative)
        "max_output_tokens": 2048   # Max words/tokens in the response
    }
)

# ElevenLabs API key for text-to-speech
ELEVENLABS_API_KEY = 'sk_87b20b619fb87a0890d68f6f483cb72aa81938694ee28e50'

# Supported languages and their voice options
SUPPORTED_LANGUAGES = {
    "en": {"name": "English", "voice": ["Samantha", "Karen"]},
    "ur": {"name": "Urdu", "voice": ["Zeina", "Laila"]},
    "ar": {"name": "Arabic", "voice": ["Amira", "Zeina"]},
    "tr": {"name": "Turkish", "voice": ["Yelda", "Filiz"]}
}

# Voice IDs for ElevenLabs API for Urdu, Arabic, Turkish
ELEVENLABS_VOICE_IDS = {
    "ar": "21m00Tcm4TlvDq8ikWAM",  # Arabic voice
    "ur": "EXAVITQu4vr4xnSDxMaL",  # Urdu voice
    "tr": "EXAVITQu4vr4xnSDxMaL"   # Turkish voice (reuse or test other)
}

# Utility function to clean AI response text
def clean_response(text):
    """Removes phrases like 'in English', 'translation:' from the end of the response"""
    text = re.sub(r'(this means|which means|in english|translation:).*?$', '', text, flags=re.IGNORECASE)
    return text.strip()

# API endpoint for Text-to-Speech using ElevenLabs
@app.route("/api/tts", methods=["POST"])
def tts():
    data = request.get_json()  # Get JSON data sent by frontend
    text = data.get("text")    # Extract text to convert
    lang = data.get("lang")    # Extract language for voice

    # Validate input
    if not text or not lang:
        return jsonify({"error": "Missing text or lang"}), 400

    # Get the voice ID for the selected language
    voice_id = ELEVENLABS_VOICE_IDS.get(lang)
    if not voice_id:
        return jsonify({"error": "Language not supported for TTS"}), 400

    # Prepare ElevenLabs API request
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    # Send request to ElevenLabs and handle response
    try:
        resp = requests.post(url, json=payload, headers=headers)
        resp.raise_for_status()  # Raise error if response not successful
        audio_data = resp.content  # Get audio binary data
        audio_base64 = base64.b64encode(audio_data).decode("utf-8")  # Convert to base64 for frontend
        return jsonify({"audio_base64": audio_base64})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Main route for the homepage
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Get question and target language from form data
            question = request.form.get("question", "").strip()
            target_language = request.form.get("language", "en")

            # Check if question is empty
            if not question:
                return jsonify({"error": "Please enter a question."})

            # Validate selected language
            if target_language not in SUPPORTED_LANGUAGES:
                return jsonify({"error": f"Unsupported language selected: {target_language}"})

            # Track start time for response duration
            start_time = time.time()

            # Prompt for Gemini to always respond in English
            prompt = (
                f"Answer this question in four lines. Respond in English regardless of the input language.\n"
                f"Question: {question}"
            )

            # Generate content using Gemini
            response = model.generate_content(prompt)

            # Check if response is empty
            if not response.text:
                raise ValueError("Empty response from AI")

            # Clean and strip unnecessary parts
            answer = clean_response(response.text.strip())

            # If target is not English, translate the answer
            if target_language != "en":
                translator = Translator(to_lang=target_language)
                answer = translator.translate(answer)

            # Limit answer length if too long
            if len(answer) > 500:
                answer = answer[:497] + "..."

            # Return response as JSON to frontend
            return jsonify({
                "answer": answer,
                "time": round(time.time() - start_time, 2),
                "language": target_language,
                "voice_options": SUPPORTED_LANGUAGES[target_language]["voice"]
            })

        # Handle any unexpected errors
        except Exception as e:
            return jsonify({"error": str(e)})

    # Render the HTML page on GET request
    return render_template("index.html")

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True, threaded=True)  # threaded=True allows handling multiple users
