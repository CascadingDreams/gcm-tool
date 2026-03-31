import subprocess
import sys

def get_staged_diff() -> str:
    """Return the staged diff as a string by running `git diff --staged`.

    Exits with code 1 if the working directory is not a git repository or
    if there are no staged changes.
    """
    result = subprocess.run(['git', 'diff', '--staged'], capture_output=True, text=True)
    if result.returncode != 0:
        print("Not inside a git repository.")
        sys.exit(1)
    if not result.stdout:
        print("Nothing staged. Run git add . first.")
        sys.exit(1)
    return result.stdout
