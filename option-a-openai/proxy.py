"""
MainbyteLabs R&D Idea Engine — Option A: OpenAI Proxy Server

Sits between the browser and the OpenAI API.
Injects your API key server-side — the browser never sees it.

Usage:
    python proxy.py

Requires:
    pip install flask flask-cors requests

Set your key before starting:
    Linux/Mac:   export OPENAI_API_KEY=your_key_here
    Windows CMD: set OPENAI_API_KEY=your_key_here
"""

import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder=".")
CORS(app)

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def get_api_key() -> str:
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise EnvironmentError(
            "OPENAI_API_KEY environment variable is not set. "
            "Set it before starting the proxy."
        )
    return key


@app.route("/")
def serve_tool():
    return send_from_directory(".", "app.html")


@app.route("/v1/chat/completions", methods=["POST"])
def proxy_completions():
    """Proxy to OpenAI chat completions, injecting API key server-side."""
    try:
        api_key = get_api_key()
    except EnvironmentError as e:
        return jsonify({"error": {"message": str(e)}}), 500

    payload = request.get_json(force=True, silent=True)
    if payload is None:
        return jsonify({"error": {"message": "Invalid JSON body."}}), 400

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    try:
        resp = requests.post(
            OPENAI_API_URL,
            headers=headers,
            json=payload,
            timeout=120,
        )
        return jsonify(resp.json()), resp.status_code

    except requests.exceptions.Timeout:
        return jsonify({"error": {"message": "Request timed out."}}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": {"message": f"Proxy error: {str(e)}"}}), 502


@app.route("/health")
def health():
    key_set = bool(os.environ.get("OPENAI_API_KEY", ""))
    return jsonify({"status": "ok", "api_key_set": key_set})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    print(f"\n  MainbyteLabs R&D Idea Engine — Option A (OpenAI)")
    print(f"  Open in browser: http://localhost:{port}/")
    print(f"  Health check:    http://localhost:{port}/health")
    key_set = bool(os.environ.get("OPENAI_API_KEY", ""))
    if not key_set:
        print(f"\n  WARNING: OPENAI_API_KEY is not set — API calls will fail.\n")
    else:
        print(f"  API key: set ✓\n")
    app.run(host="127.0.0.1", port=port, debug=False)
