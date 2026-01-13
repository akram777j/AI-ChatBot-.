from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# إنشاء عميل OpenAI بالطريقة الجديدة
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/", methods=["GET"])
def home():
    return "AI ChatBot backend is running"

@app.route("/chat", methods=["POST", "OPTIONS"])
@cross_origin()
def chat():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"reply": "No message received"}), 400

    user_message = data["message"]

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=user_message
        )

        reply = response.output_text
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
