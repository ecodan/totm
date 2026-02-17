# Module: totm.agent

The `totm.agent` package implements the AI Game Master reasoning and communication layer.

## Components

### 1. Client (`src/totm/agent/client.py`)
-   **`GMAgent`**: The agent class.
-   **Core Loop**:
    1.  Receive User Input.
    2.  Append to Context History.
    3.  Call LLM (with Tools).
    4.  If Tool Call -> Execute -> Append Result -> Repeat.
    5.  If Text -> Return to User.

### 2. Configuration (`src/totm/agent/config.py`)
-   **`ConfigLoader`**: Reads `agents.json` and resolved keys/prompts.
-   **Assets**:
    -   `agents.json`: Model definitions (Gemini, Claude, GPT).
    -   `prompts/gm.toml`: Versioned system prompts.

## Key Decisions
-   **LiteLLM**: Used for model-agnostic support.
-   **Stateless**: The agent relies on tool calls for state, never internal memory of game state.
-   **Configuration Driven**: Models and prompts can be hot-swapped via config files without changing code.
