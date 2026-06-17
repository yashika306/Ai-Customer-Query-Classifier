"""
Flask entry point. Serves the UI and exposes /classify as a JSON endpoint
that runs a customer message through the full LangGraph pipeline.

Run with:  python app.py
Then open: http://127.0.0.1:5000
"""

import os
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("GROQ_API_KEY"):
    print(
        "\n WARNING: GROQ_API_KEY is not set."
        "add your free key from https://console.groq.com/keys before running "
        "real classifications.\n"
    )

from graph import build_graph

app = Flask(__name__, static_folder="static")
pipeline = build_graph()


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json(force=True)
    message = (data or {}).get("message", "").strip()

    if not message:
        return jsonify({"error": "message is required"}), 400

    try:
        result = pipeline.invoke({"raw_input": message, "retry_count": 0})
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
