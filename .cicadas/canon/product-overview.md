# Product Overview: TOTM (Theater of the Mind)

**TOTM** is a text-based Role-Playing Game engine where an AI Game Master (GM) dynamically narrates the adventure while referring to a deterministic rule system for adjudication.

## Goal
To blend the infinite creativity of Large Language Models (LLMs) with the consistency and challenge of structured game mechanics.

## Problem Statement
- **Traditional RPGs** (D&D) require a human GM to play.
- **Solo RPGs** (Gamebooks, CRPGs) are limited by pre-written paths.
- **Pure AI RPGs** (Chatbot games) suffer from hallucination, lack of challenge, and forgotten state.

## Solution
TOTM introduces a **Split-Brain Architecture**:
1.  **The Engine (System 2)**: A rigid, graph-based world state and stat-based rule system that handles truth.
2.  **The Agent (System 1)**: A creative persona that narrates the world and translates player intent into engine commands.

## Key Features
-   **AI Game Master**: A persona-driven agent that narrates scenes, plays NPCs, and referees the game.
-   **Deterministic Rules**: Success/failure is determined by stats and dice, not the AI's whim.
-   **Arbitrated State**: The AI uses tools (`get_location`, `traverse`, `interact`) to perceive and manipulate the world.
-   **Terminal Interface**: A retro-styled command-line interface for immersive text play.

## User Personas
-   **The Solo Adventurer**: Wants a D&D-like experience without scheduling a group.
-   **The Tinkerer**: Wants to experiment with AI-driven game mechanics and world-building.
