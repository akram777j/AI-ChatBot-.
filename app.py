from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# ضع مفتاح OpenAI هنا
client = OpenAI(api_key="اشاشاشاشااشا")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=user_message
        )

        reply = response.output_text
        return jsonify({"reply": reply})

    except Exception as e:
        print("OPENAI ERROR:", e)
        return jsonify({"reply": str(e)}), 500


if __name__ == "__main__":
   import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

