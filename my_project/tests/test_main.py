"""Tests for main module."""

import pytest
from my_project.main import main


def test_main(capsys):
    """Test that main runs without error."""
    main()
    captured = capsys.readouterr()
    assert "Hello from my_project!" in captured.out
