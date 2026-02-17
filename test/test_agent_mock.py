"""Tests for Agent logic (mocked)."""

import json
from unittest.mock import MagicMock, patch
import pytest

from totm.agent.client import GMAgent
from totm.tools.api import ArbiterTools
from totm.agent.config import AgentConfig, ModelConfig

@pytest.fixture
def mock_tools():
    return MagicMock(spec=ArbiterTools)

@pytest.fixture
def mock_config():
    return AgentConfig(
        model_config=ModelConfig(
            model_version="test-model",
            model_provider="test",
            temperature=0,
            max_tokens=100,
            api_key="sk-test"
        ),
        system_prompt="Test System Prompt"
    )

@patch("totm.agent.client.ConfigLoader")
@patch("totm.agent.client.litellm.completion")
def test_agent_tool_loop(mock_completion, MockConfigLoader, mock_tools, mock_config):
    # Setup Config
    mock_loader = MockConfigLoader.return_value
    mock_loader.get_agent_config.return_value = mock_config

    # Setup Tool Mock
    mock_tools.get_location.return_value = {"name": "Test Loc"}

    # Setup LLM Responses (Sequence)
    # 1. Output a tool call
    # 2. Output final response
    
    # Mocking LiteLLM response structure is verbose...
    tool_function = MagicMock()
    tool_function.name = "get_location"
    tool_function.arguments = "{}"
    
    tool_call_msg = MagicMock()
    tool_call_msg.content = None
    tool_call_msg.tool_calls = [
        MagicMock(id="call_1", function=tool_function)
    ]
    
    final_msg = MagicMock()
    final_msg.content = "You are in Test Loc."
    final_msg.tool_calls = None

    mock_completion.side_effect = [
        MagicMock(choices=[MagicMock(message=tool_call_msg)]),
        MagicMock(choices=[MagicMock(message=final_msg)])
    ]
    
    # Initialize Agent
    agent = GMAgent(mock_tools)
    
    # Act
    response = agent.send("Where am I?")
    
    # Assert
    assert response == "You are in Test Loc."
    
    # Verify tool execution
    mock_tools.get_location.assert_called_once()
    
    # Verify history accumulation
    # 0: system
    # 1: user
    # 2: assistant (tool call)
    # 3: tool result
    # 4: assistant (final)
    assert len(agent.history) == 5
    assert agent.history[3]["role"] == "tool"
    assert "Test Loc" in agent.history[3]["content"] 
