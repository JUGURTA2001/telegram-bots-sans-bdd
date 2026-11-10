"""Tests de la recherche FAQ. Lancer : python -m unittest -v"""
import unittest

import config
from faq import best_match, normalize, tokens


class TestNormalize(unittest.TestCase):
    def test_accents_et_casse(self):
        self.assertEqual(normalize("Réservation À Midi !"), "reservation a midi")

    def test_stopwords_retires(self):
        self.assertEqual(tokens("Quels sont les horaires ?"), {"sont", "horaires"})


class TestBestMatch(unittest.TestCase):
    def idx(self, query):
        i = best_match(query, config.FAQ)
        return None if i is None else config.FAQ[i]["question"]

    def test_mot_cle_simple(self):
        self.assertEqual(self.idx("horaires"), "Quels sont vos horaires ?")

    def test_phrase_avec_accents(self):
        self.assertEqual(self.idx("Je voudrais réserver une table"), "Comment réserver une table ?")

    def test_livraison(self):
        self.assertEqual(self.idx("vous livrez à domicile ?"), "Faites-vous la livraison ?")

    def test_majuscules(self):
        self.assertEqual(self.idx("PRIX"), "Quels sont vos prix ?")

    def test_aucune_correspondance(self):
        self.assertIsNone(self.idx("blablabla xyz"))

    def test_texte_vide(self):
        self.assertIsNone(self.idx(""))

    def test_un_mot_de_la_question_seul_ne_suffit_pas(self):
        # "sont" apparaît dans une question mais ne doit pas déclencher de réponse
        self.assertIsNone(self.idx("sont"))


class TestConfig(unittest.TestCase):
    def test_entrees_valides(self):
        for entry in config.FAQ:
            self.assertTrue(entry["question"].strip())
            self.assertTrue(entry["answer"].strip())
            self.assertTrue(entry["keywords"])

    def test_limite_telegram(self):
        for entry in config.FAQ:
            self.assertLess(len(entry["answer"]), 3500)


if __name__ == "__main__":
    unittest.main()
