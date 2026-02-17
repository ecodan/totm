# Module: totm.tools

The `totm.tools` package provides the Arbiter API — a bridge between the probabilistic AI agent and the deterministic Engine.

## Components

### 1. Schema (`src/totm/tools/schema.py`)
-   **`LocationInfo`**: Structured view of the current location (desc, NPCs, exits).
-   **`TraverseResult`**: Outcome of a movement attempt (success bool, damage taken, new location).
-   **`InteractResult`**: Outcome of NPC interaction (dialogue or combat damage).
-   **`CharacterInfo`**: Current stats snapshot.

### 2. API (`src/totm/tools/api.py`)
-   **`ArbiterTools`**: The facade class.
-   **Methods**:
    -   `get_location()`: Returns context for the GM description.
    -   `get_exits()`: Returns available paths for player decision.
    -   `traverse(journey_id)`: Executes movement logic.
    -   `interact(npc_id, action)`: Resolves social/combat encounters.
    -   `update_character(...)`: Initializes stats (Prep Phase only).

## Key Decisions
-   **GM-Friendly Output**: Tool results include textual "GM Guides" (hidden from player) to help the AI narrate.
-   **Safety**: Tools handle all engine exceptions and return structured error objects, preventing agent crashes.
