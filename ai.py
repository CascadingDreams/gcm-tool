import anthropic
from dotenv import load_dotenv
import os

def generate_commit_message(diff: str) -> str:
    '''
    arg: git diff --staged results as a string
    returns: generated commit message as a string
    '''
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        max_tokens=256,
        messages=[
            {"role": "user", "content": f"Generate a commit message for this diff:\n\n{diff}"}
        ],
        model="claude-sonnet-4-6"
    )
    return message.content[0].text
