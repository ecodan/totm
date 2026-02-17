# UX Overview

**TOTM** uses a terminal-based interface designed to evoke the feeling of classic text adventures (Zork) but with the fluidity of a modern conversation.

## Design Principles
1.  **Immersion First**: The interface disappears. Focus on the narrative text.
2.  **System vs. Story**: Clearly distinguish between mechanical outputs (HP lost, items gained) and narrative descriptions.
3.  **Conversational Input**: Players type natural actions ("Check the chest", "Attack the goblin"), not rigid keywords.

## User Flows

### 1. Preparation Phase (Character Creation)
A guided wizard where the user defines their avatar before entering the world.
-   **Input**: Name, Class Selection (Warrior, Mage, Cleric, Thief).
-   **Output**: Initial Character Sheet (HP, Stats).

### 2. Gameplay Loop
The core infinite loop of the game.
1.  **Narrative Output**: The GM describes the current scene.
2.  **User Input**: The player types an action or question.
3.  **Processing**: The system displays a "Thinking..." indicator.
4.  **Result**: The GM narrates the outcome.

## Interface Elements
-   **The Stage**: The main text area where the story unfolds.
-   **System Messages**: bracketed text (e.g., `[SYSTEM] Saved Game`) for meta-information.
-   **The Prompt**: A simple cursor `> ` waiting for user command.
-   **Rich Text**: Usage of ANSI colors to highlight entities (Yellow), enemies (Red), and items (Cyan).
