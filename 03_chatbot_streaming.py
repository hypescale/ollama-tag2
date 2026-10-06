"""Streaming, Verlauf sowie save/load einer lokalen JSON-Datei."""
import json
from pathlib import Path
from ollama_api import SYSTEM, MODEL, chat_stream, eingabe

FILE = Path(__file__).resolve().parent / "chatverlauf.json"


def main():
    messages = [{"role": "system", "content": SYSTEM}]
    print(f"Modell: {MODEL} | exit / reset / save / load")
    while True:
        text = eingabe()
        command = text.lower()
        if command == "exit":
            break
        if command == "reset":
            messages = [{"role": "system", "content": SYSTEM}]
            print("Verlauf gelöscht.")
            continue
        if command == "save":
            try:
                FILE.write_text(json.dumps(messages, ensure_ascii=False, indent=2), encoding="utf-8")
                print("Gespeichert:", FILE)
            except OSError as exc:
                print("Speichern fehlgeschlagen:", exc)
            continue
        if command == "load":
            try:
                loaded = json.loads(FILE.read_text(encoding="utf-8"))
                if not isinstance(loaded, list) or not all(
                    isinstance(m, dict) and m.get("role") in {"system", "user", "assistant"}
                    and isinstance(m.get("content"), str) for m in loaded):
                    raise ValueError("Ungültiger Chatverlauf")
                messages = loaded
                print("Verlauf geladen.")
            except (OSError, ValueError) as exc:
                print("Laden fehlgeschlagen:", exc)
            continue
        if not text:
            continue
        messages.append({"role": "user", "content": text})
        print("Assistent: ", end="", flush=True)
        content, thinking = "", ""
        try:
            for message in chat_stream(messages):
                token = message.get("content", "")
                content += token
                thinking += message.get("thinking", "")
                print(token, end="", flush=True)
            print()
            answer = {"role": "assistant", "content": content}
            if thinking:
                answer["thinking"] = thinking
            messages.append(answer)
        except RuntimeError as exc:
            messages.pop()
            print("\nFehler:", exc)


if __name__ == "__main__":
    main()
