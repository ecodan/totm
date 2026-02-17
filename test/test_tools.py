"""Tests for Arbiter Tools — unit tests with mock StateEngine."""

import pytest
from unittest.mock import patch

from totm.engine.models import Character, CharacterClass, Location, Journey, NPC
from totm.engine.graph import WorldGraph
from totm.engine.store import StateEngine
from totm.tools.api import ArbiterTools


@pytest.fixture
def tools() -> ArbiterTools:
    """Build tools backed by a minimal engine with the well scenario."""
    g = WorldGraph(region="Test")
    g.add_location(Location(
        id="top", name="Well Top",
        description="A crumbling well.",
        npcs=[NPC(id="goblin", name="Goblin", hp=5, hostile=True, description="Small and green.")],
        inventory=["rope"],
        gm_guide="The rope is frayed.",
    ))
    g.add_location(Location(id="bottom", name="Well Bottom", description="Damp and dark."))
    g.add_journey(Journey(
        id="j_down", from_id="top", to_id="bottom",
        direction="down", duration="1 min",
        difficulty=3, risks=["Slippery stones"],
        description="Climb down the ladder.",
    ))
    e = StateEngine(g)
    e.set_character(Character.create("Hero", CharacterClass.WARRIOR))
    e.set_location("top")
    return ArbiterTools(e)


class TestGetLocation:
    def test_returns_location_data(self, tools: ArbiterTools):
        result = tools.get_location()
        assert result["id"] == "top"
        assert result["name"] == "Well Top"
        assert result["gm_guide"] == "The rope is frayed."
        assert len(result["npcs"]) == 1
        assert result["npcs"][0]["name"] == "Goblin"
        assert result["inventory"] == ["rope"]

    def test_no_location_returns_error(self):
        g = WorldGraph(region="T")
        e = StateEngine(g)
        t = ArbiterTools(e)
        result = t.get_location()
        assert result["error"] is True
        assert "No current location" in result["message"]


class TestGetExits:
    def test_returns_exits(self, tools: ArbiterTools):
        result = tools.get_exits()
        assert result["location_id"] == "top"
        assert len(result["exits"]) == 1
        ex = result["exits"][0]
        assert ex["journey_id"] == "j_down"
        assert ex["direction"] == "down"
        assert ex["destination_name"] == "Well Bottom"
        assert ex["difficulty"] == 3

    def test_no_location_returns_error(self):
        g = WorldGraph(region="T")
        e = StateEngine(g)
        t = ArbiterTools(e)
        result = t.get_exits()
        assert result["error"] is True


class TestTraverse:
    def test_success(self, tools: ArbiterTools):
        with patch("totm.engine.store.random.randint", return_value=8):
            result = tools.traverse("j_down")
        assert result["success"] is True
        assert result["new_location_name"] == "Well Bottom"
        assert result["character_hp"] == "12/12"

    def test_failure(self, tools: ArbiterTools):
        with patch("totm.engine.store.random.randint", return_value=1):
            result = tools.traverse("j_down")
        assert result["success"] is False
        assert result["damage"] == 2
        assert result["character_hp"] == "10/12"


class TestInteract:
    def test_talk(self, tools: ArbiterTools):
        result = tools.interact("goblin", "talk")
        assert result["success"] is True
        assert result["npc_name"] == "Goblin"
        assert "conversation" in result["message"]

    def test_attack(self, tools: ArbiterTools):
        with patch("totm.engine.store.random.randint", return_value=5):
            result = tools.interact("goblin", "attack")
        assert result["success"] is True
        assert result["damage_dealt"] == 5
        assert result["npc_defeated"] is True

    def test_missing_npc(self, tools: ArbiterTools):
        result = tools.interact("nobody", "talk")
        assert result["success"] is False


class TestUpdateCharacter:
    def test_create_character(self, tools: ArbiterTools):
        result = tools.update_character("Gandalf", "mage")
        assert result["name"] == "Gandalf"
        assert result["char_class"] == "mage"
        assert result["brains"] == 8
        assert result["hp"] == "6/6"

    def test_with_stat_overrides(self, tools: ArbiterTools):
        result = tools.update_character("Custom", "thief", brawn=10, speed=10)
        assert result["brawn"] == 10
        assert result["speed"] == 10

    def test_invalid_class(self, tools: ArbiterTools):
        result = tools.update_character("Bad", "wizard")
        assert result["error"] is True
        assert "Unknown class" in result["message"]


class TestGetCharacter:
    def test_returns_character(self, tools: ArbiterTools):
        result = tools.get_character()
        assert result["name"] == "Hero"
        assert result["char_class"] == "warrior"
        assert result["hp"] == "12/12"

    def test_no_character(self):
        g = WorldGraph(region="T")
        e = StateEngine(g)
        t = ArbiterTools(e)
        result = t.get_character()
        assert result["error"] is True


class TestIntegration:
    """End-to-end: create character, check location, traverse, interact."""

    def test_full_flow(self, tools: ArbiterTools):
        # Check location
        loc = tools.get_location()
        assert loc["name"] == "Well Top"

        # Check exits
        exits = tools.get_exits()
        assert len(exits["exits"]) == 1

        # Traverse down
        with patch("totm.engine.store.random.randint", return_value=8):
            result = tools.traverse("j_down")
        assert result["success"] is True

        # New location
        loc2 = tools.get_location()
        assert loc2["name"] == "Well Bottom"

        # No exits from bottom (no journeys defined from bottom)
        exits2 = tools.get_exits()
        assert len(exits2["exits"]) == 0
