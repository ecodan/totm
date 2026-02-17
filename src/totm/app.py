"""TOTM Application Entry Point."""

import sys
from pathlib import Path

# Add src to path if running directly
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from totm.engine.store import StateEngine
from totm.engine.graph import WorldGraph
from totm.tools.api import ArbiterTools
from totm.ui.console import Console


from totm.agent.client import GMAgent

def main() -> None:
    # Bootstrap
    # Start with an empty engine; New Game / Load Game will populate it.
    world = WorldGraph(region="Empty") 
    engine = StateEngine(world)
    tools = ArbiterTools(engine)
    
    # Initialize Agent (if configured in agents.json/env)
    # We default to "gm_agent"
    try:
        agent = GMAgent(tools, agent_name="gm_agent")
    except Exception as e:
        print(f"Warning: Could not initialize AI Agent: {e}")
        agent = None
    
    # Launch UI
    console = Console(engine, tools, agent)
    console.run()


if __name__ == "__main__":
    main()
