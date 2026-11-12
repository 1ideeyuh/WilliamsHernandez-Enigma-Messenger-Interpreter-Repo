import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cipher import Cipher
from message import Message


class TestCipher(unittest.TestCase):

    def setUp(self):
        self.cipher = Cipher(3)

    def test_basic_encrypt(self):
        self.assertEqual(self.cipher.encrypt("abc"), "def")

    def test_wraps_around_alphabet(self):
        self.assertEqual(self.cipher.encrypt("xyz"), "abc")

    def test_keeps_case(self):
        self.assertEqual(self.cipher.encrypt("Hello"), "Khoor")

    def test_leaves_non_letters_alone(self):
        self.assertEqual(self.cipher.encrypt("hi, bob! 42"), "kl, ere! 42")

    def test_decrypt_reverses_encrypt(self):
        text = "Meet me at 5pm, Alice!"
        self.assertEqual(self.cipher.decrypt(self.cipher.encrypt(text)), text)

    def test_negative_shift(self):
        self.assertEqual(Cipher(-1).encrypt("bcd"), "abc")

    def test_shift_wraps_modulo_26(self):
        self.assertEqual(Cipher(29).get_shift(), 3)
        self.assertEqual(Cipher(26).encrypt("hello"), "hello")

    def test_invalid_shift_rejected(self):
        for bad in ["3", 2.5, None, True]:
            with self.subTest(shift=bad):
                with self.assertRaises(ValueError):
                    Cipher(bad)

    def test_non_string_text_rejected(self):
        with self.assertRaises(ValueError):
            self.cipher.encrypt(123)

    def test_encrypt_message(self):
        msg = Message("alice", "bob", "hello")
        self.cipher.encrypt_message(msg)
        self.assertEqual(msg.get_content(), "khoor")
        self.assertTrue(msg.is_encrypted())

    def test_decrypt_message(self):
        msg = Message("alice", "bob", "hello")
        self.cipher.encrypt_message(msg)
        self.cipher.decrypt_message(msg)
        self.assertEqual(msg.get_content(), "hello")
        self.assertFalse(msg.is_encrypted())

    def test_double_encrypt_rejected(self):
        msg = Message("alice", "bob", "hello")
        self.cipher.encrypt_message(msg)
        with self.assertRaises(ValueError):
            self.cipher.encrypt_message(msg)

    def test_decrypt_unencrypted_rejected(self):
        msg = Message("alice", "bob", "hello")
        with self.assertRaises(ValueError):
            self.cipher.decrypt_message(msg)

    def test_non_message_rejected(self):
        with self.assertRaises(ValueError):
            self.cipher.encrypt_message("just a string")


if __name__ == "__main__":
    unittest.main()