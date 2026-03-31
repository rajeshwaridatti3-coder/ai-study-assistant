import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Create Flask app
app = Flask(__name__)
CORS(app)

# Load Gemini API key from environment variables (IMPORTANT for Railway/Render)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Home route (for checking backend is live)
@app.route("/")
def home():
    return "AI Backend is running successfully 🚀"

# Chat route (frontend will call this)
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")

        if not user_message:
            return jsonify({"reply": "No message received"}), 400

        response = model.generate_content(user_message)

        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"reply": str(e)}), 500


# Run app (IMPORTANT for deployment)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
   
