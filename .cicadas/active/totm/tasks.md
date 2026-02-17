# Tasks: TOTM (Theater of the Mind)

## Mode A: Foundation (Strict Phases)

---

### Partition 1: Data Models & State Engine → `feat/engine`

#### Phase 1: Data Models (Blocking)
- [x] Create `src/totm/engine/models.py`: Define `Character` class with archetypes (Warrior, Mage, Cleric, Thief), stats (brawn, brains, faith, speed, hp, xp), and JSON serialization <!-- id: 100 -->
- [x] Create `src/totm/engine/models.py`: Define `Location` node model (id, name, description, npcs, inventory, gm_guide) <!-- id: 101 -->
- [x] Create `src/totm/engine/models.py`: Define `Journey` edge model (from, to, direction, duration, difficulty, risks, description) <!-- id: 102 -->
- [x] Create `src/totm/engine/graph.py`: Implement `WorldGraph` class — add/get locations, add/get edges, neighbors, region scoping <!-- id: 103 -->

#### Phase 2: State Engine (Blocking)
- [x] Create `src/totm/engine/store.py`: Implement `StateEngine` — active character, current location, world graph reference <!-- id: 110 -->
- [x] Update `src/totm/engine/store.py`: Implement save/load persistence (JSON file) <!-- id: 111 -->
- [x] Update `src/totm/engine/store.py`: Implement deterministic `traverse` adjudication (stat check vs edge difficulty → result object) <!-- id: 112 -->
- [x] Update `src/totm/engine/store.py`: Implement `interact` adjudication for NPC encounters <!-- id: 113 -->

#### Phase 3: Prototype Data & Tests
- [x] Create `src/totm/engine/worlds/well.json`: Bootstrap prototype world graph (Well Bottom scenario) <!-- id: 120 -->
- [x] Create `test/test_models.py`: Unit tests for Character, Location, Journey serialization <!-- id: 121 -->
- [x] Create `test/test_graph.py`: Unit tests for WorldGraph traversal and neighbor lookups <!-- id: 122 -->
- [x] Create `test/test_engine.py`: Unit tests for StateEngine adjudication logic (traverse, interact) <!-- id: 123 -->
- [x] Create `test/test_engine.py`: Unit tests for save/load round-trip (included in test_engine.py) <!-- id: 124 -->

---

### Partition 2: Arbiter Tools → `feat/tools`

#### Phase 1: Tool API (Blocking)
- [x] Create `src/totm/tools/schema.py`: Define tool input/output schemas and result object format <!-- id: 200 -->
- [x] Create `src/totm/tools/api.py`: Implement `get_location()` — returns current location data with GM guide <!-- id: 201 -->
- [x] Update `src/totm/tools/api.py`: Implement `get_exits()` — returns connected edges with direction and risk labels <!-- id: 202 -->
- [x] Update `src/totm/tools/api.py`: Implement `traverse(edge_id)` — delegates to StateEngine, returns result object <!-- id: 203 -->
- [x] Update `src/totm/tools/api.py`: Implement `interact(npc_id, action)` — delegates to StateEngine, returns outcome <!-- id: 204 -->
- [x] Update `src/totm/tools/api.py`: Implement `update_character(stats)` — commits class and stats during Preparation Phase <!-- id: 205 -->

#### Phase 2: Tool Tests (Parallelizable)
- [x] Create `test/test_tools.py`: Unit tests for each tool (mock StateEngine, verify result schemas) <!-- id: 210 -->
- [x] Create `test/test_tools.py`: Integration tests — tools against a real StateEngine with prototype world (combined in test_tools.py) <!-- id: 211 -->

---

### Partition 3: Terminal UI & Game Flows → `feat/ui`

#### Phase 1: Shell (Blocking)
- [x] Create `src/totm/ui/console.py`: Implement terminal Main Menu (New, Load, Save, Create Character, Play) <!-- id: 300 -->
- [x] Create `src/totm/ui/triggers.py`: Implement Plain Text Trigger parser (intent → tool call mapping) <!-- id: 301 -->
- [x] Create `src/totm/ui/formatting.py`: Rich text utilities (colors, headers, GM/System/Error print helpers) <!-- id: 300 -->
- [x] Create `src/totm/ui/triggers.py`: Parser for plain text triggers (commands disguised as natural language) <!-- id: 301 -->
- [x] Create `src/totm/ui/console.py`: Main Menu loop (New/Load/Save/Quit) <!-- id: 302 -->
- [x] Update `src/totm/ui/console.py`: Implement Preparation Phase (Character Creation flow) <!-- id: 303 -->
- [x] Update `src/totm/ui/console.py`: Implement Gameplay Phase (Serial console loop, tool dispatch, narrative routing) <!-- id: 304 -->
- [x] Create `src/totm/app.py`: Application entry point (bootstraps Engine, Tools, UI) <!-- id: 305 -->

#### Phase 3: UI Tests
- [x] Create `test/test_triggers.py`: Unit tests for intent parsing regex <!-- id: 310 -->
- [x] Create `test/test_console.py`: Unit tests for shell logic (mocked engine/tools) <!-- id: 311 -->

---

### Partition 4: GM Agent & Knowledge → `feat/agent`

#### Phase 1: GM Core (Blocking)
- [x] Create `src/totm/assets/agents.json`: Define model configs (Gemini, Claude, GPT) and default agent version <!-- id: 400 -->
- [x] Create `src/totm/assets/prompts/gm.toml`: Define versioned System Prompts (v1) <!-- id: 401 -->
- [x] Create `src/totm/agent/config.py`: Utilities to load `agents.json` and resolve TOML prompts <!-- id: 402 -->
- [x] Create `src/totm/agent/__init__.py`: Package init <!-- id: 403 -->
- [x] Create `src/totm/agent/client.py`: Implement `GMAgent` class using `litellm` (chat loop, tool execution, history) <!-- id: 404 -->
- [x] Update `src/totm/ui/console.py`: Wire Agent into the shell (narrative input routing) <!-- id: 405 -->
- [x] Update `src/totm/app.py`: Initialize Agent with config and pass to UI <!-- id: 406 -->
- [x] Create `test/test_agent_mock.py`: Unit tests for `GMAgent` tool loop (mocking `litellm`) <!-- id: 407 -->
