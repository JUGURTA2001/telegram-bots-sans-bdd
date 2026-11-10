"""Recherche dans la FAQ (logique pure : pas de Telegram, pas de réseau)."""
import re
import unicodedata

# Mots trop courants pour aider à retrouver une question.
STOPWORDS = {
    "le", "la", "les", "un", "une", "des", "de", "du", "d", "l", "a", "au", "aux",
    "et", "ou", "en", "est", "que", "qui", "quoi", "quel", "quelle", "quels",
    "quelles", "pour", "sur", "dans", "vous", "votre", "vos", "je", "tu", "il",
    "nous", "ce", "cette", "ces", "mon", "ma", "mes", "y", "ya", "avez", "est-ce",
    "comment", "svp", "bonjour", "salut",
}

# Score minimum pour considérer qu'une question correspond.
MIN_SCORE = 2


def normalize(text: str) -> str:
    """Minuscules, sans accents, ponctuation remplacée par des espaces."""
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def tokens(text: str) -> set[str]:
    """Ensemble des mots utiles d'un texte."""
    return {w for w in normalize(text).split() if w and w not in STOPWORDS}


def score(query: str, entry: dict) -> int:
    """Un mot-clé trouvé vaut 2 points, un mot de la question vaut 1 point."""
    q = tokens(query)
    keywords = tokens(" ".join(entry.get("keywords", [])))
    question = tokens(entry["question"]) - keywords
    return 2 * len(q & keywords) + len(q & question)


def best_match(query: str, faq: list[dict]) -> int | None:
    """Retourne l'index de la meilleure entrée, ou None si rien ne convient."""
    best_index, best_score = None, 0
    for i, entry in enumerate(faq):
        s = score(query, entry)
        if s > best_score:
            best_index, best_score = i, s
    return best_index if best_score >= MIN_SCORE else None
