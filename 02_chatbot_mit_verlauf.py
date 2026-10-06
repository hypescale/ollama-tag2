"""Gespräch im Arbeitsspeicher; reset löscht das Gedächtnis."""
from ollama_api import SYSTEM, MODEL, chat, eingabe


def main():
    messages = [{"role": "system", "content": SYSTEM}]
    print(f"Modell: {MODEL} | exit / reset")
    while True:
        text = eingabe()
        if text.lower() == "exit":
            break
        if text.lower() == "reset":
            messages = messages[:1]
            print("Verlauf gelöscht.")
            continue
        if not text:
            continue
        messages.append({"role": "user", "content": text})
        try:
            answer = chat(messages)
            messages.append(answer)
            print("Assistent:", answer.get("content", ""))
        except RuntimeError as exc:
            messages.pop()  # Fehlgeschlagene Frage nicht im Verlauf lassen.
            print("Fehler:", exc)


if __name__ == "__main__":
    main()
