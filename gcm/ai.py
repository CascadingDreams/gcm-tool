"""AI integration module for gcm using the Anthropic SDK."""

import sys
import os
import anthropic
from dotenv import load_dotenv

MAX_DIFF_CHARS = 8000
DEFAULT_MODEL = "claude-sonnet-4-6"


def get_client() -> anthropic.Anthropic:
    """Load env and return an authenticated Anthropic client.

    Exits with code 1 if ANTHROPIC_API_KEY is not set.
    """
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("\033[31mError:\033[0m ANTHROPIC_API_KEY is not set.")
        print("  Add it to a .env file:  echo 'ANTHROPIC_API_KEY=sk-...' > .env")
        print("  Or export it:           export ANTHROPIC_API_KEY=sk-...")
        sys.exit(1)
    return anthropic.Anthropic(api_key=api_key)


def generate_commit_message(
    diff: str,
    commit_type: str = None,
    model: str = None,
    with_body: bool = False,
) -> str:
    """Generate a Conventional Commits message from a staged git diff.

    Args:
        diff: Output of `git diff --staged` as a string.
        commit_type: If set, forces the AI to use this type (e.g. "fix").
            Must be one of: feat, fix, refactor, chore, docs, test.
        model: Claude model ID to use. Falls back to the GCM_MODEL env var,
            then claude-sonnet-4-6.
        with_body: If True, generate a subject line plus an extended body
            explaining the motivation behind the change.

    Returns:
        The generated commit message as a string.

    Raises:
        SystemExit: On missing API key or unrecoverable API error.
    """
    model = model or os.getenv("GCM_MODEL", DEFAULT_MODEL)
    client = get_client()

    if len(diff) > MAX_DIFF_CHARS:
        diff = diff[:MAX_DIFF_CHARS] + "\n\n... [diff truncated to fit context window]"

    type_rule = (
        f"You MUST use the type '{commit_type}'"
        if commit_type
        else "Use one of these types: feat, fix, refactor, chore, docs, test"
    )

    if with_body:
        format_instruction = (
            "Return the commit message in this exact format:\n"
            "<type>: <short description>\n\n"
            "<body: 2-4 sentences explaining WHY this change was made, the motivation or context — not just what changed>\n\n"
            "Return ONLY the commit message, nothing else."
        )
    else:
        format_instruction = "Return ONLY the single-line commit message, nothing else."

    prompt = f"""You are a helpful assistant that writes concise, conventional git commit messages.

Given the following git diff, generate a commit message following the Conventional Commits format:
<type>: <short description>

Rules:
- {type_rule}
- The short description must be under 72 characters
- Use the imperative mood ("add", not "adds" or "added")
- Do not include a period at the end
- {format_instruction}

Git diff:
{diff}"""

    try:
        response = client.messages.create(
            model=model,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()
    except anthropic.AuthenticationError:
        print("\033[31mAuthentication error:\033[0m Invalid or expired API key.")
        print("Check your ANTHROPIC_API_KEY at https://console.anthropic.com/")
        sys.exit(1)
    except anthropic.APIError as e:
        print(f"\033[33mAPI error:\033[0m {e}")
        retry = input("Retry? [y/n] ").strip().lower()
        if retry == "y":
            response = client.messages.create(
                model=model,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text.strip()
        sys.exit(1)
