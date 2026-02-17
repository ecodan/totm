"""Configuration loader for Agents and Prompts."""

import json
import os
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

# Constants
ASSETS_DIR = Path(__file__).parent.parent / "assets"
AGENTS_CONFIG_PATH = ASSETS_DIR / "agents.json"
PROMPTS_DIR = ASSETS_DIR / "prompts"


@dataclass
class ModelConfig:
    model_version: str
    model_provider: str
    temperature: float
    max_tokens: int
    api_key: str | None


@dataclass
class AgentConfig:
    model_config: ModelConfig
    system_prompt: str


class ConfigLoader:
    """Loads agents.json and resolves prompts."""

    def __init__(self) -> None:
        self._agents_data = self._load_json(AGENTS_CONFIG_PATH)

    def _load_json(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            raise FileNotFoundError(f"Config not found: {path}")
        return json.loads(path.read_text())

    def get_agent_config(self, agent_name: str) -> AgentConfig:
        """Build full config for an agent by name."""
        agent_def = self._agents_data.get(agent_name)
        if not agent_def:
            raise ValueError(f"Agent '{agent_name}' not defined in agents.json")

        model_id = agent_def["model_id"]
        prompt_ref = agent_def["prompt"]  # e.g., "gm:v1"

        # Resolve Model
        model_def = self._agents_data["_models"].get(model_id)
        if not model_def:
            raise ValueError(f"Model '{model_id}' not defined in _models")

        # Resolve API Key from env
        api_key_tmpl = model_def["provider_auth"]["api_key"]
        api_key = self._resolve_env_var(api_key_tmpl)

        model_config = ModelConfig(
            model_version=model_def["model_version"],
            model_provider=model_def["model_provider"],
            temperature=model_def["model_parameters"]["temperature"],
            max_tokens=model_def["model_parameters"]["max_tokens"],
            api_key=api_key
        )

        # Resolve Prompt
        system_prompt = self._load_prompt(prompt_ref)

        return AgentConfig(model_config=model_config, system_prompt=system_prompt)

    def _resolve_env_var(self, value: str) -> str | None:
        """Replace {{VAR}} with os.environ[VAR]."""
        if value.startswith("{{") and value.endswith("}}"):
            var_name = value[2:-2]
            return os.environ.get(var_name)
        return value

    def _load_prompt(self, ref: str) -> str:
        """Load prompt from TOML. Format: 'filename:version' or just 'filename'."""
        if ":" in ref:
            name, version = ref.split(":")
        else:
            name, version = ref, "latest"

        toml_path = PROMPTS_DIR / f"{name}.toml"
        if not toml_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {toml_path}")

        data = tomllib.loads(toml_path.read_text())
        
        if version == "latest":
            # Sort keys (v1, v2, v10) naturally? naive string sort for v1..v9 works
            # Better to just grab the explicitly requested one for now.
            # If 'latest', let's grab the last key in the file.
            # Keys are usually unordered in dict, but TOML preserves order? 
            # Let's assume keys are versions.
            versions = sorted(data.keys())
            if not versions:
                raise ValueError(f"No prompts in {toml_path}")
            version = versions[-1]

        if version not in data:
            raise ValueError(f"Version '{version}' not found in {toml_path}")

        return data[version]
