"""Tests for WorldGraph — location/journey management and queries."""

import json
import pytest
from pathlib import Path

from totm.engine.models import Location, Journey, NPC
from totm.engine.graph import WorldGraph


@pytest.fixture
def sample_graph() -> WorldGraph:
    g = WorldGraph(region="Test Region")
    g.add_location(Location(id="a", name="Place A"))
    g.add_location(Location(id="b", name="Place B"))
    g.add_location(Location(id="c", name="Place C"))
    g.add_journey(Journey(id="j_ab", from_id="a", to_id="b", difficulty=2))
    g.add_journey(Journey(id="j_ac", from_id="a", to_id="c", difficulty=4))
    g.add_journey(Journey(id="j_ba", from_id="b", to_id="a", difficulty=1))
    return g


class TestWorldGraph:
    def test_add_get_location(self, sample_graph: WorldGraph):
        loc = sample_graph.get_location("a")
        assert loc is not None
        assert loc.name == "Place A"

    def test_get_missing_location(self, sample_graph: WorldGraph):
        assert sample_graph.get_location("zzz") is None

    def test_all_locations(self, sample_graph: WorldGraph):
        assert len(sample_graph.all_locations()) == 3

    def test_add_journey_bad_origin(self):
        g = WorldGraph(region="R")
        g.add_location(Location(id="a", name="A"))
        with pytest.raises(ValueError, match="Origin"):
            g.add_journey(Journey(id="j", from_id="x", to_id="a"))

    def test_add_journey_bad_dest(self):
        g = WorldGraph(region="R")
        g.add_location(Location(id="a", name="A"))
        with pytest.raises(ValueError, match="Destination"):
            g.add_journey(Journey(id="j", from_id="a", to_id="x"))

    def test_exits(self, sample_graph: WorldGraph):
        exits = sample_graph.exits("a")
        assert len(exits) == 2
        ids = {e.id for e in exits}
        assert ids == {"j_ab", "j_ac"}

    def test_exits_empty(self, sample_graph: WorldGraph):
        assert sample_graph.exits("c") == []

    def test_neighbors(self, sample_graph: WorldGraph):
        nbrs = sample_graph.neighbors("a")
        assert len(nbrs) == 2
        names = {n.name for n in nbrs}
        assert names == {"Place B", "Place C"}

    def test_json_round_trip(self, sample_graph: WorldGraph):
        d = sample_graph.to_dict()
        g2 = WorldGraph.from_dict(d)
        assert g2.region == "Test Region"
        assert len(g2.all_locations()) == 3
        assert len(g2.exits("a")) == 2

    def test_save_load(self, sample_graph: WorldGraph, tmp_path: Path):
        path = tmp_path / "world.json"
        sample_graph.save(path)
        g2 = WorldGraph.load(path)
        assert g2.region == "Test Region"
        assert len(g2.all_locations()) == 3


class TestWellWorld:
    """Smoke test: load the bundled well.json prototype."""

    def test_load_well(self):
        well_path = Path(__file__).resolve().parent.parent / "src" / "totm" / "engine" / "worlds" / "well.json"
        g = WorldGraph.load(well_path)
        assert g.region == "Dark Forest"
        assert g.get_location("loc_well_top") is not None
        assert g.get_location("loc_well_bottom") is not None
        exits = g.exits("loc_well_bottom")
        assert len(exits) == 2  # up to top and east to tunnel
