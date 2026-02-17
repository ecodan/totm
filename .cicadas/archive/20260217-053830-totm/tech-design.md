# Tech Design: TOTM (Theater of the Mind)

## Summary
TOTM uses a **Graph-Powered State Engine**. The world is represented as a directed graph of **Locations** connected by **Edges (Journeys)**. Characters belong to specific classes with unique attribute balances. The AI Game Master uses these models as a "Source of Truth" to narrate outcomes and world persistence.

## Data Models

### 1. Characters Classes & Stats
Four base classes derived from classic fantasy tropes:
- **Warrior**: High Brawn/HP, Low Brains.
- **Mage**: High Brains, Low Brawn/HP.
- **Cleric**: High Faith, Medium HP.
- **Thief**: High Speed, Low Brawn.

| Attribute | Description |
|-----------|-------------|
| `brawn`   | Strength and physical endurance. |
| `brains`  | Intelligence and magical aptitude. |
| `faith`   | Spiritual connection and healing. |
| `speed`   | Agility and dexterity. |
| `hp`      | Hit Points (Life). |
| `xp`      | Experience Points (Progression). |

### 2. World Model (Graph Hierarchy)
The world consists of **Regions**, each acting as a namespace for a **Graph**.

#### Node: Location
```json
{
  "id": "loc_well_bottom",
  "name": "The Bottom of the Well",
  "description": "Damp, mossy stone walls rise around you.",
  "npcs": [
    {"id": "goblin_01", "name": "Cowering Goblin", "stats": {"hp": 5}}
  ],
  "inventory": ["rusted_chest"],
  "gm_guide": "The chest contains the forest map. The goblin knows about the secret switch."
}
```

#### Edge: Journey
```json
{
  "from": "loc_well_top",
  "to": "loc_well_bottom",
  "direction": "down",
  "duration": "1 minute",
  "difficulty": 3,
  "risks": ["Slippery stones", "Darkness"],
  "description": "A precarious climb down the rusted ladder."
}
```

## Arbiter Tools (Updated)

| Tool | Action | Description |
|------|--------|-------------|
| `get_location()` | Query SE | Returns current Location data (Description, NPCs, **GM Guide**). |
| `get_exits()` | Query SE | Returns all Edges (Journeys) connected to the current location (Direction, Risk labels). |
| `traverse(edge_id)` | Modify SE | **Deterministic Adjudication**: Executes stat-based checks. Returns a `Result Object` (Success, Damage/Costs) for GM narration. |
| `interact(npc_id, action)` | Modify/Query | Handles combat or dialogue; returns state-authoritative results. |
| `update_character(stats)` | Modify SE | Critical for the **Preparation Phase**; commits character class and initial stats. |

## Implementation Patterns

### 1. Lazy-Loaded Context Scaffolding
To prevent world-drift and hallucinations, the GM's prompt is dynamically rebuilt every turn:
- **Current Node**: The exact description and properties of the current `Location`.
- **Known Edges**: Only the `to` labels, directions, and risk summaries of immediate neighbor nodes.
- **Rule Constraints**: Minimum stat thresholds required for standard actions (Mechanic Floors).

### 2. Result-Driven Narration
The GM does not determine if a character succeeds at a physical task (e.g., climbing). Instead:
1. Player states intent.
2. GM calls `traverse(edge_id)`.
3. SE calculates success based on `Character.stats` vs `Edge.difficulty`.
4. SE returns: `{"status": "partial_success", "damage": 2, "effect": "lost_item"}`.
5. GM narrates the flavored outcome based on these specific data points.

## Security & Performance
- **Validation**: SE validates all moves against the graph topology.
- **Lazy Loading**: Only the current node and immediate transitions are kept in the LLM's active world-state window.
- **Deterministic Sync**: The "Theater" (Narrative) must always lag slightly behind the "Solid Ground" (State), waiting for tool output before describing changes.
