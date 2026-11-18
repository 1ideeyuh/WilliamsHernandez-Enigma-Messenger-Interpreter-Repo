import File
import Git
import subprocess

from cipher import Cipher
from user import User
from validator import Validator

# UEMR is cloned NEXT TO this repo, not inside it:
UEMR_URL = "https://github.com/qtranokc/USAO-Enigma-Messenger-Repo.git"


# git 

def has_commits():
    """True if the UEMR clone has at least one commit."""
    result = subprocess.run(
        ["git", "-C", File.UEMR_repo, "rev-parse", "--verify", "HEAD"],
        capture_output=True,
    )
    return result.returncode == 0


def pull_repo(repo_url=UEMR_URL):
    """Download the newest messages. An empty shared repo is not an error."""
    try:
        Git.pull_uemr(repo_url)
    except RuntimeError:
        if has_commits():
            raise # a real problem, not just an empty repo
        print("Nothing to pull yet. The shared repo might be empty.")


# asking the user
def ask_for_users():
    """Ask for two usernames until Validator accepts them. Returns (me, other)."""
    while True:
        me = input("Your username: ")
        other = input("Who do you want to message? ")
        try:
            Validator.filename(me, other)  # raises ValueError if anything is wrong
            return me, other
        except ValueError as error:
            print(error)


# reading and writing
def load_conversation(filename):
    """Return (decrypted_history, shift_used). A new conversation gives ("", None)."""
    if not File.file_exists(filename):
        return "", None

    content = File.read_file(filename)
    header, _, body = content.partition("\n")  # split at the FIRST newline
    try:
        cipher = Cipher(int(header))
    except ValueError:
        raise ValueError(f"{filename} does not start with a shift number")
    return cipher.decrypt(body), cipher.get_shift()


def add_message(history, me, other, text):
    """Return `history` with a new "me: text" line added to the end."""
    message = User(me).send_message(other, text)  # checks the names and the text
    return history + f"{message.get_sender()}: {message.get_content()}\n"


def new_cipher(old_shift):
    """A Cipher with a random shift that is different from `old_shift`."""
    cipher = Cipher()
    while cipher.get_shift() == old_shift:
        cipher = Cipher()
    return cipher


def save_conversation(filename, history, cipher):
    """Write the shift on line 1 and the encrypted conversation after it."""
    File.write_file(filename,f"{cipher.get_shift()}\n{cipher.encrypt(history)}")



# main
def main(repo_url=UEMR_URL):
    try:
        pull_repo(repo_url)
    except RuntimeError:
        print("Could not pull the shared repo. Check your internet and try again.")
        return

    me, other = ask_for_users()
    filename = Validator.filename(me, other)

    try:
        history, old_shift = load_conversation(filename)
    except ValueError as error:
        print(error)
        return

    if history:
        print(history, end="")
    else:
        print("No messages yet. Start the conversation!")

    text = input("Your message: ")
    try:
        history = add_message(history, me, other, text)
    except ValueError as error:
        print(f"Message not sent: {error}")
        return

    save_conversation(filename, history, new_cipher(old_shift))

    try:
        Git.push_uemr(repo_url)
    except RuntimeError:
        print("Your message was saved on this computer but could not be pushed.")
        return
    print("Message sent!")


if __name__ == "__main__":
    main()