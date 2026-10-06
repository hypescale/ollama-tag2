"""Ein Tool-Schritt, dann eine abschließende Modellantwort."""
import json
from ollama_api import MODEL, chat, eingabe
from bestell_tools import SEARCH_TOOL, execute

SYSTEM = "Du bist ein Support-Assistent. Antworte auf Deutsch. Nutze für Bestellstatus immer das Tool. Erfinde keine Bestelldaten. Frage nach der Bestellnummer, wenn sie fehlt."


def main():
    messages = [{"role": "system", "content": SYSTEM}]
    print(f"Modell: {MODEL} | exit / reset | Beispiel: Wo ist Bestellung 1002?")
    while True:
        text = eingabe()
        if text.lower() == "exit":
            break
        if text.lower() == "reset":
            messages = messages[:1]
            continue
        if not text:
            continue
        checkpoint = len(messages)
        messages.append({"role": "user", "content": text})
        try:
            answer = chat(messages, tools=[SEARCH_TOOL])
            messages.append(answer)  # Tool-Aufrufe gehören in den Verlauf.
            calls = answer.get("tool_calls") or []
            for call in calls:
                result = execute(call)
                name = call.get("function", {}).get("name", "unbekannt")
                print("[Python führt Tool aus]", name, result)
                messages.append({"role": "tool", "tool_name": name,
                                 "content": json.dumps(result, ensure_ascii=False)})
            if calls:
                # Ohne tools: dieser Schritt formuliert nur die finale Antwort.
                answer = chat(messages)
                messages.append(answer)
            print("Assistent:", answer.get("content", ""))
        except RuntimeError as exc:
            del messages[checkpoint:]
            print("Fehler:", exc)


if __name__ == "__main__":
    main()
