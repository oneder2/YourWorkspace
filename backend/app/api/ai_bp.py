# /your_project_root/app/api/ai_bp.py
# Blueprint for AI integration related API endpoints.

import os
from flask import Blueprint, jsonify, request, current_app
# Import necessary components later (e.g., external API clients, JWT decorator)
# import openai # Example using OpenAI library
# from flask_jwt_extended import jwt_required

# Create a Blueprint instance named 'ai'
ai_bp = Blueprint('ai', __name__)

# --- AI Integration Routes ---

@ai_bp.route('/ping', methods=['GET'])
def ping_ai():
    """Simple test route."""
    return jsonify({"message": "AI API is alive!"}), 200


@ai_bp.route('/generate-text', methods=['POST'])
#@jwt_required() # Protect this route if AI usage is user-specific or metered
def generate_text():
    """
    Endpoint to interact with an external AI text generation service (e.g., OpenAI GPT).
    Expects JSON data: {'prompt': '...'}
    Handles API key securely from server configuration.
    """
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "Missing required field (prompt)"}), 400

    # --- Add logic to call the external AI API ---
    # Securely get API key from environment variables / app config
    # api_key = current_app.config.get('OPENAI_API_KEY') or os.environ.get('OPENAI_API_KEY')
    # if not api_key:
    #     current_app.logger.error("AI API Key not configured.")
    #     return jsonify({"error": "AI service not configured"}), 503 # Service Unavailable

    # Example using OpenAI library (install with `pip install openai`)
    # try:
    #     openai.api_key = api_key
    #     response = openai.Completion.create(
    #         engine="text-davinci-003", # Or another suitable model
    #         prompt=prompt,
    #         max_tokens=150 # Adjust as needed
    #     )
    #     generated_text = response.choices[0].text.strip()
    #     return jsonify({"generated_text": generated_text}), 200
    # except openai.error.AuthenticationError:
    #      current_app.logger.error("AI API Authentication Error.")
    #      return jsonify({"error": "AI service authentication failed"}), 500
    # except Exception as e:
    #     current_app.logger.error(f"Error calling AI API: {e}", exc_info=True)
    #     return jsonify({"error": "Failed to generate text from AI service"}), 500

    # Placeholder response:
    current_app.logger.info(f"Received AI prompt: {prompt}") # Use Flask's logger
    api_key = current_app.config.get('OPENAI_API_KEY') or os.environ.get('OPENAI_API_KEY')
    if not api_key:
         current_app.logger.warning("Placeholder AI: OPENAI_API_KEY not found in config.")
         # Don't expose the lack of key in the actual response if possible
         # return jsonify({"error": "AI service not configured"}), 503

    # Simulate a response
    generated_text = f"Placeholder response for prompt: '{prompt[:50]}...'"
    return jsonify({"generated_text": generated_text}), 200

# Add other AI-related endpoints as needed
# e.g., image generation, translation, summarization, etc.
# @ai_bp.route('/summarize', methods=['POST'])
# @jwt_required()
# def summarize_text():
#     data = request.get_json()
#     text_to_summarize = data.get('text')
#     # ... call summarization API ...
#     pass
