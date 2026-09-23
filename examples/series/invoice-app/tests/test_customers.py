import unittest

from invoicing.customers import display_name, initials, matches, normalise_name, sort_key


class NormaliseTests(unittest.TestCase):
    def test_composed_and_decomposed_are_equal(self):
        self.assertEqual(normalise_name("Mu\u0308ller  GmbH "), "Müller GmbH")

    def test_keeps_case_and_accents(self):
        self.assertEqual(normalise_name("  Élodie   Durand"), "Élodie Durand")

    def test_missing_name(self):
        with self.assertRaises(ValueError):
            normalise_name(None)


class CompareTests(unittest.TestCase):
    def test_sort_key_ignores_accents_then_breaks_ties(self):
        names = ["Zeta", "Čapek", "Capek", "Élodie"]
        self.assertEqual(sorted(names, key=sort_key), ["Capek", "Čapek", "Élodie", "Zeta"])

    def test_matches_ignores_case_and_accents(self):
        self.assertTrue(matches("Müller GmbH", "muller"))
        self.assertTrue(matches("Žluťoučký kůň a.s.", "ZLUTOUCKY"))
        self.assertFalse(matches("North, Ltd", "south"))

    def test_initials(self):
        self.assertEqual(initials("Élodie Durand"), "ÉD")
        self.assertEqual(initials("Čapek & syn s.r.o."), "ČS")


class DisplayTests(unittest.TestCase):
    def test_short_names_unchanged(self):
        self.assertEqual(display_name("Acme Corp", 24), "Acme Corp")

    def test_truncates_without_splitting_accents(self):
        self.assertEqual(display_name("Žluťoučký kůň a.s.", 6), "Žluťo…")

    def test_newlines_become_spaces(self):
        self.assertEqual(display_name("Line\nbreak", 24), "Line break")


if __name__ == "__main__":
    unittest.main()
