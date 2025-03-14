"""Tests for the tools command-line utility."""

from unittest.mock import patch

# Import pytest but handle the case where it might not be installed
try:
    import pytest
except ImportError:
    pytest = None  # type: ignore

from akaihola_tools.tools import main


def test_main_no_args(capsys):
    """Test that main() with no arguments lists tools."""
    main([])  # Empty list of arguments

    captured = capsys.readouterr()
    assert "Available tools:" in captured.out
    assert "github_clone_dev" in captured.out


def test_main_with_list_flag(capsys):
    """Test that main() with --list flag lists tools."""
    main(["--list"])  # --list flag

    captured = capsys.readouterr()
    assert "Available tools:" in captured.out
    assert "github_clone_dev" in captured.out


@patch("akaihola_tools.tools.subprocess.run")
def test_main_with_tool_name(mock_run):
    """Test that main() with a tool name runs that tool."""
    main(["github_clone_dev"])

    # Verify subprocess.run was called with expected arguments
    mock_run.assert_called_once()
    call_args = mock_run.call_args[0][0]  # Get the first positional argument
    assert call_args[0:2] == ["uv", "run"]
    assert "github_clone_dev.py" in str(
        call_args[2]
    )  # Tool file path should contain the tool name
