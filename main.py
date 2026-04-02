from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)

# ✅ CORS FIX (safe for frontend + Render)
CORS(app)

# ✅ Gemini API setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ FIXED MODEL (most stable)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# 🧠 Chat memory
chat_history = []

@app.route("/chat", methods=["POST"])
def chat():
    global chat_history

    try:
        data = request.get_json()

        if not data:
            return jsonify({"reply": "Invalid request"}), 400

        user_message = data.get("message", "")

        if not user_message.strip():
            return jsonify({"reply": "Please enter a message"}), 400

        # Store user message
        chat_history.append(f"User: {user_message}")

        # Keep last 10 messages only
        context = "\n".join(chat_history[-10:])

        prompt = f"""
You are an AI Study Assistant.

Rules:
- Give short and simple answers
- Use bullet points if needed
- Avoid long paragraphs

Chat History:
{context}

User:
{user_message}
"""

        response = model.generate_content(prompt)

        reply = response.text if response and response.text else "No response from AI"

        chat_history.append(f"AI: {reply}")

        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"reply": f"Server Error: {str(e)}"}), 500


# ✅ Render PORT FIX (VERY IMPORTANT)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
