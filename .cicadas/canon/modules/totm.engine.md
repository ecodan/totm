# Module: totm.engine

The `totm.engine` package is the core domain model and simulation engine. It is strictly deterministic and stateless with respect to the AI agent.

## Components

### 1. Models (`src/totm/engine/models.py`)
-   **`Character`**: The player avatar. Stores `hp` (current/max), `xp`, and stats (`brawn`, `brains`, `faith`, `speed`).
-   **`Location`**: A node in the world graph. Contains `description`, `npcs` list, `inventory` list.
-   **`Journey`**: An edge connecting locations. Defined by `from_loc`, `to_loc`, `direction`, and difficulty tiers.
-   **`NPC`**: Non-player entities with specific behaviors (friendly/hostile) and stats.

### 2. World Graph (`src/totm/engine/graph.py`)
-   **`WorldGraph`**: A directed graph implementation managing `locations` (nodes) and `journeys` (edges).
-   **API**:
    -   `add_location(loc)`: Register a node.
    -   `add_journey(journey)`: Register an edge.
    -   `get_exits(loc_id)`: Return valid outgoing journeys.

### 3. State Engine (`src/totm/engine/store.py`)
-   **`StateEngine`**: The central controller.
-   **Responsibilities**:
    -   **Persistence**: Load/Save game state to JSON.
    -   **Adjudication**: Resolve player actions against game rules.
    -   **Traverse**: Roll `d20` + `stat` vs `difficulty`. On failure, apply damage.
    -   **Interact**: Combat/Social resolution.

## Key Decisions
-   **Graph-Based World**: Locations are nodes, travel is edges. This supports non-linear exploration.
-   **Stat Checks**: All mechanics are resolvable via simple d20 logic.
-   **No AI Dependency**: The engine runs independently of the LLM. AI is just a client.
