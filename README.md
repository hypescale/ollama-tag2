# Ollama-Workshop – Tag 2

Python 3.10 oder neuer. Keine pip-Pakete erforderlich: Die Skripte verwenden die lokale Ollama-HTTP-API über die Python-Standardbibliothek. Ollama muss laufen und das Modell bereits heruntergeladen sein.

## Ubuntu: Start

ZIP entpacken, im Terminal in den Ordner ollama-tag2 wechseln:

```bash
python3 --version
ollama list
export OLLAMA_MODEL='gemma4:latest'
python3 00_verbindung_pruefen.py
python3 01_einfacher_chatbot.py
```

Eigenes Modell verwenden: `export OLLAMA_MODEL='martin'`. Für einen anderen Server: `export OLLAMA_HOST='http://localhost:11434'`. Einstellungen gelten für das aktuelle Terminal. Jederzeit `exit` eingeben; Strg+C bei der Eingabe beendet ebenfalls.

Thinking optional abschalten: `export OLLAMA_THINK=false`. Nur verwenden, wenn das Modell das unterstützt. Rückkehr zum Modellstandard: `unset OLLAMA_THINK`. Die Streaming-Übung zeigt nur Antworttext; das Ausblenden von Thinking schaltet es nicht ab.

## Reihenfolge und Übungen

| Skript | Lernziel | Test |
|---|---|---|
| 00_verbindung_pruefen.py | Server und Modell prüfen | Modell und Fähigkeiten werden angezeigt |
| 01_einfacher_chatbot.py | Nachrichtenrollen, erster Modellaufruf | „Ich heiße Martin.“ Dann „Wie heiße ich?“ – kein mitgeführter Verlauf |
| 02_chatbot_mit_verlauf.py | Gesprächsgedächtnis | Gleicher Versuch; dann `reset` und erneut fragen |
| 03_chatbot_streaming.py | Streaming, save/load/reset | Namen nennen, `save`, `reset`, `load`, Namen abfragen |
| 04_tool_calling.py | Ein Tool-Schritt mit überprüften Argumenten | „Wo ist Bestellung 1002?“ / „Und 9999?“ |
| 05_agent_schleife.py | Mehrere Modell- und Tool-Schritte | „Welche Bestellungen wurden versendet?“ |

Skripte einzeln starten, beispielsweise `python3 04_tool_calling.py`. Die gemeinsamen Module müssen im selben Ordner liegen.

## Bestellsuche

Die drei Bestellungen in bestellungen.json sind erfunden. Daten werden relativ zur Skriptdatei geladen, unabhängig vom aktuellen Terminalordner. Änderungen werden beim nächsten Start eingelesen.

04: Modell schlägt einen Tool-Aufruf vor → Python prüft Name und Argumente → Python liest die Bestellung → Ergebnis als Tool-Nachricht → Modell formuliert Antwort.

05: Gleicher Ablauf in einer Schleife. Zusätzlich kann das Modell alle Bestellnummern auflisten und anschließend deren Status abfragen. Maximal sechs Runden verhindern eine endlose Schleife. Mehrere Tool-Aufrufe einer Runde werden nacheinander ausgeführt.

Wichtig: Das Modell muss echtes Tool Calling unterstützen. Wenn 04/05 eine Fehlermeldung zeigen, 00 ausführen und ein geeignetes installiertes Modell wählen. Als dokumentiertes Beispiel kann qwen3 verwendet werden (`ollama pull qwen3`, dann `export OLLAMA_MODEL='qwen3'`); Download und Speicherbedarf vorab prüfen. Keine automatische Modellinstallation durch die Skripte.

## Moderation

- Nachrichtenrollen und Verlauf im Code gemeinsam lesen.
- Cline zuerst den Code erklären lassen, danach eine kleine Änderung beauftragen.
- Teilnehmer sollen die Tool-Ausgabe im Terminal mit der Modellantwort vergleichen.
- System-Prompts sind keine Zugriffskontrolle. Die Python-Funktion erlaubt nur zwei explizite, lesende Aktionen.
- Dieses Demo-Programm hat keine Benutzeranmeldung oder kundenbezogenen Berechtigungen. Nur erfundene Daten verwenden.
- Der Verlauf ist begrenzt durch das Modellkontextfenster, wird aber nicht automatisch gekürzt. Bei langen Gesprächen `reset` verwenden.
- `save` speichert den Gesprächsverlauf als lokale Klartextdatei und überschreibt den vorherigen Stand. Keine echten Geheimnisse eingeben.

## Erweiterungsaufgaben

1. Antwortstil im SYSTEM-Text ändern und Wirkung prüfen.
2. Streaming-Chatbot um einen Befehl `help` erweitern.
3. Eine vierte Bestellung in bestellungen.json hinzufügen.
4. Tool-Argumente absichtlich falsch testen: Nummer fehlt, Zahl statt String, fünf Ziffern.
5. Agent fragen, welche Bestellung zugestellt wurde und welche noch in Bearbeitung ist.

## Open WebUI

Für den Vergleich die bereits eingerichtete Open-WebUI-Instanz verwenden und dasselbe Modell auswählen. Die Python-Tools sind nicht automatisch in Open WebUI verfügbar. Deren Integration ist eine separate Übung; keine zusätzliche Installation nötig für dieses Paket.

## Prüfung und Grenzen

Syntax, lokale Tool-Validierung sowie HTTP-/Streaming-/Tool-Schleifen wurden mit simulierten Ollama-Antworten geprüft. Ein Live-Test mit deinem lokalen Modell ist noch erforderlich; das Paket wurde nicht gegen einen laufenden Ollama-Server getestet.

Offizielle Referenzen:
- https://docs.ollama.com/api/chat
- https://docs.ollama.com/capabilities/tool-calling
- https://docs.ollama.com/capabilities/thinking
