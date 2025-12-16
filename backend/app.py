from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ✅ ADDED ROOT ROUTE (THIS FIXES 404)
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "message": "LeadHive backend is running 🚀"
    })

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    language = data.get("language", "english")

    if not user_msg:
        return jsonify({"reply": "Please type something."})

    system_prompt = f"""
    You are LeadHive AI assistant.
    Reply strictly in {language}.
    If language is telugu, reply in Telugu.
    If language is hindi, reply in Hindi.
    If language is english, reply in English.
    Help users only with LeadHive features, pricing, installation, and privacy.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ]
    )

    return jsonify({
        "reply": response.choices[0].message.content
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

