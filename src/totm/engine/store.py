"""StateEngine — the authoritative 'Solid Ground' for TOTM.

Manages the active character, current location, world graph, and provides
deterministic adjudication for traversal and NPC interaction.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

from totm.engine.models import Character, Location, Journey, NPC
from totm.engine.graph import WorldGraph


# ---------------------------------------------------------------------------
# Result objects — returned by adjudication methods
# ---------------------------------------------------------------------------

@dataclass
class TraverseResult:
    """Outcome of attempting to traverse a Journey edge."""

    success: bool
    journey_id: str
    from_id: str
    to_id: str
    stat_used: str = ""
    stat_value: int = 0
    difficulty: int = 0
    roll: int = 0
    damage: int = 0
    message: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class InteractResult:
    """Outcome of an NPC interaction."""

    success: bool
    npc_id: str
    action: str
    stat_used: str = ""
    stat_value: int = 0
    damage_dealt: int = 0
    damage_taken: int = 0
    npc_defeated: bool = False
    message: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# StateEngine
# ---------------------------------------------------------------------------

class StateEngine:
    """Authoritative game state manager.

    The StateEngine owns:
    * The :class:`WorldGraph` (read from disk or built in-memory).
    * The active :class:`Character`.
    * The current location pointer.

    All mutations go through this class — the GM Agent must never modify
    state directly.
    """

    def __init__(self, world: WorldGraph) -> None:
        self.world = world
        self._character: Character | None = None
        self._current_location_id: str | None = None

    # -- Character -------------------------------------------------------

    @property
    def character(self) -> Character | None:
        return self._character

    def set_character(self, character: Character) -> None:
        self._character = character

    # -- Location --------------------------------------------------------

    @property
    def current_location_id(self) -> str | None:
        return self._current_location_id

    @property
    def current_location(self) -> Location | None:
        if self._current_location_id is None:
            return None
        return self.world.get_location(self._current_location_id)

    def set_location(self, location_id: str) -> None:
        if self.world.get_location(location_id) is None:
            raise ValueError(f"Location '{location_id}' not in world graph")
        self._current_location_id = location_id

    # -- Adjudication: Traverse ------------------------------------------

    def traverse(self, journey_id: str) -> TraverseResult:
        """Attempt to traverse a Journey. Deterministic stat check.

        Mechanic: ``roll = random.randint(1, stat_value)``
        Success if ``roll >= difficulty``.
        On failure, character takes ``difficulty - roll`` damage.
        """
        journey = self.world.get_journey(journey_id)
        if journey is None:
            return TraverseResult(
                success=False,
                journey_id=journey_id,
                from_id="",
                to_id="",
                message=f"Journey '{journey_id}' does not exist.",
            )

        if self._character is None:
            return TraverseResult(
                success=False,
                journey_id=journey_id,
                from_id=journey.from_id,
                to_id=journey.to_id,
                message="No active character.",
            )

        if self._current_location_id != journey.from_id:
            return TraverseResult(
                success=False,
                journey_id=journey_id,
                from_id=journey.from_id,
                to_id=journey.to_id,
                message="Character is not at the journey's origin.",
            )

        # Pick the most relevant stat for the journey's risks
        stat_name, stat_value = self._pick_stat_for_risks(journey.risks)
        roll = random.randint(1, max(stat_value, 1))

        if roll >= journey.difficulty:
            # Success — move character
            self._current_location_id = journey.to_id
            return TraverseResult(
                success=True,
                journey_id=journey_id,
                from_id=journey.from_id,
                to_id=journey.to_id,
                stat_used=stat_name,
                stat_value=stat_value,
                difficulty=journey.difficulty,
                roll=roll,
                message=f"Traversed successfully to '{journey.to_id}'.",
            )
        else:
            # Failure — take damage, stay put
            damage = journey.difficulty - roll
            self._character.hp = max(0, self._character.hp - damage)
            return TraverseResult(
                success=False,
                journey_id=journey_id,
                from_id=journey.from_id,
                to_id=journey.to_id,
                stat_used=stat_name,
                stat_value=stat_value,
                difficulty=journey.difficulty,
                roll=roll,
                damage=damage,
                message=f"Failed! Took {damage} damage. HP: {self._character.hp}/{self._character.max_hp}.",
            )

    # -- Adjudication: Interact ------------------------------------------

    def interact(self, npc_id: str, action: str) -> InteractResult:
        """Interact with an NPC at the current location.

        Supported actions: ``attack``, ``talk``.
        """
        loc = self.current_location
        if loc is None:
            return InteractResult(
                success=False, npc_id=npc_id, action=action,
                message="No current location.",
            )

        npc = next((n for n in loc.npcs if n.id == npc_id), None)
        if npc is None:
            return InteractResult(
                success=False, npc_id=npc_id, action=action,
                message=f"NPC '{npc_id}' not found at current location.",
            )

        if self._character is None:
            return InteractResult(
                success=False, npc_id=npc_id, action=action,
                message="No active character.",
            )

        if action == "attack":
            return self._attack(npc)
        elif action == "talk":
            return InteractResult(
                success=True, npc_id=npc_id, action=action,
                message=f"You engage {npc.name} in conversation.",
            )
        else:
            return InteractResult(
                success=False, npc_id=npc_id, action=action,
                message=f"Unknown action: '{action}'.",
            )

    def _attack(self, npc: NPC) -> InteractResult:
        """Simple attack: character brawn vs NPC hp."""
        assert self._character is not None
        attack_roll = random.randint(1, max(self._character.brawn, 1))
        damage_dealt = attack_roll
        npc.hp = max(0, npc.hp - damage_dealt)

        damage_taken = 0
        if npc.hostile and npc.hp > 0:
            damage_taken = random.randint(1, 3)
            self._character.hp = max(0, self._character.hp - damage_taken)

        return InteractResult(
            success=True,
            npc_id=npc.id,
            action="attack",
            stat_used="brawn",
            stat_value=self._character.brawn,
            damage_dealt=damage_dealt,
            damage_taken=damage_taken,
            npc_defeated=npc.hp <= 0,
            message=(
                f"Dealt {damage_dealt} damage to {npc.name} "
                f"(HP: {npc.hp}). "
                + (f"Took {damage_taken} damage in return. " if damage_taken else "")
                + ("NPC defeated!" if npc.hp <= 0 else "")
            ),
        )

    # -- Internal helpers ------------------------------------------------

    _RISK_STAT_MAP: dict[str, str] = {
        "slippery": "speed",
        "darkness": "brains",
        "climb": "brawn",
        "steep": "brawn",
        "trap": "speed",
        "magic": "brains",
        "curse": "faith",
        "undead": "faith",
    }

    def _pick_stat_for_risks(self, risks: list[str]) -> tuple[str, int]:
        """Heuristic: map risk keywords to the best stat to check."""
        assert self._character is not None
        stats = {
            "brawn": self._character.brawn,
            "brains": self._character.brains,
            "faith": self._character.faith,
            "speed": self._character.speed,
        }
        for risk in risks:
            for keyword, stat_name in self._RISK_STAT_MAP.items():
                if keyword in risk.lower():
                    return stat_name, stats[stat_name]
        # Default: use the character's primary stat
        return self._character.primary_stat()

    # -- Persistence -----------------------------------------------------

    def save(self, path: Path) -> None:
        """Save the full game state (world + character + location) to JSON."""
        state: dict[str, Any] = {
            "world": self.world.to_dict(),
            "character": self._character.to_dict() if self._character else None,
            "current_location_id": self._current_location_id,
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(state, indent=2))

    @classmethod
    def load(cls, path: Path) -> StateEngine:
        """Load a saved game state from JSON."""
        data = json.loads(path.read_text())
        world = WorldGraph.from_dict(data["world"])
        engine = cls(world)
        if data.get("character"):
            engine.set_character(Character.from_dict(data["character"]))
        if data.get("current_location_id"):
            engine.set_location(data["current_location_id"])
        return engine
