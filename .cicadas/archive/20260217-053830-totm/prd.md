---
steps_completed: ['Problem Statement', 'Users', 'Scope', 'Functional Requirements', 'Success Criteria', 'Research Alignment']
next_section: 'UX Design'
---

# PRD: TOTM (Theater of the Mind)

## Problem Statement
Traditional digital RPGs are often constrained by pre-defined scripts and rigid mechanics. While LLMs offer the promise of dynamic, infinite narratives, current "AI RPGs" often lack world consistency, meaningful mechanical depth, or a shared "theatrical" interface that keeps players and AI agents synchronized on the state of the world.

TOTM aims to provide this "Theater of the Mind" — a platform for role-playing games where a specialized GM AI agent (powered by skills, tools, and rulebook RAG) collaborates with players in a structured, consistent, and immersive narrative environment.

## Users
1. **The Lead Player (User)**: The primary human participant who interacts with the GM to drive the story forward.
2. **AI Game Master (GM)**: A single agent responsible for narration, rule enforcement, and world management, using hierarchical state (Regions/Sub-regions) to maintain context.
3. **Multi-player Party (v2)**: Support for multiple humans/agents playing together with a single GM.
4. **Passive Observers (Optional)**: Future users who might watch or review game logs/histories.

## Success Criteria
- **State Consistency**: The GM agent can accurately recall and manipulate NPC stats, player state, and regional inventories without "hallucinating" changes.
- **Hierarchical World Management**: The system successfully handles movement and interaction across Regions and Sub-regions.
- **Interpretative Depth**: The GM can apply rules from a provided rulebook (via RAG or tools) to resolve player actions fairly.
- **Campaign Memory**: A structured log of "epochs" (sessions/regions) allows the GM to maintain long-term consistency through summaries and detail-retrieval.
- **Theatrical Synchronicity**: All participants (including future multi-player party members) have a shared "view" of the current game state and narrative history.

## Scope

### In Scope
- **Graph-Based World Engine**: A system representing the world as a hierarchy of Regions, each containing a directed graph of Locations linked by Edges.
- **State Management Engine**: A deterministic system for tracking Character classes/stats, NPC/Monster state, and regional context.
- **GM Agent Integration**: A single-agent orchestrator with access to world state tools and skills.
- **Rulebook RAG**: A mechanism for the GM to query rulebooks and guidelines to inform storytelling and arbitration.
- **Epoch-based Summarization**: A specific mechanism to generate and store summaries (overviews) and detailed logs of game segments.
- **Multi-player Architecture**: Designing the state and communication layers to support multiple concurrent players in a future version.

### Out of Scope
- **Graphical Client**: No 2D/3D rendering; focus is on text and structured state representation.
- **Voice Integration**: Voice-to-text or text-to-speech features.

## Requirements

### Functional
1. **World Graph**: The system must support modeling the world as a graph where nodes are "Locations" and edges represent "Journeys" with properties (difficulty, risks, direction, duration).
2. **Character Classes**: Support for four distinct classes (Warrior, Mage, Cleric, Thief) with attributes (Brawn, Brains, Faith, Speed, HP, XP).
3. **Location Attributes**: Every location node must include a description, NPC/Monster list, inventory, and a **GM Guide** (narrative prompts/secrets).
4. **Tool-Driven Navigation**: The GM must use specific tools to "traverse" edges, triggering checks based on edge difficulty and risks.
5. **Rule Reference**: The GM must be able to retrieve relevant gameplay rules dynamically (via RAG) to resolve actions.
6. **Epoch Summarization**:
    - **Overview**: High-level summary of the epoch (e.g., "The party escaped the orc camp") for immediate GM context.
    - **Detail**: Granular log of specific events/decisions for deeper retrieval.
7. **Two-Phase Lifecycle**: The system must support a clear separation between the **Preparation Phase** (Character/World setup) and the **Gameplay Phase** (Active narrative interaction).
8. **Main Menu Structure**: A top-level menu must manage game lifecycle actions (New, Save, Load, Create Character, Play).
9. **Serial Interaction Mode**: The primary interface is a narrative stream where users can retrieve structured state via explicit commands (slash commands) or **natural language triggers** (voice-friendly).
10. **State-Narrative Injection**: The GM must proactively weave "Solid Ground" updates (e.g., current HP or inventory changes) into the prose to maintain immersion and situational awareness without manual querying.
11. **Session State Sync**: In a multi-player context, all active users must see updates to the shared "Theater" (game state) in real-time.
12. **Authoritative Context Injection**: Key world state, character stats, and session history (summaries) must be programmatically injected into the GM's context window on every turn to prevent world-drift and hallucinations.

### Non-Functional
- **Narrative Consistency**: The AI must maintain a coherent story thread across session transitions using the epoch system.
- **Extensibility**: The state schema should allow for adding new types of entities or regional properties (e.g., "Clocks" for escalating danger).
- **Low Latency**: GM responses (including RAG and state lookups) should feel conversational (sub-5s).

## Open Questions
- How frequently should an "Epoch" be summarized (time-based, event-based, or region-based)?
- What specific format should the "structured log" take to be most LLM-friendly (JSON vs. Narrative-heavy but structured Markdown)?
- How do we handle "concurrency" in a multi-player party? Is it turn-based or free-form?
- Which initial "rulebook" or setting should be used for the prototype RAG?
