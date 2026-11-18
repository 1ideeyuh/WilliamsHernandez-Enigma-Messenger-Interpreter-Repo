import os 

UEMR_repo = os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..", "USAO-Enigma-Messenger-Repo"))



def get_file_path(filename):
    """Get the absolute path to a file in the UEMR repository."""
    if not isinstance(filename, str) or not filename:
        raise ValueError("filename must be a non-empty string")
    return os.path.join(UEMR_repo, filename)

def file_exists(filename):
    """Check if a file exists in the UEMR repository."""
    if not filename.endswith(".txt"):
        raise ValueError("filename must end with .txt")
    return os.path.isfile(get_file_path(filename))

def read_file(filename):
    """Read the contents of a file in the UEMR repository."""
    if not os.path.isfile(get_file_path(filename)):
        raise FileNotFoundError(f"File not found: {filename}")
    with open(get_file_path(filename), 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filename, encrypted_content):
    """Write encrypted content to a file in the UEMR repository."""
    if not filename.endswith(".txt"):
        raise ValueError("filename must end with .txt")
    with open(get_file_path(filename), 'w', encoding='utf-8') as f:
        f.write(encrypted_content)

