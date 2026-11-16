import os
import subprocess

from cipher import Cipher
from user import User
from validator import Validator

# UEMR is cloned NEXT TO this repo, not inside it:
UEMR_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "USAO-Enigma-Messenger-Repo")
)


# git helpers
def run_git(*args, folder=UEMR_FOLDER):
    """Run a git command inside `folder`. Raises CalledProcessError if it fails."""
    subprocess.run(["git", *args], cwd=folder, check=True)


def has_commits(folder=UEMR_FOLDER):
    """True if the repo in `folder` has at least one commit."""
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        cwd=folder,
        capture_output=True,
    )
    return result.returncode == 0


def pull_repo(folder=UEMR_FOLDER):
    """Download the newest messages. An empty shared repo is not an error."""
    try:
        run_git("pull", folder=folder)
    except subprocess.CalledProcessError:
        if has_commits(folder):
            raise  # a real problem (no internet, conflict, ...)
        print("Nothing to pull yet (the shared repo may still be empty).")


def push_repo(filename, folder=UEMR_FOLDER):
    """Save the updated message file to GitHub."""
    run_git("add", filename, folder=folder)
    run_git("commit", "-m", f"New message in {filename}", folder=folder)
    run_git("push", "-u", "origin", "HEAD", folder=folder)


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
def load_conversation(filename, folder=UEMR_FOLDER):
    """Return (decrypted_history, shift_used). A new conversation gives ("", None)."""
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        return "", None

    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

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


def save_conversation(filename, history, cipher, folder=UEMR_FOLDER):
    """Write the shift on line 1 and the encrypted conversation after it."""
    path = os.path.join(folder, filename)
    with open(path, "w", encoding="utf-8") as file:
        file.write(f"{cipher.get_shift()}\n{cipher.encrypt(history)}")


# main
def main(folder=UEMR_FOLDER):
    try:
        pull_repo(folder)
    except subprocess.CalledProcessError:
        print("Could not pull the shared repo. Check your internet and try again.")
        return

    me, other = ask_for_users()
    filename = Validator.filename(me, other)

    try:
        history, old_shift = load_conversation(filename, folder)
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

    save_conversation(filename, history, new_cipher(old_shift), folder)

    try:
        push_repo(filename, folder)
    except subprocess.CalledProcessError:
        print("Your message was saved on this computer but could not be pushed.")
        return
    print("Message sent!")


if __name__ == "__main__":
    main()