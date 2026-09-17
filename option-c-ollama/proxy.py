"""
MainbyteLabs R&D Idea Engine — Option C: Ollama Proxy Server

Sits between the browser and your local Ollama instance.
No API key required. No third-party cost.

Usage:
    python proxy.py

Requires:
    pip install flask flask-cors requests
    Ollama installed and running: https://ollama.com
    A model pulled: ollama pull llama3  (or mistral)

Ollama must be running before starting this proxy:
    ollama serve
"""

import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder=".")
CORS(app)

OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "llama3"


def check_ollama() -> tuple[bool, str]:
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=3)
        if resp.ok:
            models = [m["name"] for m in resp.json().get("models", [])]
            return True, models
        return False, []
    except Exception:
        return False, []


@app.route("/")
def serve_tool():
    return send_from_directory(".", "app.html")


@app.route("/v1/chat", methods=["POST"])
def proxy_chat():
    """
    Accept the browser's request and forward to Ollama.
    Translates the app's payload format to Ollama's chat format.
    """
    payload = request.get_json(force=True, silent=True)
    if payload is None:
        return jsonify({"error": "Invalid JSON body."}), 400

    model = payload.get("model", DEFAULT_MODEL)
    messages = payload.get("messages", [])

    ollama_payload = {
        "model": model,
        "messages": messages,
        "stream": False,
    }

    try:
        resp = requests.post(OLLAMA_URL, json=ollama_payload, timeout=180)
        if not resp.ok:
            return jsonify({"error": f"Ollama returned {resp.status_code}"}), resp.status_code
        data = resp.json()
        content = data.get("message", {}).get("content", "")
        return jsonify({"content": content}), 200

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Cannot connect to Ollama. Make sure 'ollama serve' is running."}), 503
    except requests.exceptions.Timeout:
        return jsonify({"error": "Ollama request timed out. Try a smaller model or fewer ideas."}), 504


@app.route("/health")
def health():
    running, models = check_ollama()
    return jsonify({
        "status": "ok",
        "ollama_running": running,
        "available_models": models,
    })


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5050))
    print(f"\n  MainbyteLabs R&D Idea Engine — Option C (Ollama)")
    print(f"  Open in browser: http://localhost:{port}/")
    print(f"  Health check:    http://localhost:{port}/health")
    running, models = check_ollama()
    if not running:
        print(f"\n  WARNING: Ollama is not running.")
        print(f"  Start it with: ollama serve")
        print(f"  Then pull a model: ollama pull llama3\n")
    else:
        print(f"  Ollama: running ✓")
        print(f"  Models: {', '.join(models) if models else 'none pulled yet'}\n")
    app.run(host="127.0.0.1", port=port, debug=False)
