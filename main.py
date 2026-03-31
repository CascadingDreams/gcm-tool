import subprocess
from git import get_staged_diff
from ai import generate_commit_message
import readline


def edit_message(message: str) -> str:
    readline.set_startup_hook(lambda: readline.insert_text(message))
    try:
        return input("Edit message: ").strip()
    finally:
        readline.set_startup_hook()


def main():
    # call get_staged_diff
    diff = get_staged_diff()

    # generate message and confirm
    message = generate_commit_message(diff)
    print(f"\n Suggested commit message:\n{message}\n")

    choice = input("[y/n] Commit with this message?").strip().lower()

    if choice == "y":
        subprocess.run(["git", "commit", "-m", message])
    elif choice == "n":
        edited = edit_message(message)
        subprocess.run(["git", "commit", "-m", edited])
        # pressing enter goes back into loop


if __name__ == "__main__":
    main()
