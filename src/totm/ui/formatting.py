"""Rich text formatting utilities for the TOTM console."""

import sys
import time
import shutil

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"


def print_header(text: str) -> None:
    """Print a bold, centered header with a divider."""
    width = shutil.get_terminal_size().columns
    print(f"\n{BOLD}{CYAN}{text.center(width)}{RESET}")
    print(f"{DIM}{'=' * width}{RESET}\n")


def print_divider() -> None:
    """Print a dim horizontal divider."""
    width = shutil.get_terminal_size().columns
    print(f"{DIM}{'-' * width}{RESET}")


def print_gm(text: str) -> None:
    """Print GM narration text."""
    # Simple wrap or let terminal handle it.
    # For now, just print with some spacing.
    print(f"\n{text}\n")


def print_system(text: str) -> None:
    """Print system messages (saves, errors, info)."""
    print(f"{DIM}[SYSTEM] {text}{RESET}")


def print_error(text: str) -> None:
    """Print error messages."""
    print(f"{RED}Error: {text}{RESET}")


def print_success(text: str) -> None:
    """Print success messages."""
    print(f"{GREEN}{text}{RESET}")


def thinking_indicator(duration: float = 1.0) -> None:
    """Show a simple 'Thinking...' animation."""
    chars = [".  ", ".. ", "..." ]
    end_time = time.time() + duration
    
    sys.stdout.write(f"{DIM}GM is thinking{RESET}")
    while time.time() < end_time:
        for char in chars:
            sys.stdout.write(f"{DIM}{char}{RESET}")
            sys.stdout.flush()
            time.sleep(0.3)
            sys.stdout.write("\b\b\b")  # Backspace 3 chars
    
    # Clear the line
    sys.stdout.write("\r" + " " * 20 + "\r")
    sys.stdout.flush()
