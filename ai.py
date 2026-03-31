import anthropic
from dotenv import load_dotenv
import os


def generate_commit_message(diff: str) -> str:
    """
    arg: git diff --staged results as a string
    returns: generated commit message as a string
    """
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        max_tokens=256,
        messages=[
            {
                "role": "user",
                "content": f"""You are a helpful assistant that writes concise, conventional git commit messages.

                Given the following git diff, generate a single commit message following the Conventional Commits format:
                <type>: <short description>

                Rules:
                - Use one of these types: feat, fix, refactor, chore, docs, test
                - Description must be under 72 characters
                - Use the imperative mood ("add", not "adds" or "added")
                - Do not include a period at the end
                - Return ONLY the commit message, nothing else

                Git diff:
                {diff}""",
            }
        ],
        model="claude-sonnet-4-6",
    )

    return message.content[0].text
