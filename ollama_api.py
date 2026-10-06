"""Kleiner Ollama-HTTP-Client, nur Python-Standardbibliothek."""
import json
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

MODEL = os.getenv("OLLAMA_MODEL", "gemma4:latest")
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
if not HOST.startswith(("http://", "https://")):
    HOST = "http://" + HOST
SYSTEM = "Du bist ein freundlicher Assistent. Antworte kurz auf Deutsch."


def request(messages, stream=False, tools=None):
    body = {"model": MODEL, "messages": messages, "stream": stream,
            "options": {"temperature": 0.2}}
    # Optional: OLLAMA_THINK=false. Nicht jedes Modell unterstützt Abschalten.
    if os.getenv("OLLAMA_THINK") is not None:
        value = os.environ["OLLAMA_THINK"].lower()
        body["think"] = {"true": True, "false": False}.get(value, value)
    if tools:
        body["tools"] = tools
    req = Request(HOST + "/api/chat", data=json.dumps(body).encode(),
                  headers={"Content-Type": "application/json"})
    try:
        return urlopen(req, timeout=300)
    except HTTPError as exc:
        raise RuntimeError(f"Ollama HTTP {exc.code}: {exc.read().decode()}") from exc
    except URLError as exc:
        raise RuntimeError(f"Ollama unter {HOST} nicht erreichbar. Server prüfen: {exc.reason}") from exc


def chat(messages, tools=None):
    with request(messages, tools=tools) as response:
        data = json.load(response)
    if data.get("error"):
        raise RuntimeError(data["error"])
    return data["message"]


def chat_stream(messages):
    """Liefert NDJSON-Nachrichten. Thinking bleibt getrennt von content."""
    with request(messages, stream=True) as response:
        for line in response:
            if not line.strip():
                continue
            data = json.loads(line)
            if data.get("error"):
                raise RuntimeError(data["error"])
            yield data.get("message", {})


def eingabe():
    try:
        return input("Du: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return "exit"
