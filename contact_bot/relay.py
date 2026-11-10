"""Aide au relais de messages (logique pure : pas de Telegram, pas de réseau).

Astuce « sans base de données » : l'identifiant de l'utilisateur est écrit dans le
message transmis à l'administrateur. Quand l'administrateur répond à ce message,
on relit l'identifiant dans le texte cité pour savoir à qui renvoyer la réponse.
"""
import re

ID_TAG = re.compile(r"\[ID:(\d{1,20})\]")
MAX_LENGTH = 3000  # Telegram accepte 4096 caractères : on garde de la marge pour l'en-tête


def build_forward(user_id: int, full_name: str, username: str | None, text: str) -> str:
    """Message envoyé à l'administrateur (texte brut, sans mise en forme risquée)."""
    who = full_name.strip() or "Utilisateur"
    if username:
        who += f" (@{username})"
    # L'identifiant réel est placé EN PREMIER : extract_user_id() lit le premier tag,
    # donc un nom ou un texte contenant un faux « [ID:...] » ne peut pas le détourner.
    return f"[ID:{user_id}] 📩 Message de {who}\n\n{text}"


def extract_user_id(replied_text: str | None) -> int | None:
    """Retrouve l'identifiant dans le message auquel l'administrateur répond."""
    if not replied_text:
        return None
    match = ID_TAG.search(replied_text)
    return int(match.group(1)) if match else None


def is_too_long(text: str) -> bool:
    return len(text) > MAX_LENGTH


class RateLimiter:
    """Anti-spam en mémoire : un message toutes les `delay` secondes par utilisateur."""

    def __init__(self, delay: float = 2.0):
        self.delay = delay
        self._last: dict[int, float] = {}

    def allow(self, user_id: int, now: float) -> bool:
        last = self._last.get(user_id)
        if last is not None and now - last < self.delay:
            return False
        self._last[user_id] = now
        # Évite que le dictionnaire grossisse indéfiniment.
        if len(self._last) > 10_000:
            self._last = {u: t for u, t in self._last.items() if now - t < self.delay}
        return True
