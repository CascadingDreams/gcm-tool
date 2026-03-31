import subprocess
from git import get_staged_diff
from ai import generate_commit_message


def main():
    # call get_staged_diff
    diff = get_staged_diff()
        
    # generate message and confirm
    while True:
        message = generate_commit_message(diff)
        print(f"\n Suggested commit message:\n{message}\n")
        
        choice = input("[y/n] Commit with this message?").strip().lower()
        
        if choice == "y":
            subprocess.run(["git", "commit", "-m", message])
            break
        elif choice == "n":
            custom = input("Enter your own message, or press Enter to regenerate.").strip()
            if custom:
                subprocess.run(["git", "commit", "-m", custom])
                break
            # pressing enter goes back into loop
            
if __name__ == "__main__":
    main()