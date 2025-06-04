import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import requests
import json

load_dotenv()
app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message")
        print("🧠 Prompt received:", user_input)

        if not user_input:
            return jsonify(content="⚠️ Please enter a valid prompt.")

        # ✅ Use v1beta endpoint (supported by free Gemini key)
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

        headers = {"Content-Type": "application/json"}
        params = {"key": GEMINI_API_KEY}
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": user_input}
                    ]
                }
            ]
        }

        response = requests.post(url, headers=headers, params=params, json=data)
        result = response.json()

        import json
        print("📦 Gemini Raw Response:\n", json.dumps(result, indent=2))

        if "candidates" in result and len(result["candidates"]) > 0:
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
            print("✅ Gemini reply:", reply)
            return jsonify(content=reply)
        elif "error" in result:
            error_msg = result["error"].get("message", "Unknown error.")
            print("❌ Gemini API error:", error_msg)
            return jsonify(content=f"❌ Gemini error: {error_msg}")
        else:
            return jsonify(content="⚠️ Gemini API returned an unexpected format.")

    except Exception as e:
        print("❌ Python Error:", e)
        return jsonify(content=f"❌ An error occurred: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
