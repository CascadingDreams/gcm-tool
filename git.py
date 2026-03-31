import subprocess

def get_staged_diff() -> str:
    '''
    Runs git diff --staged as subprocess and saves output as a string
    args: none
    returns: string of git diff --staged results
    '''
    result = subprocess.run(['git', 'diff', '--staged'], capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    print(get_staged_diff())