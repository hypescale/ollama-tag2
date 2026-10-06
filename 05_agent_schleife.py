"""Agentische Schleife: Modell -> Tools -> Modell, maximal sechs Runden."""
import json
from ollama_api import MODEL, chat, eingabe
from bestell_tools import SEARCH_TOOL, LIST_TOOL, execute

SYSTEM = "Du bist ein Support-Assistent. Antworte auf Deutsch. Verwende die Tools für alle Bestelldaten. Für einen Überblick liste zuerst die Nummern auf und suche dann die einzelnen Bestellungen. Erfinde keine Daten."
MAX_ROUNDS = 6


def main():
    messages = [{"role": "system", "content": SYSTEM}]
    print(f"Modell: {MODEL} | exit / reset | Beispiel: Welche Bestellungen wurden versendet?")
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
            for step in range(MAX_ROUNDS):
                print(f"[Agent: Runde {step + 1}]")
                answer = chat(messages, tools=[SEARCH_TOOL, LIST_TOOL])
                messages.append(answer)
                calls = answer.get("tool_calls") or []
                if not calls:
                    print("Assistent:", answer.get("content", ""))
                    break
                for call in calls:
                    result = execute(call, allow_list=True)
                    name = call.get("function", {}).get("name", "unbekannt")
                    print("[Python führt Tool aus]", name, result)
                    messages.append({"role": "tool", "tool_name": name,
                                     "content": json.dumps(result, ensure_ascii=False)})
            else:
                print("Schrittlimit erreicht. Keine abgeschlossene Antwort; bitte gezielter fragen.")
                del messages[checkpoint:]
        except RuntimeError as exc:
            del messages[checkpoint:]
            print("Fehler:", exc)


if __name__ == "__main__":
    main()
