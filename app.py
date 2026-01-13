from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
import openai

app = Flask(__name__)

# تفعيل CORS لكل التطبيق
CORS(app)

# مفتاح OpenAI من Environment Variables
openai.api_key = os.environ.get("OPENAI_API_KEY")


# صفحة رئيسية (لتجنب 404)
@app.route("/", methods=["GET"])
def home():
    return "AI ChatBot backend is running"


# مسار الشات (يدعم POST + OPTIONS)
@app.route("/chat", methods=["POST", "OPTIONS"])
@cross_origin()
def chat():
    # التعامل مع طلب OPTIONS (CORS preflight)
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"reply": "No message received"}), 400

    user_message = data["message"]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": str(e)}), 500


# تشغيل السيرفر على Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
