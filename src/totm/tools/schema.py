"""Arbiter Tool result schemas — structured outputs for GM consumption.

Every tool returns a typed result dict that the GM can directly interpret
without needing to understand the engine internals.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any


@dataclass
class LocationInfo:
    """Result of get_location — what the GM 'sees' at the current node."""

    id: str
    name: str
    description: str
    npcs: list[dict[str, Any]]
    inventory: list[str]
    gm_guide: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ExitInfo:
    """A single outgoing journey from the current location."""

    journey_id: str
    direction: str
    destination_name: str
    difficulty: int
    risks: list[str]
    description: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ExitsResult:
    """Result of get_exits — all outgoing journeys from current location."""

    location_id: str
    location_name: str
    exits: list[ExitInfo]

    def to_dict(self) -> dict[str, Any]:
        return {
            "location_id": self.location_id,
            "location_name": self.location_name,
            "exits": [e.to_dict() for e in self.exits],
        }


@dataclass
class TraverseToolResult:
    """Result of traverse — wraps engine TraverseResult with GM-friendly fields."""

    success: bool
    journey_id: str
    from_location: str
    to_location: str
    stat_used: str
    stat_value: int
    difficulty: int
    roll: int
    damage: int
    message: str
    new_location_name: str = ""
    character_hp: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class InteractToolResult:
    """Result of interact — wraps engine InteractResult with GM-friendly fields."""

    success: bool
    npc_id: str
    npc_name: str
    action: str
    stat_used: str
    damage_dealt: int
    damage_taken: int
    npc_defeated: bool
    npc_hp: int
    character_hp: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CharacterInfo:
    """Result of update_character or get_character — full character snapshot."""

    name: str
    char_class: str
    brawn: int
    brains: int
    faith: int
    speed: int
    hp: str  # "current/max" format
    xp: int
    inventory: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ToolError:
    """Returned when a tool call fails."""

    error: bool = True
    tool: str = ""
    message: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
