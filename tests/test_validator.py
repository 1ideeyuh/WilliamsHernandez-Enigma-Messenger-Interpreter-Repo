import unittest
from src.validator import Validator

class TestValidator(unittest.TestCase):
    def test_valid_names(self):
        self.assertTrue(Validator.is_valid("alice"))
        self.assertTrue(Validator.is_valid("Bob3"))

    def test_invalid_names(self):
        for bad in ["", "1abc", "al ice", "al_ice", "al-ice", "al!ce"]:
            self.assertFalse(Validator.is_valid(bad))

    def test_non_string(self):
        self.assertFalse(Validator.is_valid(None))

    def test_filename_orders_names(self):
        self.assertEqual(Validator.filename("bob", "alice"), "alice-bob.txt")

    def test_filename_same_either_way(self):
        self.assertEqual(Validator.filename("a1", "b2"), Validator.filename("b2", "a1"))

    def test_filename_invalid_raises(self):
        with self.assertRaises(ValueError):
            Validator.filename("1bad", "alice")

    def test_filename_same_user_raises(self):
        with self.assertRaises(ValueError):
            Validator.filename("alice", "alice")

if __name__ == "__main__":
    unittest.main()
