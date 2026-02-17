"""Tests for StateEngine — adjudication, persistence, and state management."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch

from totm.engine.models import Character, CharacterClass, Location, Journey, NPC
from totm.engine.graph import WorldGraph
from totm.engine.store import StateEngine


@pytest.fixture
def engine() -> StateEngine:
    """Build a minimal engine with the well scenario."""
    g = WorldGraph(region="Test")
    g.add_location(Location(
        id="top", name="Top",
        npcs=[NPC(id="goblin", name="Goblin", hp=5, hostile=True)],
    ))
    g.add_location(Location(id="bottom", name="Bottom"))
    g.add_journey(Journey(
        id="j_down", from_id="top", to_id="bottom",
        difficulty=3, risks=["Slippery stones"],
    ))
    g.add_journey(Journey(
        id="j_up", from_id="bottom", to_id="top",
        difficulty=5, risks=["Climb"],
    ))
    e = StateEngine(g)
    e.set_character(Character.create("Hero", CharacterClass.WARRIOR))
    e.set_location("top")
    return e


class TestStateEngineLocation:
    def test_set_location(self, engine: StateEngine):
        assert engine.current_location_id == "top"
        assert engine.current_location is not None
        assert engine.current_location.name == "Top"

    def test_set_invalid_location(self, engine: StateEngine):
        with pytest.raises(ValueError):
            engine.set_location("nonexistent")


class TestTraverse:
    def test_traverse_success(self, engine: StateEngine):
        # Force a high roll to guarantee success
        with patch("totm.engine.store.random.randint", return_value=8):
            result = engine.traverse("j_down")
        assert result.success is True
        assert engine.current_location_id == "bottom"

    def test_traverse_failure(self, engine: StateEngine):
        # Force a low roll to guarantee failure
        with patch("totm.engine.store.random.randint", return_value=1):
            result = engine.traverse("j_down")
        assert result.success is False
        assert engine.current_location_id == "top"  # stayed put
        assert result.damage == 2  # difficulty(3) - roll(1) = 2

    def test_traverse_nonexistent_journey(self, engine: StateEngine):
        result = engine.traverse("fake")
        assert result.success is False
        assert "does not exist" in result.message

    def test_traverse_wrong_location(self, engine: StateEngine):
        # Character is at "top", try a journey that starts at "bottom"
        result = engine.traverse("j_up")
        assert result.success is False
        assert "not at" in result.message

    def test_traverse_no_character(self):
        g = WorldGraph(region="T")
        g.add_location(Location(id="a", name="A"))
        g.add_location(Location(id="b", name="B"))
        g.add_journey(Journey(id="j", from_id="a", to_id="b", difficulty=1))
        e = StateEngine(g)
        e._current_location_id = "a"
        result = e.traverse("j")
        assert result.success is False
        assert "No active character" in result.message


class TestInteract:
    def test_talk(self, engine: StateEngine):
        result = engine.interact("goblin", "talk")
        assert result.success is True
        assert "conversation" in result.message

    def test_attack(self, engine: StateEngine):
        with patch("totm.engine.store.random.randint", return_value=3):
            result = engine.interact("goblin", "attack")
        assert result.success is True
        assert result.damage_dealt == 3

    def test_attack_defeat(self, engine: StateEngine):
        with patch("totm.engine.store.random.randint", return_value=5):
            result = engine.interact("goblin", "attack")
        assert result.npc_defeated is True

    def test_interact_missing_npc(self, engine: StateEngine):
        result = engine.interact("nobody", "talk")
        assert result.success is False
        assert "not found" in result.message

    def test_interact_unknown_action(self, engine: StateEngine):
        result = engine.interact("goblin", "dance")
        assert result.success is False
        assert "Unknown action" in result.message


class TestPersistence:
    def test_save_load_round_trip(self, engine: StateEngine, tmp_path: Path):
        path = tmp_path / "save.json"
        engine.save(path)
        e2 = StateEngine.load(path)
        assert e2.current_location_id == "top"
        assert e2.character is not None
        assert e2.character.name == "Hero"
        assert e2.world.region == "Test"
        assert len(e2.world.all_locations()) == 2

    def test_save_no_character(self, tmp_path: Path):
        g = WorldGraph(region="Empty")
        g.add_location(Location(id="x", name="X"))
        e = StateEngine(g)
        path = tmp_path / "save.json"
        e.save(path)
        e2 = StateEngine.load(path)
        assert e2.character is None
        assert e2.current_location_id is None
