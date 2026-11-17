import os
import subprocess

UEMR_repo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "USAO-Enigma-Messenger-Repo"))  # Path to the UEMR folder

def pull_uemr(repo_url):
    """Pull the latest changes from the UEMR repository."""
    try:
        subprocess.run(["git", "-C", str(UEMR_repo), "pull", repo_url,  'main'], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to pull from {repo_url}: {e}")
def push_uemr(repo_url):
    """Push local changes to the UEMR repository."""
    try:
        subprocess.run(["git", "-C", str(UEMR_repo), "add", "--all"], check=True)
        status = subprocess.run(["git", "-C", str(UEMR_repo), "status"], capture_output=True, text=True)
        if "nothing to commit" in status.stdout:
            print("No changes to commit.")
            return
        subprocess.run(["git", "-C", str(UEMR_repo), "commit", "-m", "Update"], check=True)
        subprocess.run(["git", "-C", str(UEMR_repo), "pull",  '--rebase', repo_url, "main"], check=True)
        subprocess.run(["git", "-C", str(UEMR_repo), "push", repo_url, "main"], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to push to {repo_url}: {e}")
