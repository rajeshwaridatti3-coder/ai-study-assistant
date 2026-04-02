from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app, origins=["*"])

# 🔐 Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

# 🧠 Chat memory
chat_history = []

@app.route("/chat", methods=["POST"])
def chat():
    global chat_history

    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message.strip():
            return jsonify({"reply": "⚠️ Please enter a message"})

        # Store user message
        chat_history.append(f"User: {user_message}")

        # Keep last 10 messages
        context = "\n".join(chat_history[-10:])

        # Prompt
        prompt = f"""
You are an AI Study Assistant.

RULES:
- Give short and simple answers
- Use bullet points if needed
- Avoid long paragraphs

Chat History:
{context}

User:
{user_message}
"""

        # Generate response
        response = model.generate_content(prompt)

        reply = response.text if response.text else "⚠️ No response from AI"

        # Store AI reply
        chat_history.append(f"AI: {reply}")

        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", str(e))  # for Render logs
        return jsonify({"reply": f"Error: {str(e)}"})


# ✅ IMPORTANT FOR RENDER (PORT FIX)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
