# Converter Bot

Bot Telegram qui convertit des unités et des devises.

## Utilisation

**Unités** (hors ligne) : écrire une ligne de texte.

```
10 km en mi
70 kg to lb
25 °C en °F
3 litres en gallons
```

Catégories : longueur, masse, volume, vitesse, température. Liste complète : `/unites`.

**Devises** : `/devise 100 EUR USD` (ou `/devise 100 usd en dzd`).

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

Les tests couvrent les conversions, la température (y compris le zéro absolu), les noms d'unités (pluriels, accents) et les entrées invalides.

## À savoir

- Les taux viennent de l'API gratuite [ExchangeRate-API](https://www.exchangerate-api.com) (une mise à jour par jour). La **mention de la source est obligatoire** : le bot l'affiche déjà. Ce sont des taux indicatifs, pas des taux de marché en direct ni des taux de change parallèles.
- Si une devise n'est pas gérée par l'API, le bot répond « Devise inconnue ». Testez les devises dont votre client a besoin avant de livrer.
- Les taux sont gardés en mémoire pendant 1 h pour limiter les appels ; la mémoire est vidée au redémarrage.
- Les unités sont dans `converter.py` (dictionnaire `CATEGORIES`) : ajoutez-en en une ligne.
