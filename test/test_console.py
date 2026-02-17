"""Tests for Console logic (mocked)."""

import pytest
from unittest.mock import patch, MagicMock

from totm.ui.console import Console
from totm.engine.store import StateEngine
from totm.tools.api import ArbiterTools


@pytest.fixture
def mock_console():
    engine = MagicMock(spec=StateEngine)
    tools = MagicMock(spec=ArbiterTools)
    return Console(engine, tools)


class TestConsoleFlow:
    def test_create_character_flow(self, mock_console):
        # Mock inputs: Name="Test", Class="1" (Warrior)
        with patch("builtins.input", side_effect=["Test", "1", ""]):
            mock_console.tools.update_character.return_value = {
                "name": "Test", "char_class": "warrior", "hp": "10/10"
            }
            # Mock engine returning a stat just for the print statement
            mock_console.engine.character.primary_stat.return_value = ("brawn", 8)
            
            mock_console._create_character()
            
            mock_console.tools.update_character.assert_called_with("Test", "warrior")

    def test_play_game_no_character(self, mock_console):
        mock_console.engine.character = None
        with patch("totm.ui.console.print_error") as mock_err:
            mock_console._play_game()
            mock_err.assert_called_with("No character created! Go to 'Create Character' first.")
