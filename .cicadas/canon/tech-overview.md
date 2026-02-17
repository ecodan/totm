# Technical Overview

TOTM is built on a **Modular Monolith** architecture, separating the deterministic game engine from the probabilistic AI agent.

## Architecture

```mermaid
graph TD
    User[User] <--> UI[UI Shell (Console)]
    UI <--> Agent[GM Agent (LiteLLM)]
    Agent <--> Tools[Arbiter Tools (API)]
    Tools <--> Engine[State Engine]
    Engine <--> Graph[World Graph]
```

### Components

#### 1. Engine (`src/totm/engine`)
The source of mechanical truth.
-   **Models**: Pydantic/Dataclass models for `Character`, `Location`, `Journey`, `NPC`.
-   **WorldGraph**: A directed graph representing the map connectivity.
-   **StateEngine**: Manages the simulation loop, persistence, and rule adjudication (dice rolls).

#### 2. Tools (`src/totm/tools`)
The API layer exposed to the Agent.
-   **ArbiterTools**: Facade providing GM-friendly methods (`get_location`, `traverse`, etc.).
-   **Schemas**: Input/Output definitions optimized for LLM consumption.

#### 3. Agent (`src/totm/agent`)
The AI brain.
-   **GMAgent**: Orchestrates the conversation loop.
-   **LiteLLM**: Provides model-agnostic LLM access (Gemini, Claude, GPT).
-   **Config**: Externalized configuration (`agents.json`, `gm.toml`).

#### 4. UI (`src/totm/ui`)
The presentation layer.
-   **Console**: Handles the read-eval-print loop.
-   **Triggers**: Heuristic parser for intent detection.
-   **Formatting**: ANSI text styling.

## Key Decisions
-   **Orchestration**: The Agent runs in a loop *inside* the UI, calling tools and feeding results back into context before outputting final narration.
-   **Persistence**: Game state is serialized to JSON (`save_game.json`), ensuring sessions can be resumed exactly where left off.
-   **Stateless Agent**: The agent holds conversation history but relies on the Engine for game state. It must always "look" to see.
