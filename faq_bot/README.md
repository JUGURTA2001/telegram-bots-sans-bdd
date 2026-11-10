# FAQ Bot

Bot Telegram pour un commerce : les clients obtiennent les horaires, prix, adresse, etc. sans attendre une réponse humaine.

## Fonctionnalités

- Menu à boutons (une question = un bouton), navigation « Retour au menu ».
- **Recherche libre** : le client écrit « vous livrez ? » et le bot trouve la bonne réponse (insensible aux accents et à la casse).
- Bouton **Contact**.
- Aucune base de données : tout le contenu est dans `config.py`.

## Personnaliser pour un client

Modifiez uniquement **`config.py`** : nom du commerce, message d'accueil, coordonnées, et la liste `FAQ`. Chaque entrée a :

```python
{
    "question": "Quels sont vos horaires ?",
    "answer": "Ouvert tous les jours de 8h à 22h.",
    "keywords": ["horaires", "heures", "ouvert"],   # aident la recherche libre
}
```

Ajoutez des mots-clés que les clients utilisent vraiment (sans accents, une forme par mot).

## Lancer

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env      # collez le token de @BotFather
python bot.py
```

## Tests

```powershell
python -m unittest -v
```

## Comment fonctionne la recherche libre

`faq.py` retire les mots courants (« le », « vous »…), puis compte les mots en commun : un mot-clé vaut 2 points, un mot de la question vaut 1 point. Il faut au moins 2 points pour répondre ; sinon le bot propose le menu.
