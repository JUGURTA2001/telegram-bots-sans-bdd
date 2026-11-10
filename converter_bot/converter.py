"""Conversions d'unités et analyse des demandes (logique pure : sans réseau ni Telegram)."""
import re
import unicodedata


class ConversionError(ValueError):
    """Erreur lisible par l'utilisateur."""


# Pour chaque catégorie : facteur de conversion vers l'unité de base.
CATEGORIES: dict[str, dict[str, float]] = {
    "longueur (base : m)": {
        "mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0,
        "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.344,
    },
    "masse (base : kg)": {
        "mg": 1e-6, "g": 0.001, "kg": 1.0, "t": 1000.0,
        "oz": 0.028349523125, "lb": 0.45359237,
    },
    "volume (base : l)": {
        "ml": 0.001, "cl": 0.01, "l": 1.0, "m3": 1000.0, "gal": 3.785411784,
    },
    "vitesse (base : m/s)": {
        "m/s": 1.0, "km/h": 1 / 3.6, "mph": 0.44704, "kn": 1852 / 3600,
    },
}

TEMPERATURES = {"c", "f", "k"}

# Noms alternatifs (sans accents, au singulier) -> unité canonique.
ALIASES = {
    "metre": "m", "kilometre": "km", "centimetre": "cm", "millimetre": "mm",
    "mile": "mi", "pied": "ft", "foot": "ft", "feet": "ft", "pouce": "in",
    "inch": "in", "inche": "in", "yard": "yd",
    "gramme": "g", "gram": "g", "kilogramme": "kg", "kilo": "kg", "tonne": "t",
    "livre": "lb", "pound": "lb", "once": "oz", "ounce": "oz",
    "litre": "l", "millilitre": "ml", "centilitre": "cl", "gallon": "gal",
    "kmh": "km/h", "kph": "km/h", "ms": "m/s", "noeud": "kn", "knot": "kn",
    "celsius": "c", "fahrenheit": "f", "kelvin": "k",
}

CONNECTORS = {"en", "to", "vers", "->", "=>", "="}

UNIT_TO_CATEGORY = {
    unit: name for name, units in CATEGORIES.items() for unit in units
}


def _strip_accents(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c))


def canonical_unit(raw: str) -> str:
    """Retourne l'unité canonique (ex. « Kilomètres » -> « km »)."""
    unit = _strip_accents(raw.strip().lower()).replace("°", "")
    candidates = [unit]
    if unit.endswith("s") and len(unit) > 2:
        candidates.append(unit[:-1])  # pluriel
    for candidate in candidates:
        candidate = ALIASES.get(candidate, candidate)
        if candidate in UNIT_TO_CATEGORY or candidate in TEMPERATURES:
            return candidate
    raise ConversionError(f"Unité inconnue : « {raw} ». Tapez /unites pour la liste.")


def _convert_temperature(value: float, src: str, dst: str) -> float:
    if src == "c":
        celsius = value
    elif src == "f":
        celsius = (value - 32) * 5 / 9
    else:
        celsius = value - 273.15
    if celsius < -273.15 - 1e-9:
        raise ConversionError("Température sous le zéro absolu.")
    if dst == "c":
        return celsius
    if dst == "f":
        return celsius * 9 / 5 + 32
    return celsius + 273.15


def convert(value: float, src: str, dst: str) -> float:
    """Convertit `value` de `src` vers `dst` (unités déjà canoniques)."""
    if src in TEMPERATURES or dst in TEMPERATURES:
        if src not in TEMPERATURES or dst not in TEMPERATURES:
            raise ConversionError("Impossible de convertir une température en autre chose.")
        return _convert_temperature(value, src, dst)
    cat_src, cat_dst = UNIT_TO_CATEGORY[src], UNIT_TO_CATEGORY[dst]
    if cat_src != cat_dst:
        raise ConversionError(
            f"Impossible de convertir {src} ({cat_src.split(' ')[0]}) "
            f"en {dst} ({cat_dst.split(' ')[0]})."
        )
    factors = CATEGORIES[cat_src]
    return value * factors[src] / factors[dst]


_NUMBER = re.compile(r"^\s*([-+]?\d+(?:[.,]\d+)?)\s*(.*)$")


def parse_number(raw: str) -> float:
    try:
        return float(raw.replace(",", "."))
    except ValueError:
        raise ConversionError(f"Nombre invalide : « {raw} ».") from None


def parse_query(text: str) -> tuple[float, str, str]:
    """Analyse « 10 km en mi » ou « 20°C to F » -> (10.0, 'km', 'mi')."""
    match = _NUMBER.match(text)
    if not match:
        raise ConversionError("Format attendu : « 10 km en mi » (nombre, unité, unité).")
    value = parse_number(match.group(1))
    rest = match.group(2).replace("°", " ")
    words = [w for w in rest.split() if w.lower() not in CONNECTORS]
    if len(words) != 2:
        raise ConversionError("Format attendu : « 10 km en mi » (nombre, unité, unité).")
    return value, canonical_unit(words[0]), canonical_unit(words[1])


def format_number(x: float) -> str:
    """Nombre lisible : espaces comme séparateur de milliers, 6 décimales maximum."""
    if x == 0:
        return "0"
    if abs(x) >= 1e12 or abs(x) < 1e-6:
        return f"{x:.6e}"
    text = f"{x:,.6f}".rstrip("0").rstrip(".")
    return text.replace(",", " ")


def answer(text: str) -> str:
    """Texte complet de la réponse pour une demande d'utilisateur."""
    value, src, dst = parse_query(text)
    result = convert(value, src, dst)
    return f"{format_number(value)} {src} = {format_number(result)} {dst}"


_CODE = re.compile(r"^[A-Za-z]{3}$")


def parse_currency(args: str) -> tuple[float, str, str]:
    """Analyse « 100 EUR USD » ou « 100 eur en dzd » -> (100.0, 'EUR', 'USD')."""
    match = _NUMBER.match(args or "")
    if not match:
        raise ConversionError("Format : /devise 100 EUR USD")
    amount = parse_number(match.group(1))
    words = [w for w in match.group(2).split() if w.lower() not in CONNECTORS]
    if len(words) != 2 or not all(_CODE.match(w) for w in words):
        raise ConversionError("Format : /devise 100 EUR USD (codes à 3 lettres).")
    if amount < 0:
        raise ConversionError("Le montant doit être positif.")
    return amount, words[0].upper(), words[1].upper()


def units_help() -> str:
    lines = ["📏 Unités disponibles :"]
    for name, units in CATEGORIES.items():
        lines.append(f"• {name.split(' ')[0].capitalize()} : {', '.join(units)}")
    lines.append("• Température : c, f, k")
    return "\n".join(lines)
