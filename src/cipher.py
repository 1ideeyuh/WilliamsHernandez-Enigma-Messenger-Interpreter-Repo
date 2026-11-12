"""
basic Caesar cipher: every letter is moved forward by a fixed
number of places in the alphabet. Digits, spaces and punctuation are left
alone. Later versions can build on this.
"""

from message import Message


class Cipher:
    """Encrypts and decrypts text with a Caesar shift.

    Attributes:
        shift (int): how many places to move each letter (stored as 0-25)
    """

    ALPHABET_SIZE = 26

    def __init__(self, shift=3):
        if not isinstance(shift, int) or isinstance(shift, bool):
            raise ValueError("shift must be an integer")
        self._shift = shift % Cipher.ALPHABET_SIZE

    def get_shift(self):
        return self._shift

    # working with plain text
    def encrypt(self, text):
        """Return `text` with every letter shifted forward."""
        return self._shift_text(text, self._shift)

    def decrypt(self, text):
        """Undo encrypt(): shift every letter backward."""
        return self._shift_text(text, -self._shift)

    # working with Message objects 
    def encrypt_message(self, message):
        """Encrypt a Message's content in place and mark it as encrypted."""
        self._check_message(message)
        if message.is_encrypted():
            raise ValueError("Message is already encrypted")
        message.set_content(self.encrypt(message.get_content()), encrypted=True)
        return message

    def decrypt_message(self, message):
        """Decrypt a Message's content in place and mark it as not encrypted."""
        self._check_message(message)
        if not message.is_encrypted():
            raise ValueError("Message is not encrypted")
        message.set_content(self.decrypt(message.get_content()), encrypted=False)
        return message

    # helpers
    @staticmethod
    def _check_message(message):
        if not isinstance(message, Message):
            raise ValueError("Expected a Message object")

    @staticmethod
    def _shift_text(text, shift):
        if not isinstance(text, str):
            raise ValueError("text must be a string")

        result = []
        for ch in text:
            if "a" <= ch <= "z":
                start = ord("a")
            elif "A" <= ch <= "Z":
                start = ord("A")
            else:
                result.append(ch)  # not a letter, leave it alone
                continue
            position = (ord(ch) - start + shift) % Cipher.ALPHABET_SIZE
            result.append(chr(start + position))
        return "".join(result)