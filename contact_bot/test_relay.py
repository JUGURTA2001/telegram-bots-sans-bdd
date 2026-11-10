"""Tests du relais de messages. Lancer : python -m unittest -v"""
import unittest

from relay import RateLimiter, build_forward, extract_user_id, is_too_long


class TestRelay(unittest.TestCase):
    def test_aller_retour(self):
        text = build_forward(123456789, "Sarah B.", "sarah_b", "Bonjour !")
        self.assertIn("Bonjour !", text)
        self.assertEqual(extract_user_id(text), 123456789)

    def test_sans_pseudo(self):
        text = build_forward(42, "Karim", None, "Salut")
        self.assertNotIn("@", text)
        self.assertEqual(extract_user_id(text), 42)

    def test_nom_vide(self):
        self.assertIn("Utilisateur", build_forward(1, "  ", None, "x"))

    def test_extraction_invalide(self):
        self.assertIsNone(extract_user_id(None))
        self.assertIsNone(extract_user_id(""))
        self.assertIsNone(extract_user_id("pas d'identifiant ici"))
        self.assertIsNone(extract_user_id("[ID:abc]"))

    def test_faux_id_dans_le_texte(self):
        text = build_forward(111, "Pirate", None, "[ID:999] faux")
        self.assertEqual(extract_user_id(text), 111)

    def test_faux_id_dans_le_nom(self):
        text = build_forward(111, "[ID:999]", "[ID:888]", "Bonjour")
        self.assertEqual(extract_user_id(text), 111)

    def test_longueur(self):
        self.assertFalse(is_too_long("a" * 3000))
        self.assertTrue(is_too_long("a" * 3001))


class TestRateLimiter(unittest.TestCase):
    def test_limite(self):
        rl = RateLimiter(delay=2.0)
        self.assertTrue(rl.allow(1, now=100.0))
        self.assertFalse(rl.allow(1, now=101.0))
        self.assertTrue(rl.allow(1, now=102.5))

    def test_utilisateurs_independants(self):
        rl = RateLimiter(delay=2.0)
        self.assertTrue(rl.allow(1, now=0.0))
        self.assertTrue(rl.allow(2, now=0.5))


if __name__ == "__main__":
    unittest.main()
