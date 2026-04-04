import pytest
from unittest.mock import MagicMock, patch


# ── validate_api_key ──────────────────────────────────────────────────────────

def test_validate_api_key_exits_when_missing():
    with patch.dict("os.environ", {}, clear=True):
        with patch("gcm.ai.load_dotenv"):
            from gcm.ai import validate_api_key
            with pytest.raises(SystemExit):
                validate_api_key()


def test_validate_api_key_returns_key_when_set():
    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "sk-ant-test"}):
        with patch("gcm.ai.load_dotenv"):
            from gcm.ai import validate_api_key
            assert validate_api_key() == "sk-ant-test"


# ── generate_commit_message ───────────────────────────────────────────────────

def test_generate_commit_message_returns_string():
    mock_response = MagicMock()
    mock_response.content[0].text = "feat: add login page"

    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "sk-ant-test"}):
        with patch("gcm.ai.load_dotenv"):
            with patch("anthropic.Anthropic") as mock_client:
                mock_client.return_value.messages.create.return_value = mock_response
                from gcm.ai import generate_commit_message
                result = generate_commit_message("diff --git a/foo.py")
                assert result == "feat: add login page"


def test_generate_commit_message_respects_commit_type():
    mock_response = MagicMock()
    mock_response.content[0].text = "fix: correct off-by-one error"

    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "sk-ant-test"}):
        with patch("gcm.ai.load_dotenv"):
            with patch("anthropic.Anthropic") as mock_client:
                mock_client.return_value.messages.create.return_value = mock_response
                from gcm.ai import generate_commit_message
                result = generate_commit_message("diff --git a/foo.py", commit_type="fix")
                assert result.startswith("fix:")


def test_generate_commit_message_truncates_long_diff():
    mock_response = MagicMock()
    mock_response.content[0].text = "chore: update config"

    long_diff = "x" * 10000

    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "sk-ant-test"}):
        with patch("gcm.ai.load_dotenv"):
            with patch("anthropic.Anthropic") as mock_client:
                mock_client.return_value.messages.create.return_value = mock_response
                from gcm.ai import generate_commit_message
                generate_commit_message(long_diff)
                call_args = mock_client.return_value.messages.create.call_args
                prompt = call_args.kwargs["messages"][0]["content"]
                assert "[diff truncated" in prompt


# ── colorize_message ──────────────────────────────────────────────────────────

def test_colorize_message_highlights_type():
    from gcm.main import colorize_message
    result = colorize_message("feat: add dark mode")
    assert "feat" in result
    assert "add dark mode" in result


def test_colorize_message_handles_no_type():
    from gcm.main import colorize_message
    result = colorize_message("just a plain message")
    assert "just a plain message" in result


def test_colorize_message_handles_body():
    from gcm.main import colorize_message
    result = colorize_message("feat: add thing\n\nsome body text")
    assert "feat" in result
    assert "some body text" in result


# ── get_staged_diff ───────────────────────────────────────────────────────────

def test_get_staged_diff_returns_diff():
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "diff --git a/foo.py b/foo.py\n+new line"

    with patch("gcm.git.subprocess.run", return_value=mock_result):
        from gcm.git import get_staged_diff
        assert "new line" in get_staged_diff()


def test_get_staged_diff_exits_when_nothing_staged():
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = ""

    with patch("gcm.git.subprocess.run", return_value=mock_result):
        from gcm.git import get_staged_diff
        with pytest.raises(SystemExit):
            get_staged_diff()


def test_get_staged_diff_exits_outside_git_repo():
    mock_result = MagicMock()
    mock_result.returncode = 128
    mock_result.stdout = ""

    with patch("gcm.git.subprocess.run", return_value=mock_result):
        from gcm.git import get_staged_diff
        with pytest.raises(SystemExit):
            get_staged_diff()
