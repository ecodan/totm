"""WorldGraph — a region-scoped directed graph of Locations and Journeys."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from totm.engine.models import Location, Journey


@dataclass
class WorldGraph:
    """Directed graph representing a game world region.

    Nodes are :class:`Location` instances, edges are :class:`Journey` instances.
    The graph is region-scoped: each WorldGraph represents a single named
    region (e.g. "Dark Forest").
    """

    region: str
    _locations: dict[str, Location] = field(default_factory=dict)
    _journeys: dict[str, Journey] = field(default_factory=dict)
    # Adjacency: location_id -> list of journey_ids originating there
    _adj: dict[str, list[str]] = field(default_factory=dict)

    # -- Locations -------------------------------------------------------

    def add_location(self, location: Location) -> None:
        self._locations[location.id] = location
        self._adj.setdefault(location.id, [])

    def get_location(self, location_id: str) -> Location | None:
        return self._locations.get(location_id)

    def all_locations(self) -> list[Location]:
        return list(self._locations.values())

    # -- Journeys --------------------------------------------------------

    def add_journey(self, journey: Journey) -> None:
        if journey.from_id not in self._locations:
            raise ValueError(
                f"Origin location '{journey.from_id}' not in graph"
            )
        if journey.to_id not in self._locations:
            raise ValueError(
                f"Destination location '{journey.to_id}' not in graph"
            )
        self._journeys[journey.id] = journey
        self._adj[journey.from_id].append(journey.id)

    def get_journey(self, journey_id: str) -> Journey | None:
        return self._journeys.get(journey_id)

    def exits(self, location_id: str) -> list[Journey]:
        """Return all outgoing Journeys from *location_id*."""
        journey_ids = self._adj.get(location_id, [])
        return [self._journeys[jid] for jid in journey_ids if jid in self._journeys]

    def neighbors(self, location_id: str) -> list[Location]:
        """Return the destination Locations reachable from *location_id*."""
        return [
            self._locations[j.to_id]
            for j in self.exits(location_id)
            if j.to_id in self._locations
        ]

    # -- Serialization ---------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "region": self.region,
            "locations": [loc.to_dict() for loc in self._locations.values()],
            "journeys": [j.to_dict() for j in self._journeys.values()],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorldGraph:
        graph = cls(region=data["region"])
        for loc_data in data.get("locations", []):
            graph.add_location(Location.from_dict(loc_data))
        for j_data in data.get("journeys", []):
            graph.add_journey(Journey.from_dict(j_data))
        return graph

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2))

    @classmethod
    def load(cls, path: Path) -> WorldGraph:
        return cls.from_dict(json.loads(path.read_text()))
