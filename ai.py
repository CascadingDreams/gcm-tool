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
        model="claude-opus-4-6"
    )
    return message.content[0].text

if __name__ == "__main__":
    test_diff = """
diff --git a/test.py b/test.py
index e69de29..b6fc4c6 100644
--- a/test.py
+++ b/test.py
@@ -0,0 +1,2 @@
+def hello():
+    print("hello world")
"""
    print(generate_commit_message(test_diff))