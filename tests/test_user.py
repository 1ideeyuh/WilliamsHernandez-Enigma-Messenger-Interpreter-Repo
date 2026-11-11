import os
import sys 
import unittest

# let the tests find user, message, and validator modules in src folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__),"..","src"))

from message import Message
from user import User

class TestUser(unittest.TestCase):

    def setUp(self):
        self.alice = User("alice")
        self.bob = User("bob")

    def test_username(self):
        self.assertEqual(self.alice.get_username(), "alice")
        self.assertEqual(str(self.alice), "alice")

    def test_invalid_usernames_rejected(self):
        for bad in ["", "al ice", "1bob", "alice123", 42, None]:
            with self.assertRaises(ValueError):
                User(bad)

    def test_send_message(self):
        msg = self.alice.send_message("bob", "hi bob")
        self.assertIsInstance(msg, Message)
        self.assertEqual(msg.get_sender(), "alice")
        self.assertEqual(msg.get_recipient(), "bob")
        self.assertEqual(self.alice.get_sent(), [msg])
 
    def test_send_to_self_rejected(self):
        with self.assertRaises(ValueError):
            self.alice.send_message("Alice", "talking to myself")
 
    def test_send_to_invalid_user_rejected(self):
        with self.assertRaises(ValueError):
            self.alice.send_message("not valid!", "hi")
 
    def test_receive_message(self):
        msg = self.alice.send_message("bob", "hi bob")
        self.bob.receive_message(msg)
        self.assertEqual(self.bob.get_inbox(), [msg])
 
    def test_receive_wrong_recipient_rejected(self):
        msg = self.alice.send_message("bob", "hi bob")
        carol = User("carol")
        with self.assertRaises(ValueError):
            carol.receive_message(msg)
 
    def test_receive_non_message_rejected(self):
        with self.assertRaises(ValueError):
            self.bob.receive_message("just a string")
 
    def test_inbox_copy_is_safe(self):
        msg = self.alice.send_message("bob", "hi bob")
        self.bob.receive_message(msg)
        self.bob.get_inbox().clear()
        self.assertEqual(len(self.bob.get_inbox()), 1)
 
    def test_conversation_is_in_order(self):
        first = self.alice.send_message("bob", "first")
        self.bob.receive_message(first)
        reply = self.bob.send_message("alice", "second")
        self.alice.receive_message(reply)
        third = self.alice.send_message("bob", "third")
 
        convo = self.alice.get_conversation("bob")
        self.assertEqual([m.get_content() for m in convo],
                         ["first", "second", "third"])
 
    def test_conversation_ignores_other_users(self):
        self.alice.send_message("bob", "for bob")
        self.alice.send_message("carol", "for carol")
        convo = self.alice.get_conversation("bob")
        self.assertEqual(len(convo), 1)
        self.assertEqual(convo[0].get_content(), "for bob")
 
    def test_usernames_not_case_sensitive(self):
        self.assertEqual(User("Alice"), User("alice"))
 
 
if __name__ == "__main__":
    unittest.main()