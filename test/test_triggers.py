"""Tests for plain text trigger parsing."""

from totm.ui.triggers import TriggerParser


class TestTriggerParser:
    def test_stats(self):
        p = TriggerParser()
        assert p.parse("check stats").tool == "get_character"
        assert p.parse("stats").tool == "get_character"
        assert p.parse("how am i doing?").tool == "get_character"
        assert p.parse("/hp").tool == "get_character"

    def test_inventory(self):
        p = TriggerParser()
        assert p.parse("check inventory").tool == "get_character"
        assert p.parse("open bag").tool == "get_character"
        assert p.parse("my items").tool == "get_character"
        assert p.parse("/inv").tool == "get_character"

    def test_location(self):
        p = TriggerParser()
        assert p.parse("look").tool == "get_location"
        assert p.parse("look around").tool == "get_location"
        assert p.parse("where am i").tool == "get_location"
        assert p.parse("/map").tool == "get_location"

    def test_exits(self):
        p = TriggerParser()
        assert p.parse("exits").tool == "get_exits"
        assert p.parse("directions").tool == "get_exits"
    
    def test_narrative_input(self):
        p = TriggerParser()
        assert p.parse("I climb down the well") is None
        assert p.parse("attack the goblin") is None
        assert p.parse("say hello") is None
