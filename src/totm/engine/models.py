"""Core data models for TOTM: Characters, Locations, Journeys, NPCs."""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Character
# ---------------------------------------------------------------------------

class CharacterClass(Enum):
    """The four playable archetypes."""

    WARRIOR = "warrior"
    MAGE = "mage"
    CLERIC = "cleric"
    THIEF = "thief"


# Default stat blocks per class — (brawn, brains, faith, speed, hp)
_CLASS_DEFAULTS: dict[CharacterClass, dict[str, int]] = {
    CharacterClass.WARRIOR: {"brawn": 8, "brains": 3, "faith": 2, "speed": 4, "hp": 12},
    CharacterClass.MAGE:    {"brawn": 2, "brains": 8, "faith": 3, "speed": 4, "hp": 6},
    CharacterClass.CLERIC:  {"brawn": 4, "brains": 4, "faith": 8, "speed": 3, "hp": 8},
    CharacterClass.THIEF:   {"brawn": 3, "brains": 5, "faith": 2, "speed": 8, "hp": 7},
}


@dataclass
class Character:
    """A player character with class-based stats."""

    name: str
    char_class: CharacterClass
    brawn: int = 0
    brains: int = 0
    faith: int = 0
    speed: int = 0
    hp: int = 0
    max_hp: int = 0
    xp: int = 0
    inventory: list[str] = field(default_factory=list)

    # -- Factories -------------------------------------------------------

    @classmethod
    def create(cls, name: str, char_class: CharacterClass) -> Character:
        """Create a new character with default stats for *char_class*."""
        defaults = _CLASS_DEFAULTS[char_class]
        return cls(
            name=name,
            char_class=char_class,
            brawn=defaults["brawn"],
            brains=defaults["brains"],
            faith=defaults["faith"],
            speed=defaults["speed"],
            hp=defaults["hp"],
            max_hp=defaults["hp"],
            xp=0,
        )

    # -- Serialization ---------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["char_class"] = self.char_class.value
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Character:
        data = dict(data)  # shallow copy
        data["char_class"] = CharacterClass(data["char_class"])
        return cls(**data)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_json(cls, raw: str) -> Character:
        return cls.from_dict(json.loads(raw))

    # -- Queries ---------------------------------------------------------

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def primary_stat(self) -> tuple[str, int]:
        """Return the name and value of the character's highest stat."""
        stats = {"brawn": self.brawn, "brains": self.brains,
                 "faith": self.faith, "speed": self.speed}
        name = max(stats, key=stats.get)  # type: ignore[arg-type]
        return name, stats[name]


# ---------------------------------------------------------------------------
# NPC
# ---------------------------------------------------------------------------

@dataclass
class NPC:
    """A non-player character inhabiting a Location."""

    id: str
    name: str
    hp: int = 10
    hostile: bool = False
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> NPC:
        return cls(**data)


# ---------------------------------------------------------------------------
# Location (Graph Node)
# ---------------------------------------------------------------------------

@dataclass
class Location:
    """A node in the world graph."""

    id: str
    name: str
    description: str = ""
    npcs: list[NPC] = field(default_factory=list)
    inventory: list[str] = field(default_factory=list)
    gm_guide: str = ""

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["npcs"] = [npc.to_dict() for npc in self.npcs]
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Location:
        data = dict(data)
        data["npcs"] = [NPC.from_dict(n) for n in data.get("npcs", [])]
        return cls(**data)


# ---------------------------------------------------------------------------
# Journey (Graph Edge)
# ---------------------------------------------------------------------------

@dataclass
class Journey:
    """A directed edge between two Locations."""

    id: str
    from_id: str
    to_id: str
    direction: str = ""
    duration: str = ""
    difficulty: int = 1
    risks: list[str] = field(default_factory=list)
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Journey:
        return cls(**data)
