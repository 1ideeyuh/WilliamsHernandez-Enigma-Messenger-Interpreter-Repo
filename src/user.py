from message import Message
from validator import Validator

class User:
    """A person using enigma messenger
    
    attributes:
    username: str
    sent (list): message objects this user has sent
    inbox(list): message objects this user has received
    """

    def __init__(self, username):
        if not Validator.is_valid(username):
            raise ValueError(f"Invalid username: {username!r}")
        self._username = username 
        self._sent = []
        self._inbox = []

# getters
    def get_username(self):
        return self._username

    def get_sent(self):
        """return a copy of the sent list so outside code cant change it"""
        return list(self._sent)

    def get_inbox(self):
        """return a copy of the inbox so outside code cant change it"""
        return list(self._inbox)

# sending and receiving messages
    def send_message(self, recipient, content):
        """create a message from this user to 'recipient' (a username str)
        
        the new message is saved in this users sent list and returned,
        so the caller can encrypt it, save it to a file, or deliver it"""

        if self._same_name(recipient, self._username):
            raise ValueError("Cannot send a message to yourself")
        message = Message(self._username, recipient, content)
        self._sent.append(message)
        return message

    def receive_message(self, message):
        """add a message to this user's inbox"""
        if not isinstance(message, Message):
            raise ValueError("receive_message needs a message object")
        if not self._same_name(message.get_recipient(), self._username):
            raise ValueError("This message is not addressed to this user")
        self._inbox.append(message)

    def get_conversation(self, other_username):
        """return a list of messages exchanged between this user and 'other_user',
        oldest first"""
        conversation = []
        for message in self._sent:
            if self._same_name(message.get_recipient(), other_username):
                conversation.append(message)
        for message in self._inbox:
            if self._same_name(message.get_sender(), other_username):
                conversation.append(message)
        return sorted(conversation, key=lambda message: message.get_timestamp())

# helper methods
    @staticmethod
    def _same_name(name_a, name_b):
        """usernames are not case sensitive (matches validator.filename)"""
        return (
            isinstance(name_a, str)
            and isinstance(name_b, str)
            and name_a.lower() == name_b.lower()
        )

    def __eq__(self, other):
        return isinstance(other, User) and self._same_name(
            self._username, other._username
        )

    def __hash__(self):
        return hash(self._username.lower())

    def __str__(self):
        return self._username