import subprocess
import sys

def get_staged_diff() -> str:
    '''
    Runs git diff --staged as subprocess and saves output as a string
    args: none
    returns: string of git diff --staged results
    '''
    result = subprocess.run(['git', 'diff', '--staged'], capture_output=True, text=True)
    if result.returncode != 0:
        print("Not inside a git repository.")
        sys.exit(1)
    if not result.stdout:
        print("Nothing staged. Run git add . first.")
        sys.exit(1)
    return result.stdout
