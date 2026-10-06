"""Jede Frage ist unabhängig: noch kein Gesprächsgedächtnis."""
from ollama_api import SYSTEM, MODEL, chat, eingabe


def main():
    print(f"Modell: {MODEL} | exit beendet")
    while True:
        text = eingabe()
        if text.lower() == "exit":
            break
        if not text:
            continue
        messages = [{"role": "system", "content": SYSTEM},
                    {"role": "user", "content": text}]
        try:
            print("Assistent:", chat(messages).get("content", ""))
        except RuntimeError as exc:
            print("Fehler:", exc)


if __name__ == "__main__":
    main()
