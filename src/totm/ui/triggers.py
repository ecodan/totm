"""Plain Text Trigger parser — maps natural language to tool intents."""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class Intent:
    """A parsed user intent."""
    tool: str
    args: dict[str, str]
    confidence: float


class TriggerParser:
    """Parses user input for specific command patterns."""

    # Regex patterns for various tools.
    # Order matters: more specific patterns first.
    PATTERNS = [
        # Character Status
        (r"(?i)^(?:check|show|what are|my)?\s*stats?$", "get_character", {}),
        (r"(?i)^(?:/?)(?:how am i.*|status|health|hp)$", "get_character", {}),
        
        # Inventory
        (r"(?i)^(?:check|show|open|my)?\s*(?:bag|inventory|items?|gear)$", "get_character", {}), # Inventory is part of character info now, or we could filter
        (r"(?i)^/inv(?:entory)?$", "get_character", {}),

        # World Info / Look
        (r"(?i)^(?:look|l|where am i|look around|describe|scan)$", "get_location", {}),
        (r"(?i)^(?:/map|/look)$", "get_location", {}),

        # Exits
        (r"(?i)^(?:exits|paths|ways out|directions)$", "get_exits", {}),
        
        # Help
        (r"(?i)^(?:help|what can i do\??)$", "help", {}),
        
        # Quit
        (r"(?i)^(?:quit|exit|stop)$", "quit", {}),
    ]

    def parse(self, text: str) -> Optional[Intent]:
        """Attempt to parse text into a structured Intent.
        
        Returns None if no specific command trigger is matched (implies strictly narrative input).
        """
        text = text.strip()
        if not text:
            return None

        # Check plain text regex triggers
        for pattern, tool, args in self.PATTERNS:
            if re.match(pattern, text):
                return Intent(tool=tool, args=args, confidence=1.0)

        # Check specific slash commands if any remain that aren't regex'd
        if text.startswith("/"):
            # Fallback simple slash command parser? 
            # For now, if it didn't match regex, maybe we handle it or treat as narrative.
            pass

        return None
