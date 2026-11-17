"""
basic Caesar cipher: every letter is moved forward by a fixed
number of places in the alphabet. Digits, spaces and punctuation are left
alone. Later versions can build on this.
"""

import random
from message import Message


class Cipher:
    """Encrypts and decrypts text with a rotating caesar cipher.

    Attributes:
        shift (int): the base shift, stored as 0-25. If no shift is provided, a random shift is used.
    """

    ALPHABET_SIZE = 26
 
    def __init__(self, shift=None):
        if shift is None:
            shift = Cipher.random_shift()
        if not isinstance(shift, int) or isinstance(shift, bool):
            raise ValueError("shift must be an integer")
        # Reducing mod 26 gives exactly the same result, because every
        # letter's shift is (position * shift) mod 26.
        self._shift = shift % Cipher.ALPHABET_SIZE
 
    @staticmethod
    def random_shift():
        """Pick a random shift from 1-25.
 
        13 is skipped on purpose: 13 * 2 = 26, so every second letter
        would be left unchanged. 0 is skipped because it does nothing.
        """
        choices = [s for s in range(1, Cipher.ALPHABET_SIZE) if s != 13]
        return random.choice(choices)
 
    def get_shift(self):
        return self._shift
 
    # working with plain text
    def encrypt(self, text):
        """Return `text` with the rotating shift applied."""
        return self._rotate(text, self._shift)
 
    def decrypt(self, text):
        """Undo encrypt()."""
        return self._rotate(text, -self._shift)
 
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
    def _rotate(text, shift):
        if not isinstance(text, str):
            raise ValueError("text must be a string")
 
        result = []
        current_shift = shift
        for ch in text:
            if "a" <= ch <= "z":
                start = ord("a")
            elif "A" <= ch <= "Z":
                start = ord("A")
            else:
                result.append(ch)  # not a letter: leave it, don't advance
                continue
            position = (ord(ch) - start + current_shift) % Cipher.ALPHABET_SIZE
            result.append(chr(start + position))
            current_shift += shift  # next letter gets one more shift
        return "".join(result)