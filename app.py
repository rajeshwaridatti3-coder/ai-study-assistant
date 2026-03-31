from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

# 🔑 Your Gemini API Key
client = genai.Client(api_key="AIzaSyDgcG9Z5AaZanej5cUlmfdiH3BrNhOjw2I")

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

        # keep last 10 messages only
        context = "\n".join(
            [f"{c['role']}: {c['text']}" for c in chat_history[-10:]]
        )

        # 🧠 system prompt (controls AI behavior)
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

        # store bot response
        chat_history.append({"role": "assistant", "text": reply})

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)