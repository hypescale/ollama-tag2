"""Prüft Server, Modell und verfügbare Fähigkeiten ohne Modellgenerierung."""
import json
from urllib.request import Request, urlopen
from urllib.error import URLError
from ollama_api import MODEL, HOST


def main():
    try:
        with urlopen(HOST + "/api/version", timeout=10) as response:
            print("Ollama:", json.load(response))
        req = Request(HOST + "/api/show", data=json.dumps({"model": MODEL}).encode(),
                      headers={"Content-Type": "application/json"})
        with urlopen(req, timeout=30) as response:
            data = json.load(response)
        print("Modell:", MODEL)
        print("Fähigkeiten:", data.get("capabilities", "Keine Metadaten verfügbar"))
        print("Thinking:", data.get("thinking", "Keine Metadaten verfügbar"))
        print("Für Übungen 04/05 muss das Modell Tool Calling unterstützen.")
    except URLError as exc:
        print("Fehler:", exc)
        if hasattr(exc, "read"):
            print(exc.read().decode())
        print("Server prüfen und Modell gegebenenfalls mit ollama pull herunterladen.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
