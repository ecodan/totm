"""GMAgent Client — The AI brain powered by LiteLLM."""

import json
import logging
from typing import Any, Callable
import litellm

from totm.agent.config import ConfigLoader, AgentConfig
from totm.tools.api import ArbiterTools

# Logging setup
logger = logging.getLogger(__name__)

class GMAgent:
    """The Game Master Agent.
    
    Wraps an LLM client (via LiteLLM) and manages the conversation loop:
    User Input -> LLM -> Tool Calls -> Tool Execution -> LLM -> Response.
    """

    def __init__(self, tools: ArbiterTools, agent_name: str = "gm_agent") -> None:
        self.tools = tools
        self.config = ConfigLoader().get_agent_config(agent_name)
        self.history: list[dict[str, Any]] = []
        
        # Initialize history with system prompt
        self.history.append({
            "role": "system",
            "content": self.config.system_prompt
        })
        
        # Prepare tool definitions for LiteLLM
        self.tool_definitions = self._generate_tool_definitions()
        self.tool_map = self._generate_tool_map()

    def send(self, user_input: str) -> str:
        """Send a message to the agent and get the final response."""
        # Add user message
        self.history.append({"role": "user", "content": user_input})
        
        # Loop for tool use
        max_turns = 5
        for _ in range(max_turns):
            response = self._call_llm()
            message = response.choices[0].message
            
            # Append assistant message (even if tool calls)
            self.history.append(message.model_dump())
            
            if message.tool_calls:
                # Execute tools
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    logger.info(f"Tool Call: {function_name}({function_args})")
                    
                    # Execute
                    if function_name in self.tool_map:
                        result = self.tool_map[function_name](**function_args)
                    else:
                        result = {"error": f"Tool '{function_name}' not found."}
                        
                    # Append tool result
                    self.history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": json.dumps(result)
                    })
                # Loop again to let LLM see results and continue
            else:
                # No more tools, return final text
                return message.content or ""
                
        return "Thinking process timed out (too many tool calls)."

    def _call_llm(self):
        """Invoke LiteLLM."""
        kwargs = {}
        if self.config.model_config.api_key:
            kwargs["api_key"] = self.config.model_config.api_key
            
        return litellm.completion(
            model=self.config.model_config.model_version, # e.g. "gemini/gemini-pro" or just "gpt-4"
            messages=self.history,
            tools=self.tool_definitions,
            tool_choice="auto",
            temperature=self.config.model_config.temperature,
            max_tokens=self.config.model_config.max_tokens,
            **kwargs
        )

    def _generate_tool_map(self) -> dict[str, Callable]:
        """Map function names to methods on ArbiterTools."""
        return {
            "get_location": self.tools.get_location,
            "get_exits": self.tools.get_exits,
            "traverse": self.tools.traverse,
            "interact": self.tools.interact,
            "get_character": self.tools.get_character,
            "update_character": self.tools.update_character,
        }

    def _generate_tool_definitions(self) -> list[dict[str, Any]]:
        """Manual definitions for now. Reflection is brittle with decorators."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_location",
                    "description": "Get details about the current location (description, NPCs, items).",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_exits",
                    "description": "Get a list of available paths/exits from the current location.",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "traverse",
                    "description": "Move the character to a new location via a connected journey edge.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "journey_id": {"type": "string", "description": "The ID of the journey/edge to take."}
                        },
                        "required": ["journey_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "interact",
                    "description": "Interact with an NPC (talk, attack, etc).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "npc_id": {"type": "string", "description": "ID of the target NPC."},
                            "action": {"type": "string", "enum": ["talk", "attack"], "description": "Action to perform."}
                        },
                        "required": ["npc_id", "action"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_character",
                    "description": "Get the current character's status (HP, stats, inventory).",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_character",
                    "description": "Create or update the active character (Preparation Phase only).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "char_class": {"type": "string", "enum": ["warrior", "mage", "cleric", "thief"]},
                            "brawn": {"type": "integer"},
                            "brains": {"type": "integer"},
                            "faith": {"type": "integer"},
                            "speed": {"type": "integer"}
                        },
                        "required": ["name", "char_class"]
                    }
                }
            }
        ]
