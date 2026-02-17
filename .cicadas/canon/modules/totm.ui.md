# Module: totm.ui

The `totm.ui` package manages the terminal interface and user interaction flow.

## Components

### 1. Console (`src/totm/ui/console.py`)
-   **`Console`**: The main application controller.
-   **Lifecycle**:
    -   `run()`: Main loop (Menu -> Game).
    -   `_main_menu()`: Options for New/Load/Save/Quit.
    -   `_game_loop()`: The play session.
-   **Integration**: Instantiates the Agent and routes user input to it.

### 2. Triggers (`src/totm/ui/triggers.py`)
-   **`TriggerParser`**: A regex-based intent detector.
-   **Purpose**: Maps common natural language queries (e.g., "where am i", "look around") directly to tool calls, bypassing the LLM for simple queries to save tokens and latency.

### 3. Formatting (`src/totm/ui/formatting.py`)
-   **Rich Text**: ANSI codes for `CYAN` (items), `YELLOW` (entities), `RED` (enemies).
-   **Helpers**: `print_gm`, `print_system`, `thinking_indicator`.

## Key Decisions
-   **Hybrid Input**: Supports both direct commands (`/look`) and natural language.
-   **Thinking Indicator**: Provides visual feedback during AI generation.
-   **Separation of Concerns**: UI handles display; Agent handles narration; Engine handles logic.
