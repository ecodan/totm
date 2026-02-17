"""Tests for engine data models: Character, NPC, Location, Journey."""

import json
import pytest

from totm.engine.models import Character, CharacterClass, NPC, Location, Journey


# -- Character -----------------------------------------------------------

class TestCharacter:
    def test_create_warrior(self):
        c = Character.create("Thorin", CharacterClass.WARRIOR)
        assert c.name == "Thorin"
        assert c.char_class == CharacterClass.WARRIOR
        assert c.brawn == 8
        assert c.hp == 12
        assert c.max_hp == 12
        assert c.xp == 0

    def test_create_mage(self):
        c = Character.create("Gandalf", CharacterClass.MAGE)
        assert c.brains == 8
        assert c.hp == 6

    def test_create_cleric(self):
        c = Character.create("Friar", CharacterClass.CLERIC)
        assert c.faith == 8
        assert c.hp == 8

    def test_create_thief(self):
        c = Character.create("Shadow", CharacterClass.THIEF)
        assert c.speed == 8
        assert c.hp == 7

    def test_json_round_trip(self):
        c = Character.create("Test", CharacterClass.WARRIOR)
        c.inventory = ["sword", "shield"]
        raw = c.to_json()
        c2 = Character.from_json(raw)
        assert c2.name == c.name
        assert c2.char_class == c.char_class
        assert c2.brawn == c.brawn
        assert c2.inventory == ["sword", "shield"]

    def test_is_alive(self):
        c = Character.create("Test", CharacterClass.WARRIOR)
        assert c.is_alive
        c.hp = 0
        assert not c.is_alive

    def test_primary_stat(self):
        c = Character.create("Test", CharacterClass.WARRIOR)
        name, val = c.primary_stat()
        assert name == "brawn"
        assert val == 8


# -- NPC ----------------------------------------------------------------

class TestNPC:
    def test_round_trip(self):
        npc = NPC(id="g1", name="Goblin", hp=5, hostile=True, description="Nasty")
        d = npc.to_dict()
        npc2 = NPC.from_dict(d)
        assert npc2.id == "g1"
        assert npc2.hostile is True


# -- Location ------------------------------------------------------------

class TestLocation:
    def test_round_trip(self):
        npc = NPC(id="n1", name="Guard", hp=10)
        loc = Location(
            id="loc_1", name="Castle Gate", description="A big gate.",
            npcs=[npc], inventory=["key"], gm_guide="Secret passage behind."
        )
        d = loc.to_dict()
        loc2 = Location.from_dict(d)
        assert loc2.id == "loc_1"
        assert len(loc2.npcs) == 1
        assert loc2.npcs[0].name == "Guard"
        assert loc2.inventory == ["key"]


# -- Journey ------------------------------------------------------------

class TestJourney:
    def test_round_trip(self):
        j = Journey(
            id="j1", from_id="a", to_id="b",
            direction="north", duration="5m",
            difficulty=3, risks=["Darkness"],
            description="A dark path."
        )
        d = j.to_dict()
        j2 = Journey.from_dict(d)
        assert j2.id == "j1"
        assert j2.difficulty == 3
        assert j2.risks == ["Darkness"]
