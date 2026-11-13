import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cipher import Cipher
from message import Message


class TestCipher(unittest.TestCase):

    def setUp(self):
        self.cipher = Cipher(3)

    def test_letters_rotate_one_more_each_time(self):
        #a+3, b+6, c+9
        self.assertEqual(self.cipher.encrypt("abc"),"dhl")

    def test_wraps_around_alphabet(self):
        self.assertEqual(self.cipher.encrypt("xyz"), "aei")

    def test_keeps_case(self):
        self.assertEqual(self.cipher.encrypt("Hello"), "Kkuxd")

    def test_non_letters_unchanged_and_do_not_advance(self):
        self.assertEqual(self.cipher.encrypt("hi, bob! 42"), "ko, kaq! 42")
        self.assertEqual(self.cipher.encrypt("a b"), "d h")

    def test_decrypt_reverses_encrypt(self):
        text = "Meet me at 5pm, Alice!"
        self.assertEqual(self.cipher.decrypt(self.cipher.encrypt(text)), text)

    def test_round_trip_for_every_shift(self):
        text = "The Quick Brown Fox, 123 jumps over the lazy dog."
        for shift in range(-30, 60):
            with self.subTest(shift=shift):
                c = Cipher(shift)
                self.assertEqual(c.decrypt(c.encrypt(text)), text)

    def test_negative_shift(self):
        self.assertEqual(Cipher(-1).encrypt("bcd"), "aaa")

    def test_shift_wraps_modulo_26(self):
        self.assertEqual(Cipher(29).get_shift(), 3)
        self.assertEqual(Cipher(29).encrypt("hello world"),
                         Cipher(3).encrypt("hello world"))
        self.assertEqual(Cipher(26).encrypt("hello"), "hello")

    def test_random_shift_in_range(self):
        for _ in range(200):
            shift = Cipher.random_shift()
            self.assertGreaterEqual(shift, 1)
            self.assertLessEqual(shift, 25)
            self.assertNotEqual(shift, 13)

    def test_default_shift_is_random_but_valid(self):
        c = Cipher()
        self.assertIn(c.get_shift(), range(1, 26))

    def test_invalid_shift_rejected(self):
        for bad in ["3", 2.5, True]:
            with self.subTest(shift=bad):
                with self.assertRaises(ValueError):
                    Cipher(bad)

    def test_non_string_text_rejected(self):
        with self.assertRaises(ValueError):
            self.cipher.encrypt(123)

    def test_encrypt_message(self):
        msg = Message("alice", "bob", "abc")
        self.cipher.encrypt_message(msg)
        self.assertEqual(msg.get_content(), "dhl")
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