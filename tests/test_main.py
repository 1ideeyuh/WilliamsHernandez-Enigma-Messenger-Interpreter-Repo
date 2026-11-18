#uses temp folders, not real UEMR
import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import File
import Git
import main
from cipher import Cipher

def point_uemr_at(testcase, folder):
    """make file.py and git.py use 'folder' as the UEMR repo instead of the real one"""
    for module in (File, Git):
        patcher = patch.object(module, "UEMR_repo", folder)
        patcher.start()
        testcase.addCleanup(patcher.stop)

class TestHelpers(unittest.TestCase):

    def setUp(self):
        self.folder = tempfile.mkdtemp()
        self.addCleanup(shitil.rmtree, self.folder, ignore_errors=True)
        point_uemr_at(self, self.folder)

    def test_ask_for_users_returns_valid_names(self):
        with patch("builtins.input", side_effect=["alice", "bob"]):
            self.assertEqual(main.ask_for_users(), ("alice", "bob"))

    def test_ask_for_users_asks_again_after_bad_input(self):
        answers = ["al ice", "bob", "alice", "alice", "alice", "bob"]
        with patch("builtins.input", side_effect=answers), \
                redirect_stdout(io.StringIO()):
            self.assertEqual(main.ask_for_users(), ("alice", "bob"))

    def test_load_missing_file_gives_empty_history(self):
        self.assertEqual(main.load_conversation("alice-bob.txt", self.folder),
                         ("", None))

    def test_save_then_load_round_trip(self):
        main.save_conversation("alice-bob.txt", "alice: hi, 42!\n",
                               Cipher(7), self.folder)
        history, shift = main.load_conversation("alice-bob.txt", self.folder)
        self.assertEqual(history, "alice: hi, 42!\n")
        self.assertEqual(shift, 7)

    def test_saved_file_is_encrypted_and_has_shift_header(self):
        main.save_conversation("alice-bob.txt", "alice: hello\n",
                               Cipher(7), self.folder)
        with open(os.path.join(self.folder, "alice-bob.txt"), encoding="utf-8") as f:
            content = f.read()
        self.assertTrue(content.startswith("7\n"))
        self.assertNotIn("hello", content)

    def test_load_bad_header_rejected(self):
        with open(os.path.join(self.folder, "alice-bob.txt"), "w") as f:
            f.write("not a number\nsome text")
        with self.assertRaises(ValueError):
            main.load_conversation("alice-bob.txt", self.folder)

    def test_add_message_appends_line(self):
        history = main.add_message("alice: hi\n", "bob", "alice", "hello")
        self.assertEqual(history, "alice: hi\nbob: hello\n")

    def test_add_message_rejects_empty_text(self):
        with self.assertRaises(ValueError):
            main.add_message("", "alice", "bob", "   ")

    def test_new_cipher_differs_from_old_shift(self):
        for _ in range(200):
            self.assertNotEqual(main.new_cipher(5).get_shift(), 5)


@unittest.skipIf(shutil.which("git") is None, "git is not installed")
class TestWholeProgram(unittest.TestCase):
    """Runs main() against a temporary 'GitHub' (a local bare repo)."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.remote = os.path.join(self.tmp, "remote.git")

    def git(self, cwd, *args):
        subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)

    def make_remote(self, seeded=True):
        """A bare repo whose branch is called main. Seeded = has one commit."""
        remote = os.path.join(self.tmp, "remote.git")
        self.git(self.tmp, "init", "--bare", "--initial-branch=main", remote)
        if seeded:
            seed = self.clone(remote, "seed")
            with open(os.path.join(seed, "seed.txt"), "w") as f:
                f.write("seed")
            self.git(seed, "add", ".")
            self.git(seed, "commit", "-m", "Seed")
            self.git(seed, "push", "origin", "HEAD:main")
        return remote

    def clone(self, remote, name):
        folder = os.path.join(self.tmp, name)
        self.git(self.tmp, "clone", remote, folder)
        for key, value in [("user.name", "Test"), ("user.email", "t@example.com"),
                           ("commit.gpgsign", "false")]:
            self.git(folder, "config", key, value)
        return folder

    def run_main(self, remote, folder, answers):
        output = io.StringIO()
        with patch.object(File, "UEMR_repo", folder), \
                patch.object(Git, "UEMR_repo", folder), \
                patch("builtins.input", side_effect=answers), \
                redirect_stdout(output):
            main.main(remote)
        return output.getvalue()

    def read(self, folder, filename):
        with patch.object(File, "UEMR_repo", folder):
            return main.load_conversation(filename)

    def test_two_users_chat_through_the_shared_repo(self):
        remote = self.make_remote()
        alice_copy = self.clone(remote, "alice-copy")
        bob_copy = self.clone(remote, "bob-copy")  # cloned before alice writes

        self.run_main(remote, alice_copy, ["alice", "bob", "hello bob"])
        output = self.run_main(remote, bob_copy, ["bob", "alice", "hi alice"])

        self.assertIn("alice: hello bob", output)  # bob saw alice's message

        carol_copy = self.clone("carol-copy")
        history, _ = self.read(carol_copy, "alice-bob.txt")
        self.assertEqual(history, "alice: hello bob\nbob: hi alice\n")

    def test_shift_changes_every_time_a_message_is_saved(self):
        remote = self.make_remote()
        copy = self.clone(remote, "copy")
        self.run_main(copy, ["alice", "bob", "one"])
        _, first_shift = self.read(copy, "alice-bob.txt")
        self.run_main(remote, copy, ["alice", "bob", "two"])
        _, second_shift = self.read(copy, "alice-bob.txt")
        self.assertNotEqual(first_shift, second_shift)

    def test_empty_message_is_not_saved(self):
        remote = self.make_remote()
        copy = self.clone(remote, "copy")
        output = self.run_main(remote, copy, ["alice", "bob", "   "])
        self.assertIn("Message not sent", output)
        self.assertFalse(os.path.exists(os.path.join(copy, "alice-bob.txt")))


if __name__ == "__main__":
    unittest.main()
