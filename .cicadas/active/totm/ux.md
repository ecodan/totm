# UX Design: TOTM (Theater of the Mind)

## Menu & Phases

### Main Menu
The application starts at a terminal-style main menu providing entry points for the lifecycle of a game:
- **(a) New Game**: Initialize a fresh world and epoch.
- **(b) Load Game**: Resume a previously saved epoch/state.
- **(c) Save Game**: Commit the current state and narrative synthesis to disk.
- **(d) Create Character**: Enter the **Preparation Phase**.
- **(e) Play**: Enter the **Gameplay Phase** (requires a character).

---

## User Flows

### Flow 1: Preparation Phase (In-Universe Character Creation)
1. **User** selects "Create Character" from the Main Menu.
2. **GM** adopts a narrative persona (e.g., an Old Hermit, a Recruiter, or a Mirror) and begins an in-universe dialogue.
3. **User** explores their identity through conversation; the GM subtly maps this to **Solid Ground** attributes.
4. **GM** summarizes the character's "nature" and confirms the finalized stats.
5. **System** saves the character and returns to the Main Menu.

### Flow 2: Gameplay Phase (Serial & Voice-Friendly)
1. **User** selects "Play" from the Main Menu.
2. **System** loads the current Region/Sub-region and Character.
3. **GM** provides a narrative prompt, occasionally weaving in key state (e.g., "[HP: 8/10]").
4. **User** responds with prose actions or **Plain Text Triggers** (e.g., "tell me my stats").
5. **GM** adjudicates, updates state, and responds with narrative.

---

## Serial Interaction & Commands

Instead of a split screen, TOTM uses a "Serial Flow" where the narrative log is the primary interface. The user can explicitly query the "Solid Ground" using slash commands.

### Interaction Triggers
Instead of just slash commands, which are hard to use via voice, TOTM supports **Plain Text Triggers** that the GM interprets.

| Intent | Slash Command | Plain Text Equivalent (Voice-Friendly) |
|---------|---------------|-----------------------------------------|
| Character Status | `/stats` | "What are my stats?", "How am I doing?" |
| Inventory | `/inv` | "Check my bag", "What am I carrying?" |
| World Info | `/map` | "Where am I?", "What's the area like?" |
| Help | `/help` | "I'm lost", "Help me" |

> [!TIP]
> **Topical Insertion**: The GM should proactively mention crucial state changes in the narrative (e.g. "The trap springs! You take 2 damage [HP: 8/10]") to reduce the need for manual querying.

---

## UI States

### The Console
- **Default/Active**: A clean command-line interface. LLM text is formatted for readability.
- **Interactive**: The prompt `> ` where the user types.
- **Loading/GM Thinking**: A subtle "..." or pulsing character to show the GM is processing rules/states.
- **Menu State**: A formatted list of options (a-e).

## Mockups (Serial Console)

```text
[ TOTM: Theater of the Mind ]

(a) New Game
(b) Load Game
(c) Save Game
(d) Create Character
(e) Play

Selection > e

--- PLAYING: The Dark Forest ---

GM: The canopy above is thick, blotting out the stars. You stand 
at the mouth of an abandoned well. The air is cold.

> /stats

[ CHARACTER INFO ]
Name: Dan the Brave
HP: 10/10
Power: 5
Location: Dark Forest > Abandoned Well

> I descend into the well, holding my lantern high.

GM: (Thinking...)
The stones are slippery, but your grip is firm. As you reach the 
bottom, your lantern illuminates a heavy, rusted chest.

> /inv

[ INVENTORY ]
- Lantern (Lit)
- Rusted Key
- Dried Rations

>
```
