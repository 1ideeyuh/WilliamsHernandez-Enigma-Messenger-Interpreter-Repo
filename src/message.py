from datetime import datetime
from validator import Validator

class Message:
    """A single message sent from one user to another.

    Attributes:
        sender (str): username of the person sending the message
        recipient (str): username of the person receiving the message
        content (str): the text of the message
        timestamp (datetime): when the message was created
        encrypted (bool): True if content is currently ciphertext
    """

    def __init__(self, sender, recipient, content, timestamp=None, encrypted=False):
        if not Validator.is_valid(sender):
            raise ValueError(f"Invalid sender username: {sender!r}")
        if not Validator.is_valid(recipient):
            raise ValueError(f"Invalid recipient username: {recipient!r}")
        if not isinstance(content, str) or not content.strip():
            raise ValueError("content must be a non-empty string")

        self._sender = sender
        self._recipient = recipient
        self._content = content
        self._timestamp = timestamp if timestamp is not None else datetime.now()
        self._encrypted = encrypted

    #getters
    def get_sender(self):
        return self._sender

    def get_recipient(self):
        return self._recipient

    def get_content(self):
        return self._content

    def get_timestamp(self):
        return self._timestamp

    def is_encrypted(self):
        return self._encrypted

    # setters
    def set_content(self, new_content, encrypted=False):
        """Replace the content (e.g. after a Cipher encrypts or decrypts it)."""
        if not isinstance(new_content, str) or not new_content.strip():
            raise ValueError("content must be a non-empty string")
        self._content = new_content
        self._encrypted = encrypted

    # saving / loading
    def to_dict(self):
        """Turn the message into a plain dictionary so it can be saved to a file."""
        return {
            "sender": self._sender,
            "recipient": self._recipient,
            "content": self._content,
            "timestamp": self._timestamp.isoformat(),
            "encrypted": self._encrypted,
        }

    @classmethod
    def from_dict(cls, data):
        """Rebuild a Message from a dictionary made by to_dict()."""
        return cls(
            sender=data["sender"],
            recipient=data["recipient"],
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            encrypted=data["encrypted"],
        )

    def __str__(self):
        time_text = self._timestamp.strftime("%Y-%m-%d %H:%M")
        return f"[{time_text}] {self._sender} -> {self._recipient}: {self._content}"