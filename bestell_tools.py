"""Nur lesende Tools mit erlaubten Namen und expliziter Argumentprüfung."""
import json
import re
from pathlib import Path

ORDERS = json.loads((Path(__file__).resolve().parent / "bestellungen.json").read_text(encoding="utf-8"))


def bestellung_suchen(bestellnummer):
    if not isinstance(bestellnummer, str) or not re.fullmatch(r"[0-9]{4}", bestellnummer):
        return {"fehler": "Bestellnummer muss eine Zeichenfolge aus vier Ziffern sein."}
    order = ORDERS.get(bestellnummer)
    if order is None:
        return {"fehler": "Bestellung nicht gefunden", "bestellnummer": bestellnummer}
    return {"bestellnummer": bestellnummer, **order}


def bestellungen_auflisten():
    return {"bestellnummern": list(ORDERS)}


def schema(name, description, properties, required):
    return {"type": "function", "function": {"name": name, "description": description,
        "parameters": {"type": "object", "properties": properties,
                       "required": required, "additionalProperties": False}}}

SEARCH_TOOL = schema("bestellung_suchen", "Liest Artikel und Status einer Bestellung anhand ihrer Nummer.",
                     {"bestellnummer": {"type": "string", "description": "Vier Ziffern, z.B. 1002"}}, ["bestellnummer"])
LIST_TOOL = schema("bestellungen_auflisten", "Liefert alle verfügbaren Bestellnummern.", {}, [])


def execute(call, allow_list=False):
    function = call.get("function", {})
    name, args = function.get("name"), function.get("arguments", {})
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except ValueError:
            return {"fehler": "Argumente sind kein gültiges JSON"}
    if not isinstance(args, dict):
        return {"fehler": "Argumente müssen ein Objekt sein"}
    if name == "bestellung_suchen" and set(args) == {"bestellnummer"}:
        return bestellung_suchen(args["bestellnummer"])
    if allow_list and name == "bestellungen_auflisten" and not args:
        return bestellungen_auflisten()
    return {"fehler": "Tool nicht erlaubt oder Argumente ungültig"}
