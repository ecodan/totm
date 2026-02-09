# Implementation Approach: TOTM (Theater of the Mind)

## Overview
The implementation of TOTM follows a "Solid Ground" philosophy, where the world state and mechanics are governed by a deterministic engine (the State Engine), while the narrative experience is woven by an AI Game Master (GM) that strictly observes and reacts to this engine.

## Core Strategy

### 1. Separation of Concerns
- **State Engine (SE)**: Authoritative source for characters, locations, and mechanics.
- **Arbiter Tools**: The bridge between the SE and the GM Agent.
- **GM Agent**: Responsible ONLY for narrative, persona, and interpreting player intent into tool calls.

### 2. Hierarchical Context Management
To maintain consistency without overwhelming the LLM, we use a lazy-loading strategy. The GM only "sees":
- The Current Location details.
- Immediate neighbors (Exit summaries).
- Relevant Character Stats.
- High-level Epoch summaries for long-term memory.

### 3. Tool-First Adjudication
The GM must never "roll dice" or decide success/failure. It must call `traverse` or `interact`, and the SE will return a result object. The GM's job is to "paint the picture" of that result.

## Development Phases

### Phase 0: Scaffolding
- Initialize project structure (package directories, `__init__.py` files).
- Set up core configuration (pyproject.toml/package.json).
- Define the `totm` namespace and internal package boundaries.
- **Proposed Structure**:
  ```text
  totm/
  ├── __init__.py
  ├── app.py              # Entry point
  ├── engine/             # State Engine & Data Models
  │   ├── __init__.py
  │   ├── models.py
  │   └── store.py
  ├── tools/              # Arbiter Tools (GM-to-Engine Bridge)
  │   ├── __init__.py
  │   └── api.py
  ├── agent/              # GM Persona & Context Logic
  │   ├── __init__.py
  │   └── persona.py
  └── ui/                 # Terminal Interface
      ├── __init__.py
      └── console.py
  ```

### Phase 1: Foundation (The Engine)
- Implement `Character`, `Location`, and `Journey` data models.
- Build the `StateEngine` class with persistence (JSON/SQLite).
- Develop the initial world graph for the prototype.

### Phase 2: Orchestration (Arbiter Tools)
- Implement the defined Arbiter Tools: `get_location`, `get_exits`, `traverse`, `interact`, `update_character`.
- Create unit tests for deterministic adjudication.

### Phase 3: The Theater (UI & Flow)
- Build the Terminal Main Menu.
- Implement the **Preparation Phase** flow (narrative character creation).
- Implement the **Gameplay Phase** serial console.

### Phase 4: Intelligence (GM Agent & RAG)
- Integrate the GM Agent with tools.
- Set up the Rulebook RAG system for dynamic rule reference.
- Implement the **Epoch** system for summarization and memory.

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| **World Hallucination** | Authoritative state injection in every LLM turn. |
| **Logic Drift** | Strict deterministic results from tools; GM cannot overwrite SE state. |
| **Context Exhaustion** | Hierarchical world model; only immediate proximity is loaded. |
| **User Friction** | Serial interaction with Plain Text Triggers (voice-friendly). |

## Migration Paths
- **v1 (MVP)**: Single-player, CLI, local state.
- **v2**: Multi-player party support, WebSocket sync.
- **v3**: Web UI (Retro-terminal aesthetic).
