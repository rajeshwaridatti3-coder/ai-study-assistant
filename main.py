from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# ✅ FIX: stable config
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY"),
    transport="rest"
)

# ✅ FIXED MODEL (stable)
model = genai.GenerativeModel("gemini-1.5-flash")

chat_history = []

@app.route("/chat", methods=["POST"])
def chat():
    global chat_history

    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message.strip():
            return jsonify({"reply": "Please enter a message"})

        chat_history.append(f"User: {user_message}")
        context = "\n".join(chat_history[-10:])

        prompt = f"""
You are an AI Study Assistant.
Keep answers short and simple.

Chat:
{context}

User: {user_message}
"""

        response = model.generate_content(prompt)

        reply = response.text if response else "No response"

        chat_history.append(f"AI: {reply}")

        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"reply": f"Error: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
