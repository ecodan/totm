"""Arbiter Tools API — the bridge between the GM Agent and the StateEngine.

The GM calls these methods; they delegate to the StateEngine and return
structured result objects suitable for LLM consumption.
"""

from __future__ import annotations

from totm.engine.models import Character, CharacterClass
from totm.engine.store import StateEngine
from totm.tools.schema import (
    LocationInfo,
    ExitInfo,
    ExitsResult,
    TraverseToolResult,
    InteractToolResult,
    CharacterInfo,
    ToolError,
)

from typing import Any


class ArbiterTools:
    """Stateless façade that wraps a :class:`StateEngine` with GM-friendly tools.

    Every public method returns a dict (via ``.to_dict()``) so the GM can
    consume the result directly as structured data.
    """

    def __init__(self, engine: StateEngine) -> None:
        self._engine = engine

    # -- get_location ----------------------------------------------------

    def get_location(self) -> dict[str, Any]:
        """Return details of the current location, including GM guide."""
        loc = self._engine.current_location
        if loc is None:
            return ToolError(tool="get_location", message="No current location set.").to_dict()

        return LocationInfo(
            id=loc.id,
            name=loc.name,
            description=loc.description,
            npcs=[{"id": n.id, "name": n.name, "hp": n.hp,
                   "hostile": n.hostile, "description": n.description}
                  for n in loc.npcs],
            inventory=loc.inventory,
            gm_guide=loc.gm_guide,
        ).to_dict()

    # -- get_exits -------------------------------------------------------

    def get_exits(self) -> dict[str, Any]:
        """Return all exits (journeys) from the current location."""
        loc = self._engine.current_location
        if loc is None:
            return ToolError(tool="get_exits", message="No current location set.").to_dict()

        journeys = self._engine.world.exits(loc.id)
        exit_infos = []
        for j in journeys:
            dest = self._engine.world.get_location(j.to_id)
            exit_infos.append(ExitInfo(
                journey_id=j.id,
                direction=j.direction,
                destination_name=dest.name if dest else j.to_id,
                difficulty=j.difficulty,
                risks=j.risks,
                description=j.description,
            ))

        return ExitsResult(
            location_id=loc.id,
            location_name=loc.name,
            exits=exit_infos,
        ).to_dict()

    # -- traverse --------------------------------------------------------

    def traverse(self, journey_id: str) -> dict[str, Any]:
        """Attempt to traverse a journey. Returns deterministic outcome."""
        result = self._engine.traverse(journey_id)

        new_loc = self._engine.current_location
        char = self._engine.character

        return TraverseToolResult(
            success=result.success,
            journey_id=result.journey_id,
            from_location=result.from_id,
            to_location=result.to_id,
            stat_used=result.stat_used,
            stat_value=result.stat_value,
            difficulty=result.difficulty,
            roll=result.roll,
            damage=result.damage,
            message=result.message,
            new_location_name=new_loc.name if new_loc else "",
            character_hp=f"{char.hp}/{char.max_hp}" if char else "",
        ).to_dict()

    # -- interact --------------------------------------------------------

    def interact(self, npc_id: str, action: str) -> dict[str, Any]:
        """Interact with an NPC (attack, talk). Returns outcome."""
        result = self._engine.interact(npc_id, action)

        # Get current NPC state for the response
        loc = self._engine.current_location
        npc = None
        if loc:
            npc = next((n for n in loc.npcs if n.id == npc_id), None)

        char = self._engine.character

        return InteractToolResult(
            success=result.success,
            npc_id=result.npc_id,
            npc_name=npc.name if npc else npc_id,
            action=result.action,
            stat_used=result.stat_used,
            damage_dealt=result.damage_dealt,
            damage_taken=result.damage_taken,
            npc_defeated=result.npc_defeated,
            npc_hp=npc.hp if npc else 0,
            character_hp=f"{char.hp}/{char.max_hp}" if char else "",
            message=result.message,
        ).to_dict()

    # -- update_character ------------------------------------------------

    def update_character(
        self,
        name: str,
        char_class: str,
        *,
        brawn: int | None = None,
        brains: int | None = None,
        faith: int | None = None,
        speed: int | None = None,
    ) -> dict[str, Any]:
        """Create or update the active character. Used during Preparation Phase.

        If custom stats are provided they override the class defaults.
        """
        try:
            cls = CharacterClass(char_class.lower())
        except ValueError:
            return ToolError(
                tool="update_character",
                message=f"Unknown class '{char_class}'. Valid: warrior, mage, cleric, thief.",
            ).to_dict()

        char = Character.create(name, cls)

        # Apply optional stat overrides
        if brawn is not None:
            char.brawn = brawn
        if brains is not None:
            char.brains = brains
        if faith is not None:
            char.faith = faith
        if speed is not None:
            char.speed = speed

        self._engine.set_character(char)

        return CharacterInfo(
            name=char.name,
            char_class=char.char_class.value,
            brawn=char.brawn,
            brains=char.brains,
            faith=char.faith,
            speed=char.speed,
            hp=f"{char.hp}/{char.max_hp}",
            xp=char.xp,
            inventory=char.inventory,
        ).to_dict()

    # -- get_character (bonus utility) -----------------------------------

    def get_character(self) -> dict[str, Any]:
        """Return the current character snapshot."""
        char = self._engine.character
        if char is None:
            return ToolError(tool="get_character", message="No active character.").to_dict()

        return CharacterInfo(
            name=char.name,
            char_class=char.char_class.value,
            brawn=char.brawn,
            brains=char.brains,
            faith=char.faith,
            speed=char.speed,
            hp=f"{char.hp}/{char.max_hp}",
            xp=char.xp,
            inventory=char.inventory,
        ).to_dict()
