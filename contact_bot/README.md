# Contact Bot

Bot Telegram qui sert de **boîte de réception** : les clients lui écrivent, le propriétaire reçoit les messages et répond directement depuis Telegram.

## Fonctionnement (sans base de données)

1. Un client écrit au bot.
2. Le bot envoie au propriétaire : `[ID:123456789] 📩 Message de Sarah (@sarah) …`
3. Le propriétaire utilise **Répondre** (Reply) sur ce message.
4. Le bot relit l'identifiant `[ID:…]` dans le message cité et renvoie la réponse au bon client.

L'identifiant est placé en premier dans le message : un client ne peut pas se faire passer pour un autre en écrivant un faux `[ID:…]` (cas couvert par les tests).

## Configuration

1. Créez le bot avec **@BotFather** et copiez le token.
2. Trouvez votre identifiant Telegram numérique (par exemple avec un bot comme @userinfobot).
3. Copiez `.env.example` en `.env` et remplissez `BOT_TOKEN` et `ADMIN_ID`.
4. **Ouvrez une conversation avec votre bot et envoyez `/start`** : sans cela, le bot ne peut pas vous écrire.

## Lancer

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python bot.py
```

## Tests

```powershell
python -m unittest -v
```

## Limites

- Messages **texte uniquement** (photos, fichiers, vocaux : message d'information au client).
- Anti-spam simple en mémoire : 1 message toutes les 2 secondes par client.
- Un seul administrateur. Pour plusieurs agents, il faudrait stocker les conversations (base de données).
- Si le client a bloqué le bot, l'administrateur en est informé.
