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

> **Mac users:** macOS ships with Python 3.9 by default, which is below the required version. You will need to install Python 3.10+ via Homebrew or python.org before continuing.

### Installing Python

**Mac:**
```bash
# Option 1 — Homebrew (recommended)
brew install python@3.13

# Verify the version
python3.13 --version

# Option 2 — Download the installer from https://python.org/downloads/
```

**Windows:**
```powershell
# Option 1 — winget
winget install Python.Python.3.12

# Option 2 — Download the installer from https://python.org/downloads/
# During install, check "Add Python to PATH"
```

### Installing Git

**Mac:**
```bash
# Option 1 — Homebrew
brew install git

# Option 2 — Xcode Command Line Tools (installs git automatically)
xcode-select --install
```

**Windows:**
- Download and install from [git-scm.com](https://git-scm.com/download/win)
- During setup, leave all defaults — this adds `git` to your PATH

---

## Installation

### Option A — pipx (recommended for global use)

[pipx](https://pipx.pypa.io/) installs CLI tools in isolated environments so `gcm` works anywhere without affecting other projects.

**Mac:**
```bash
brew install pipx
pipx ensurepath
# Restart your terminal so the PATH update takes effect, then:
pipx install --python python3.13 git+https://github.com/CascadingDreams/gcm-tool.git
```

> If `python3.13` isn't found, use the full path: `--python /opt/homebrew/bin/python3.13`

**Windows:**
```powershell
pip install pipx
pipx ensurepath
# Restart your terminal, then:
pipx install git+https://github.com/CascadingDreams/gcm-tool.git
```

### Option B — pip in a virtual environment

**Mac / Linux:**
```bash
git clone https://github.com/CascadingDreams/gcm-tool.git
cd gcm-tool
python3.13 -m venv .venv
source .venv/bin/activate
pip install -e .
```

**Windows (Command Prompt):**
```cmd
git clone https://github.com/CascadingDreams/gcm-tool.git
cd gcm-tool
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

**Windows (PowerShell):**
```powershell
git clone https://github.com/CascadingDreams/gcm-tool.git
cd gcm-tool
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
```

> **Windows PowerShell note:** If you see an error about script execution being disabled, run:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## Configuration

### 1. Get your API key

Sign up at [console.anthropic.com](https://console.anthropic.com/) and create an API key.

### 2. Set your API key

**Option A — `.env` file** (good for venv installs, per-project):

> This only works if you installed via Option B (venv). If you used pipx, use Option B below instead — pipx installs gcm globally and there is no shared project folder.

```bash
cp .env.example .env        # Mac / Linux
copy .env.example .env      # Windows Command Prompt
```

Then open `.env` in any text editor and replace `sk-ant-...` with your real key:

```
ANTHROPIC_API_KEY=sk-ant-your-real-key-here
```

**Option B — environment variable** (recommended for pipx users, works globally):

Mac / Linux — add to `~/.zshrc` or `~/.bashrc`:
```bash
export ANTHROPIC_API_KEY=sk-ant-your-real-key-here
```
Then reload: `source ~/.zshrc`

Windows — set permanently via Command Prompt (run as Administrator):
```cmd
setx ANTHROPIC_API_KEY "sk-ant-your-real-key-here"
```
Or via PowerShell:
```powershell
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-your-real-key-here", "User")
```
Then restart your terminal.

### 3. Choose a model (optional)

By default `gcm` uses `claude-sonnet-4-6`. You can override this:

**Mac / Linux:**
```bash
export GCM_MODEL=claude-opus-4-6          # more capable, slower
export GCM_MODEL=claude-haiku-4-5-20251001  # faster, cheaper
```

**Windows:**
```cmd
setx GCM_MODEL "claude-opus-4-6"
```
Then restart your terminal for it to take effect.

Or pass it per-run with `--model` (works on all platforms):
```bash
gcm --model claude-opus-4-6
```

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

**Mac / Linux** — add to `~/.zshrc` or `~/.bashrc`:
```bash
eval "$(register-python-argcomplete gcm)"
```
Then restart your shell.

**Windows** — tab completion is not supported on Windows Command Prompt or PowerShell at this time.

---

## Project structure

```
gcm-tool/
├── gcm/
│   ├── main.py     # CLI entry point, argument parsing, user interaction
│   ├── ai.py       # Claude API integration
│   └── git.py      # Git diff utilities
├── tests/
│   └── test_gcm.py # Unit tests (no real API calls)
├── pyproject.toml  # Package config and dependencies
├── .env.example    # Template — copy to .env and add your key
└── .env            # Your API key (not committed, git-ignored)
```

---

## Testing

Tests are included and do not require a real API key — the Anthropic client is mocked.

Install the dev dependencies and run:

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

The test suite covers:
- API key validation (missing key exits cleanly, valid key is returned)
- Commit message generation (correct output, type enforcement, long diff truncation)
- Commit message formatting and ANSI colorization
- Git diff retrieval (staged changes, nothing staged, outside a repo)

---

## Uninstalling

**If installed with pipx (Mac / Windows):**
```bash
pipx uninstall gcm
```

**If installed with pip in a virtual environment:**

Mac / Linux:
```bash
# Delete the project folder — that's it
rm -r gcm-tool/
```

Windows (Command Prompt):
```cmd
rmdir /s gcm-tool
```

Windows (PowerShell):
```powershell
Remove-Item -Recurse gcm-tool
```

**Remove your API key (optional):**

If you set it in your shell profile (`~/.zshrc` or `~/.bashrc`), open the file and delete the `export ANTHROPIC_API_KEY=...` line, then run `source ~/.zshrc`.

If you set it on Windows with `setx`, remove it via PowerShell:
```powershell
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", $null, "User")
```
Or go to **System Properties → Environment Variables** and delete it from there.

---

## Troubleshooting

**`ANTHROPIC_API_KEY is not set`**
→ Follow the [Configuration](#configuration) steps above. Make sure the key is set in `.env` or your environment before running `gcm`.

**`Nothing staged. Run git add . first.`**
→ Stage your changes with `git add <files>` before running `gcm`.

**`Not inside a git repository.`**
→ Run `gcm` from inside a git repo (`git init` if needed).

**`gcm` not found after install**
→ Make sure pipx's bin directory is on your PATH. Run `pipx ensurepath` and restart your terminal. On Windows, you may need to restart your session entirely.

**Authentication error**
→ Your key may be invalid or expired. Regenerate it at [console.anthropic.com](https://console.anthropic.com/).

**Virtual environment not activating on Windows**
→ If `.venv\Scripts\activate` fails in PowerShell, you may need to allow local scripts to run. This only affects your user account, not the whole system:
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**API errors**
→ `gcm` will offer a retry on API failures. If it keeps failing, check your key is correct and your network connection is working.

**Clipboard not working (`--copy`) on Linux**
→ Install `xclip` or `xsel`: `sudo apt install xclip`

**Clipboard not working (`--copy`) on Windows**
→ Clipboard should work out of the box. If not, ensure `pyperclip` is installed: `pip install pyperclip`
