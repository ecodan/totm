# Tasks: TOTM (Theater of the Mind)

## 0. Project Scaffolding
- [ ] Initialize project structure following the `src/totm` namespace.
- [ ] Create core packages in `src/totm`: `engine`, `tools`, `agent`, `ui`.
- [ ] Create `test/` directory for automated verification.
- [ ] Add `__init__.py` to all packages in `src/totm` and to `test/`.
- [ ] Verify project can be imported (test/smoke setup).

## 1. Project Infrastructure & Data Models
- [ ] Initialize Python project structure in `src/totm/`.
- [ ] Implement `Character` class (Warrior, Mage, Cleric, Thief) with JSON serialization.
- [ ] Implement `Location` node model (Description, NPCs, GM Guide, Inventory).
- [ ] Implement `Journey` edge model (Direction, Duration, Difficulty, Risks).
- [ ] Implement `WorldGraph` to manage regions and location traversal.

## 2. State Engine (Solid Ground)
- [ ] Create `StateEngine` for managing active character, current location, and world persistence.
- [ ] Implement `Save/Load` functionality for game states.
- [ ] Implement deterministic adjudication logic for `traverse` (Stat checks vs Edge difficulty).
- [ ] Implement `interact` logic for NPC encounters.

## 3. Arbiter Tools
- [ ] Interface `get_location()` tool with the State Engine.
- [ ] Interface `get_exits()` tool with the State Engine.
- [ ] Interface `traverse(edge_id)` tool (returning success/fail/cost result).
- [ ] Interface `update_character(stats)` tool for character creation.

## 4. Shell & Interaction (The Console)
- [ ] Implement terminal-based Main Menu (New, Load, Save, Create, Play).
- [ ] Implement the "Serial Console" for the Gameplay Phase.
- [ ] Implement Plain Text Trigger parser (mapping natural language to slash commands).
- [ ] Add "Thinking..." indicators and rich text formatting for GM output.

## 5. Game Flows
- [ ] Implement **Preparation Phase**: Narrative-driven character setup flow.
- [ ] Implement **Gameplay Phase**: Main loop with GM narration and state-narrative injection.
- [ ] Implement **Epoch System**: Automated summarization and granular logging.

## 6. AI & Knowledge (The GM)
- [ ] Standardize the GM System Prompt (Persona, Constraints, Tool usage).
- [ ] Integrate Rulebook RAG (Retriever for dynamic rule reference).
- [ ] Implement context injection logic: Building the context window from current SE state.

## 7. Verification & Polish
- [ ] Unit tests for Graph traversal and Stat checks.
- [ ] Integration tests for Tool-Agent round-trips.
- [ ] Manual walkthrough of a "Sample Encounter" (Well Bottom).
