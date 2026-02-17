"""TOTM Application Entry Point."""

import sys
from pathlib import Path

# Add src to path if running directly
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from totm.engine.store import StateEngine
from totm.engine.graph import WorldGraph
from totm.tools.api import ArbiterTools
from totm.ui.console import Console


def main() -> None:
    # Bootstrap
    # Start with an empty engine; New Game / Load Game will populate it.
    world = WorldGraph(region="Empty") 
    engine = StateEngine(world)
    tools = ArbiterTools(engine)
    
    # Launch UI
    console = Console(engine, tools)
    console.run()


if __name__ == "__main__":
    main()
