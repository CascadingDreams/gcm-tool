import argparse
import subprocess
import sys
import readline
from gcm.git import get_staged_diff
from gcm.ai import generate_commit_message

# ANSI codes
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
CYAN   = "\033[36m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
RED    = "\033[31m"


def colorize_message(message: str) -> str:
    """Apply ANSI colors to a commit message for terminal display.

    The commit type is colored cyan+bold, the description bold, and any
    extended body dim. Falls back to plain bold if the message has no
    conventional-commits type prefix.
    """
    lines = message.split("\n", 1)
    first = lines[0]
    if ": " in first:
        type_part, desc = first.split(": ", 1)
        first = f"{CYAN}{BOLD}{type_part}{RESET}: {BOLD}{desc}{RESET}"
    else:
        first = f"{BOLD}{first}{RESET}"
    if len(lines) > 1:
        return first + "\n" + DIM + lines[1] + RESET
    return first


def edit_message(message: str) -> str:
    """Open an inline readline editor pre-filled with the given message.

    Returns the edited string after the user presses Enter.
    The readline buffer is restored to its original state afterwards.
    """
    readline.set_startup_hook(lambda: readline.insert_text(message))
    try:
        return input("Edit message: ").strip()
    finally:
        readline.set_startup_hook()


def copy_to_clipboard(text: str) -> bool:
    """Copy text to the system clipboard using pyperclip.

    Returns True on success. Prints a helpful message and returns False if
    pyperclip is not installed or the clipboard is unavailable (e.g. no
    display server on headless Linux).
    """
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except ImportError:
        print(f"{YELLOW}Note:{RESET} pyperclip is not installed. Run: pip install pyperclip")
        return False
    except Exception as e:
        print(f"{YELLOW}Clipboard error:{RESET} {e}")
        return False


def do_commit(message: str, push: bool):
    """Run git commit with the given message, then optionally git push.

    push is only attempted if the commit exits with a zero return code.
    """
    result = subprocess.run(["git", "commit", "-m", message])
    if result.returncode == 0 and push:
        print(f"\n{DIM}Pushing...{RESET}")
        subprocess.run(["git", "push"])


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser for the gcm CLI."""
    parser = argparse.ArgumentParser(
        prog="gcm",
        description="AI-generated conventional git commit messages powered by Claude.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the suggested message without committing.",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy the suggested message to clipboard instead of committing.",
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Run git push automatically after a successful commit.",
    )
    parser.add_argument(
        "--type",
        metavar="TYPE",
        choices=["feat", "fix", "refactor", "chore", "docs", "test"],
        help="Force a specific commit type.",
    )
    parser.add_argument(
        "--model",
        metavar="MODEL",
        help="Claude model to use (overrides GCM_MODEL env var).",
    )
    parser.add_argument(
        "--body",
        action="store_true",
        help="Generate an extended commit body explaining the motivation.",
    )
    return parser


def main():
    """Entry point for the gcm CLI.

    Parses arguments, fetches the staged diff, generates a commit message
    via Claude, and drives the accept/edit/abort interaction.
    """
    parser = build_parser()
    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass

    args = parser.parse_args()

    diff = get_staged_diff()

    print(f"{DIM}Generating commit message...{RESET}", end="\r", flush=True)
    message = generate_commit_message(
        diff,
        commit_type=args.type,
        model=args.model,
        with_body=args.body,
    )
    print(" " * 35, end="\r")  # clear the status line

    print(f"\n  Suggested commit message:\n  {colorize_message(message)}\n")

    if args.dry_run:
        return

    if args.copy:
        if copy_to_clipboard(message):
            print(f"{GREEN}Copied to clipboard.{RESET}")
        return

    choice = input("[y/n/e] Commit? (e to edit) ").strip().lower()

    if choice == "y":
        do_commit(message, args.push)
    elif choice == "e":
        edited = edit_message(message)
        if not edited:
            print(f"{RED}Aborted:{RESET} commit message is empty.")
            sys.exit(1)
        do_commit(edited, args.push)
    else:
        print(f"{DIM}Aborted.{RESET}")


if __name__ == "__main__":
    main()
