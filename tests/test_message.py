import os
import sys
import unittest
from datetime import datetime

#Let the tests find message.py in the src/ folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from message import Message

class TestMessage(unittest.TestCase):

    def setUp(self):
        self.msg = Message("alice", "bob", "hello there")

    def test_getters(self):
        self.assertEqual(self.msg.get_sender(), "alice")
        self.assertEqual(self.msg.get_recipient(), "bob")
        self.assertEqual(self.msg.get_content(), "hello there")
        self.assertFalse(self.msg.is_encrypted())
        self.assertIsInstance(self.msg.get_timestamp(), datetime)

    def test_empty_sender_rejected(self):
        with self.assertRaises(ValueError):
            Message("", "bob", "hi")

    def test_empty_recipient_rejected(self):
        with self.assertRaises(ValueError):
            Message("alice", "   ", "hi")

    def test_username_with_space_rejected(self):
        with self.assertRaises(ValueError):
            Message("al ice", "bob", "hi")

    def test_username_starting_with_digit_rejected(self):
        with self.assertRaises(ValueError):
            Message("alice", "1bob", "hi")

    def test_non_ascii_username_rejected(self):
        with self.assertRaises(ValueError):
            Message("alicé", "bob", "hi")

    def test_non_string_username_rejected(self):
        with self.assertRaises(ValueError):
            Message(42, "bob", "hi")

    def test_empty_content_rejected(self):
        with self.assertRaises(ValueError):
            Message("alice", "bob", "")

    def test_non_string_rejected(self):
        with self.assertRaises(ValueError):
            Message("alice", "bob", 123)

    def test_set_content(self):
        self.msg.set_content("khoor wkhuh", encrypted=True)
        self.assertEqual(self.msg.get_content(), "khoor wkhuh")
        self.assertTrue(self.msg.is_encrypted())

    def test_set_content_empty_rejected(self):
        with self.assertRaises(ValueError):
            self.msg.set_content("")

    def test_dict_round_trip(self):
        copy = Message.from_dict(self.msg.to_dict())
        self.assertEqual(copy.get_sender(), self.msg.get_sender())
        self.assertEqual(copy.get_recipient(), self.msg.get_recipient())
        self.assertEqual(copy.get_content(), self.msg.get_content())
        self.assertEqual(copy.get_timestamp(), self.msg.get_timestamp())
        self.assertEqual(copy.is_encrypted(), self.msg.is_encrypted())

    def test_str(self):
        text = str(self.msg)
        self.assertIn("alice -> bob: hello there", text)


if __name__ == "__main__":
    unittest.main()
 