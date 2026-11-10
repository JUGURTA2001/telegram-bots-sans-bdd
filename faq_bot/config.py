"""
Personnalisez ce fichier pour chaque client : c'est le SEUL à modifier.
Les informations ci-dessous sont un exemple fictif.
"""

BUSINESS_NAME = "Café Atlas"

WELCOME = (
    f"👋 Bienvenue chez {BUSINESS_NAME} !\n\n"
    "Choisissez une question ci-dessous, ou écrivez-moi simplement "
    "votre question (ex. « horaires », « livraison »)."
)

FALLBACK = (
    "🤔 Je n'ai pas trouvé de réponse à votre question.\n"
    "Choisissez une question dans le menu, ou contactez-nous directement."
)

CONTACT = (
    "📞 Nous contacter\n\n"
    "Téléphone : 0X XX XX XX XX\n"
    "Email : contact@exemple.com\n"
    "Adresse : 12 rue Didouche Mourad, Alger"
)

# Chaque entrée : question affichée, réponse, mots-clés pour la recherche libre.
FAQ = [
    {
        "question": "Quels sont vos horaires ?",
        "answer": "🕗 Nous sommes ouverts tous les jours de 8h à 22h, sauf le vendredi matin.",
        "keywords": ["horaires", "heures", "ouvert", "ouverture", "fermeture", "ferme"],
    },
    {
        "question": "Où êtes-vous situés ?",
        "answer": "📍 12 rue Didouche Mourad, Alger. À 5 minutes du métro.",
        "keywords": ["adresse", "situe", "localisation", "ou", "plan", "metro"],
    },
    {
        "question": "Quels sont vos prix ?",
        "answer": (
            "💰 Quelques exemples :\n"
            "• Café : 120 DA\n"
            "• Thé à la menthe : 150 DA\n"
            "• Menu du jour : 900 DA"
        ),
        "keywords": ["prix", "tarif", "tarifs", "cout", "combien", "carte", "menu"],
    },
    {
        "question": "Faites-vous la livraison ?",
        "answer": "🛵 Oui, livraison gratuite à partir de 2 000 DA dans un rayon de 5 km.",
        "keywords": ["livraison", "livrer", "domicile", "commande", "emporter"],
    },
    {
        "question": "Comment réserver une table ?",
        "answer": "📅 Appelez-nous au 0X XX XX XX XX ou écrivez-nous via le bouton Contact.",
        "keywords": ["reserver", "reservation", "table", "groupe", "anniversaire"],
    },
    {
        "question": "Quels moyens de paiement acceptez-vous ?",
        "answer": "💳 Espèces et carte CIB. Le paiement en ligne n'est pas encore disponible.",
        "keywords": ["paiement", "payer", "carte", "cib", "especes", "cash"],
    },
]
