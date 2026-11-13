import subprocess

def run_git(command, cwd=r"c:\School\Projects\USAO-Enigma-Messenger-Repo"):
    subprocess.run(["git"] + command.split(), cwd = cwd, check=True)



if __name__ == "__main__":
    run_git("status")