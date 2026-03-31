# gcm — AI Git Commit Messages

`gcm` is a CLI tool that uses Claude AI to generate [Conventional Commits](https://www.conventionalcommits.org/)-style commit messages from your staged changes. Stage your files, run `gcm`, review the suggestion, and commit — all in seconds.

---

## How it works

1. Reads your staged diff (`git diff --staged`)
2. Sends it to Claude to generate a commit message
3. Shows you the suggestion (with color highlighting)
4. You accept it, edit it inline, or cancel

---

## Requirements

- Python 3.10+
- Git installed and on your PATH
- An [Anthropic API key](https://console.anthropic.com/)

---

## Installation

### Option A — pipx (recommended for global use)

[pipx](https://pipx.pypa.io/) installs CLI tools in isolated environments without polluting any project virtualenv.

```bash
pipx install git+https://github.com/your-username/gcm-tool.git
```

### Option B — pip in a virtual environment

```bash
git clone https://github.com/your-username/gcm-tool.git
cd gcm-tool
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
pip install -e .
```

---

## Configuration

### API key (required)

Get your key at [console.anthropic.com](https://console.anthropic.com/), then either:

**Option 1 — `.env` file** (per-project):
```bash
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

**Option 2 — shell profile** (global, recommended):
```bash
# Add to ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY=sk-ant-...
```

### Model (optional)

By default `gcm` uses `claude-sonnet-4-6`. Override with the `GCM_MODEL` env var:

```bash
export GCM_MODEL=claude-opus-4-6   # more capable, slower
export GCM_MODEL=claude-haiku-4-5-20251001  # faster, cheaper
```

Or pass it per-run with `--model`.

---

## Usage

```bash
# Stage your changes as usual
git add .

# Run gcm
gcm
```

You'll see something like:

```
  Suggested commit message:
  feat: add user authentication with JWT tokens

[y/n/e] Commit? (e to edit)
```

- **`y`** — commit immediately with the suggested message
- **`e`** — open an inline editor pre-filled with the suggestion, then commit on Enter
- **`n`** — abort, nothing is committed

---

## Flags

| Flag | Description |
|------|-------------|
| `--dry-run` | Show the suggested message without committing |
| `--copy` | Copy the suggested message to clipboard instead of committing |
| `--push` | Run `git push` automatically after a successful commit |
| `--type TYPE` | Force a specific commit type (`feat`, `fix`, `refactor`, `chore`, `docs`, `test`) |
| `--model MODEL` | Claude model to use (overrides `GCM_MODEL` env var) |
| `--body` | Generate an extended commit body explaining the motivation behind the change |

### Examples

```bash
# Preview what gcm would suggest without committing
gcm --dry-run

# Force the type when you know it
gcm --type fix

# Commit and push in one step
gcm --push

# Get a full commit with subject + body
gcm --body

# Copy the message to clipboard (e.g. for use in a GUI)
gcm --copy

# Use a specific model for this run
gcm --model claude-opus-4-6
```

---

## Commit message format

`gcm` strictly follows the [Conventional Commits](https://www.conventionalcommits.org/) standard:

```
<type>: <short description>
```

With `--body`:

```
<type>: <short description>

<2–4 sentences explaining the motivation and context>
```

| Type | When to use |
|------|-------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `refactor` | Code change that isn't a fix or feature |
| `chore` | Maintenance, tooling, dependencies |
| `docs` | Documentation only changes |
| `test` | Adding or updating tests |

Rules enforced by the AI:
- Description under 72 characters
- Imperative mood ("add", not "adds" or "added")
- No period at the end

---

## Shell completions

`gcm` supports tab completion via [argcomplete](https://kislyuk.github.io/argcomplete/).

**One-time setup** — add this to your `~/.bashrc` or `~/.zshrc`:

```bash
eval "$(register-python-argcomplete gcm)"
```

Then restart your shell. You'll get tab completion for all flags.

---

## Project structure

```
gcm-tool/
├── gcm/
│   ├── main.py     # CLI entry point, argument parsing, user interaction
│   ├── ai.py       # Claude API integration
│   └── git.py      # Git diff utilities
├── pyproject.toml  # Package config and dependencies
└── .env            # Your API key (not committed)
```

---

## Troubleshooting

**`ANTHROPIC_API_KEY is not set`**
→ See [Configuration](#configuration) above. The key must be set before running `gcm`.

**`Nothing staged. Run git add . first.`**
→ Stage your changes with `git add <files>` before running `gcm`.

**`Not inside a git repository.`**
→ Run `gcm` from inside a git repo (`git init` if needed).

**API errors**
→ `gcm` will offer a retry on API failures. If it keeps failing, check your key and network connection.

**Clipboard not working (`--copy`)**
→ On Linux you may need `xclip` or `xsel`: `sudo apt install xclip`
