from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from google import genai

app = Flask(__name__)
CORS(app, origins=["*"])  # allow all origins

# 🔐 Secure API key from environment variable
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 🧠 Memory storage
chat_history = []

@app.route("/chat", methods=["POST"])
def chat():
    try:
        global chat_history

        data = request.get_json()
        user_message = data.get("message", "")

        # store user message
        chat_history.append({"role": "user", "text": user_message})

        # keep last 10 messages
        context = "\n".join(
            [f"{c['role']}: {c['text']}" for c in chat_history[-10:]]
        )

        # system prompt
        prompt = f"""
You are an AI Study Assistant.

RULES:
- Give short and simple answers
- Use bullet points when needed
- Avoid long theory unless asked
- Keep answers clean and readable

Chat History:
{context}

User Question:
{user_message}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        reply = response.text.strip()

        # store bot reply
        chat_history.append({"role": "assistant", "text": reply})

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})


# ✅ IMPORTANT for Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
