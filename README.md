# 🤖 Bots Telegram sans base de données

Trois bots Telegram en Python ([aiogram 3](https://docs.aiogram.dev/)), faciles à personnaliser et à livrer à un client. Aucun ne nécessite de base de données.

| Bot | Rôle |
|---|---|
| [`faq_bot`](faq_bot/) | Répond aux questions fréquentes d'un commerce (menu à boutons + recherche libre par mots-clés) |
| [`converter_bot`](converter_bot/) | Convertit des unités et des devises |
| [`contact_bot`](contact_bot/) | Relaie les messages des clients vers le propriétaire, qui répond depuis Telegram |

## Technologies

Python · aiogram 3 · aiohttp · python-dotenv · tests unitaires (`unittest`)

## Installation (Windows, PowerShell)

```powershell
git clone https://github.com/JUGURTA2001/telegram-bots-sans-bdd.git
cd telegram-bots-sans-bdd
python -m venv venv
venv\Scripts\activate
pip install -r converter_bot\requirements.txt
```

Créez chaque bot avec **@BotFather** (`/newbot`), puis dans chaque dossier :

```powershell
copy faq_bot\.env.example faq_bot\.env
```
et collez le token dans `.env`. Le `contact_bot` demande aussi `ADMIN_ID` (votre identifiant Telegram numérique).

> ⚠️ Ne publiez jamais un fichier `.env` : il contient le token du bot. Il est exclu par `.gitignore`.

## Lancer un bot

```powershell
python faq_bot\bot.py
python converter_bot\bot.py
python contact_bot\bot.py
```

## Tests

Dans le dossier d'un bot : `python -m unittest -v`

## Captures d'écran

<!-- Ajoutez vos images dans un dossier docs/ puis : ![FAQ](docs/faq.png) -->

