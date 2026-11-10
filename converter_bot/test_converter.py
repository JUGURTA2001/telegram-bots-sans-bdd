"""Tests du convertisseur. Lancer : python -m unittest -v"""
import unittest

from converter import (
    ConversionError,
    answer,
    canonical_unit,
    convert,
    format_number,
    parse_currency,
    parse_query,
)


class TestUnits(unittest.TestCase):
    def test_longueur(self):
        self.assertAlmostEqual(convert(1, "km", "m"), 1000)
        self.assertAlmostEqual(convert(1, "mi", "km"), 1.609344)
        self.assertAlmostEqual(convert(12, "in", "ft"), 1.0)

    def test_masse(self):
        self.assertAlmostEqual(convert(1, "kg", "lb"), 2.2046226, places=5)
        self.assertAlmostEqual(convert(500, "g", "kg"), 0.5)

    def test_vitesse(self):
        self.assertAlmostEqual(convert(36, "km/h", "m/s"), 10)
        self.assertAlmostEqual(convert(100, "km/h", "mph"), 62.1371, places=3)

    def test_volume(self):
        self.assertAlmostEqual(convert(1000, "ml", "l"), 1)

    def test_identite(self):
        self.assertAlmostEqual(convert(42, "m", "m"), 42)


class TestTemperature(unittest.TestCase):
    def test_points_connus(self):
        self.assertAlmostEqual(convert(0, "c", "f"), 32)
        self.assertAlmostEqual(convert(100, "c", "f"), 212)
        self.assertAlmostEqual(convert(32, "f", "c"), 0)
        self.assertAlmostEqual(convert(0, "c", "k"), 273.15)
        self.assertAlmostEqual(convert(-40, "c", "f"), -40)

    def test_zero_absolu(self):
        with self.assertRaises(ConversionError):
            convert(-300, "c", "f")

    def test_temperature_vers_longueur(self):
        with self.assertRaises(ConversionError):
            convert(10, "c", "km")


class TestErrors(unittest.TestCase):
    def test_categories_incompatibles(self):
        with self.assertRaises(ConversionError):
            convert(1, "kg", "km")

    def test_unite_inconnue(self):
        with self.assertRaises(ConversionError):
            canonical_unit("parsec")

    def test_format_invalide(self):
        for bad in ["bonjour", "10", "10 km", "10 km mi kg", "km en mi"]:
            with self.subTest(bad=bad), self.assertRaises(ConversionError):
                parse_query(bad)


class TestParsing(unittest.TestCase):
    def test_formes_courantes(self):
        self.assertEqual(parse_query("10 km en mi"), (10.0, "km", "mi"))
        self.assertEqual(parse_query("10km to mi"), (10.0, "km", "mi"))
        self.assertEqual(parse_query("2,5 kg lb"), (2.5, "kg", "lb"))
        self.assertEqual(parse_query("-5 °C en °F"), (-5.0, "c", "f"))

    def test_noms_complets_et_pluriels(self):
        self.assertEqual(parse_query("3 Kilomètres en miles"), (3.0, "km", "mi"))
        self.assertEqual(parse_query("2 litres en gallons"), (2.0, "l", "gal"))

    def test_reponse_complete(self):
        self.assertEqual(answer("1 km en m"), "1 km = 1 000 m")
        self.assertEqual(answer("100 c en f"), "100 c = 212 f")


class TestFormat(unittest.TestCase):
    def test_nombres(self):
        self.assertEqual(format_number(0), "0")
        self.assertEqual(format_number(1.50), "1.5")
        self.assertEqual(format_number(1234567.891), "1 234 567.891")
        self.assertEqual(format_number(1e15), "1.000000e+15")


class TestCurrencyParsing(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(parse_currency("100 eur usd"), (100.0, "EUR", "USD"))
        self.assertEqual(parse_currency("12,5 USD en DZD"), (12.5, "USD", "DZD"))

    def test_invalide(self):
        for bad in ["", "abc", "100 EUR", "100 EURO USD", "-5 EUR USD", "100 EUR USD GBP"]:
            with self.subTest(bad=bad), self.assertRaises(ConversionError):
                parse_currency(bad)


if __name__ == "__main__":
    unittest.main()
