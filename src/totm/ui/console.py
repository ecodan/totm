"""The TOTM Console — primary user interface.

Manages the Main Menu and the primary Game Loop (Preparation & Gameplay).
"""

import sys
import shutil
from typing import Callable, NoReturn, Optional

from totm.engine.store import StateEngine
from totm.engine.models import Character, CharacterClass
from totm.tools.api import ArbiterTools
from totm.ui.formatting import (
    print_header, print_divider, print_gm, print_system,
    print_error, print_success, thinking_indicator, 
    CYAN, GREEN, YELLOW, RESET, BOLD, DIM
)
from totm.ui.triggers import TriggerParser, Intent


from totm.agent.client import GMAgent

class Console:
    """The terminal interface controller."""

    def __init__(self, engine: StateEngine, tools: ArbiterTools, agent: Optional[GMAgent] = None) -> None:
        self.engine = engine
        self.tools = tools
        self.agent = agent
        self.parser = TriggerParser()
        self._running = True

    def run(self) -> None:
        """Start the main application loop."""
        while self._running:
            try:
                self._show_main_menu()
            except KeyboardInterrupt:
                print_system("\nExiting...")
                self._running = False
            except Exception as e:
                print_error(f"Unexpected error: {e}")
                # Optional: prompt to retry or crash
                if input("Continue? (y/n) > ").lower() != "y":
                    self._running = False

    def _show_main_menu(self) -> None:
        """Display the top-level menu."""
        print_header("TOTM: Theater of the Mind")
        print(f"{BOLD}[ Main Menu ]{RESET}")
        print("(a) New Game")
        print("(b) Load Game")
        print("(c) Save Game")
        print("(d) Create Character")
        print("(e) Play")
        print("(q) Quit")
        print_divider()

        choice = input(f"{CYAN}Select > {RESET}").lower().strip()

        if choice == "a":
            self._new_game()
        elif choice == "b":
            self._load_game()
        elif choice == "c":
            self._save_game()
        elif choice == "d":
            self._create_character()
        elif choice == "e":
            self._play_game()
        elif choice == "q":
            self._running = False
        else:
            print_error("Invalid selection.")

    # -- High-Level Actions ----------------------------------------------

    def _new_game(self) -> None:
        """Initialize a fresh game state."""
        # For prototype, we just reload the world graph from source or template.
        # But StateEngine is persistent in memory. We might need a reset method
        # or re-instantiate outside. For now, assume engine handles reset or we just clear.
        # Since engine is passed in constructor, maybe we just reset variables.
        # Let's assume loading "well.json" is the "New Game"
        from pathlib import Path
        well_path = Path("src/totm/engine/worlds/well.json")
        if well_path.exists():
            from totm.engine.graph import WorldGraph
            new_world = WorldGraph.load(well_path)
            self.engine.world = new_world
            self.engine.set_character(None) # Clear active char
            self.engine.set_location("loc_well_top")
            print_success("New game initialized: Dark Forest")
        else:
            print_error("Could not find world template.")

    def _save_game(self) -> None:
        from pathlib import Path
        save_path = Path("save.json")
        self.engine.save(save_path)
        print_success(f"Game saved to {save_path.absolute()}")

    def _load_game(self) -> None:
        from pathlib import Path
        save_path = Path("save.json")
        if not save_path.exists():
            print_error("No save file found.")
            return
        
        # We need to *replace* the engine instance or update it in place.
        # The clean way is to load a new engine and copy state.
        loaded = StateEngine.load(save_path)
        self.engine.world = loaded.world
        self.engine._character = loaded._character
        self.engine._current_location_id = loaded._current_location_id
        # Re-sync tools? Tools hold a reference to the engine instance, so mutating it in place works.
        print_success("Game loaded.")

    # -- Preparation Phase -----------------------------------------------

    def _create_character(self) -> None:
        """Interactive character creation flow."""
        print_header("Character Creation")
        print_gm("Welcome, traveler. A new destiny awaits.")
        
        name = input("What is your name? > ").strip()
        if not name:
            name = "Hero"

        print("\nChoose your path:")
        print(f"1. {BOLD}Warrior{RESET} (Strong, Tough)")
        print(f"2. {BOLD}Mage{RESET}    (Smart, Fragile)")
        print(f"3. {BOLD}Cleric{RESET}  (Faithful, Healer)")
        print(f"4. {BOLD}Thief{RESET}   (Fast, Sneaky)")
        
        cls_map = {"1": "warrior", "2": "mage", "3": "cleric", "4": "thief"}
        choice = input(f"{CYAN}Select (1-4) > {RESET}").strip()
        char_class = cls_map.get(choice, "warrior")

        # Confirm
        parsed = self.tools.update_character(name, char_class)
        if "error" in parsed:
            print_error(parsed["message"])
            return

        print_success(f"\nCharacter created: {parsed['name']} the {parsed['char_class'].title()}")
        print(f"HP: {parsed['hp']} | Key Stat: {self.engine.character.primary_stat()[0]}")
        input(f"\n{DIM}Press Enter to return to menu...{RESET}")

    # -- Gameplay Phase --------------------------------------------------

    def _play_game(self) -> None:
        """The main gameplay loop."""
        if not self.engine.character:
            print_error("No character created! Go to 'Create Character' first.")
            return

        if not self.engine.current_location:
            print_error("No starting location! (Try New Game)")
            return

        print_header(f"Playing: {self.engine.world.region}")
        print_system(f"Character: {self.engine.character.name}")
        
        # Initial look
        self._handle_tool("get_location", {})

        while True:
            try:
                user_input = input(f"\n{GREEN}> {RESET}").strip()
                if not user_input:
                    continue

                # check triggers
                intent = self.parser.parse(user_input)

                if intent:
                    if intent.tool == "quit":
                        break
                    elif intent.tool == "help":
                        self._show_help()
                        continue
                    
                    # Tool call
                    self._handle_tool(intent.tool, intent.args)
                else:
                    # Narrative input -> GM Agent
                    self._handle_narrative(user_input)

            except KeyboardInterrupt:
                break

    def _handle_tool(self, tool_name: str, args: dict) -> None:
        """Execute a tool and print the result."""
        # Map generic tool names to actual tool calls if needed, or dispatch dynamically
        if tool_name == "get_location":
            res = self.tools.get_location()
            if "error" in res:
                print_error(res["message"])
            else:
                print_gm(f"{BOLD}{res['name']}{RESET}\n{res['description']}")
                if res['npcs']:
                    print(f"{YELLOW}Beings here:{RESET}")
                    for npc in res['npcs']:
                        print(f"- {npc['name']}: {npc['description']} ({'Hostile' if npc['hostile'] else 'Neutral'})")
                if res['inventory']:
                    print(f"{YELLOW}Items visible:{RESET} {', '.join(res['inventory'])}")

        elif tool_name == "get_character":
            res = self.tools.get_character()
            if "error" in res:
                print_error(res["message"])
            else:
                print_divider()
                print(f"{BOLD}{res['name']}{RESET} ({res['char_class']})")
                print(f"HP: {res['hp']} | XP: {res['xp']}")
                print(f"Stats: Brawn {res['brawn']}, Brains {res['brains']}, Faith {res['faith']}, Speed {res['speed']}")
                print(f"Inventory: {', '.join(res['inventory']) or 'Empty'}")
                print_divider()

        elif tool_name == "get_exits":
            res = self.tools.get_exits()
            if "error" in res:
                print_error(res["message"])
            else:
                print(f"\n{BOLD}Exits:{RESET}")
                if not res['exits']:
                    print("No obvious exits.")
                for ex in res['exits']:
                    risk_str = f" [{','.join(ex['risks'])}]" if ex['risks'] else ""
                    print(f"- {BOLD}{ex['direction'].upper()}{RESET} to {ex['destination_name']} ({ex['difficulty']}){risk_str}")
                    print(f"  {DIM}{ex['description']}{RESET}")

    def _handle_narrative(self, text: str) -> None:
        """Handle raw narrative input -> GM Agent."""
        if not self.agent:
            print_system("GM Agent is not connected. (Set GEMINI_API_KEY to enable)")
            return

        thinking_indicator()
        try:
            response = self.agent.send(text)
            print_gm(response)
        except Exception as e:
            print_error(f"Agent error: {e}")

    def _show_help(self) -> None:
        print("\n[ HELP ]")
        print("Commands:")
        print("  look, /look      - Describe current area")
        print("  exits, /exits    - Show paths")
        print("  stats, /stats    - Show character sheet")
        print("  quit, /quit      - Leave game")
        print("Narrative:")
        print("  Just type what you want to do! (e.g. 'I climb down the well')") 
