Yes—there are already a few fairly mature “LLM-as-GM” systems that are exactly this.

If by “theater of the mind” you mean: no formal grid, no UI-heavy VTT, just conversation, rules, and shared imagination with the model acting as GM, then we’re basically talking about a continuum that runs from AI Dungeon–style sandboxes to more rules‑anchored proto-systems. Let me sketch the landscape and where people have actually built things.

Existing “LLM GM” / theater‑of‑the‑mind systems

The most on-the-nose example in your search results is AI Dungeon, which is built around an LLM playing all roles in a text adventure / RPG and is often run as pure prose with no map or visuals. In practice it’s a very loose “system,” but structurally it already has:

- A GM/narrator role handled by the model

- PC stats / inventory / world state tracked in hidden or semi‑hidden metadata

- Freeform player inputs, often in natural language, with the model adjudicating outcomes

That’s very much “theater of the mind” plus a thin, mutable ruleset. ​⁠https://www.skillshare.com/en/classes/ai-and-gaming-large-language-models/830670154?srsltid=AfmBOoqxpCZaHxYiUeEBDcADPNTMQ-FFfQ8zjjNQudjJ6L9Y726NFfWW

The Infinite Worlds project goes further toward the thing you’re describing, just in audio form rather than text. It explicitly positions itself as a screenless, LLM-driven, audio‑only RPG: you talk, it talks back, and everything from narration to consequences is handled by an “invisible game engine” under the hood. It’s still theater-of-the-mind, just mediated through headphones rather than a chat window. ​⁠https://www.sngular.com/insights/450/infinite-worlds-when-the-best-graphic-is-your-imagination

Outside those, there’s a growing ecosystem of:

- Bots in Discord/Telegram that run solo text RPGs with persistent character sheets

- Homebrew tools where folks glue GPT‑like models to a rules engine (5e, OSR, story games, etc.), using the LLM as a narrative layer on top of deterministic mechanics

- Academic and indie prototypes where the LLM is explicitly cast as “Narrator/GM agent” in multi‑agent setups

The Gallotta et al. “Large Language Models and Games” survey has an entire section on LLMs as narrators, quest generators, and dungeon masters, although most examples are more experimental than productized. ​⁠https://arxiv.org/html/2402.18659v5

So: nobody has “the” definitive, standardized system that’s become the D&D of LLM TotM, but multiple attempts absolutely exist and are converging on that pattern.

What seems novel and still unsolved

Where things are still janky (and where you could plausibly do something interesting):

- Separation of rules from narration.
Most current systems either let the LLM hallucinate mechanics or bury the rules in prompt spaghetti. A cleaner design would treat the LLM purely as narrative+interpretation, with a transparent stateful rules engine making authoritative calls.

- Stable, referenceable spatial abstraction.
In human TotM, a good GM keeps a consistent sense of space without a grid. LLMs are notoriously bad at this unless you give them a structured representation (zones, fronts, clocks). A robust “LLM‑friendly ToM spatial/temporal model” is still an open design space.

- Long‑term campaign memory.
Persistent world state over many sessions—NPC relationships, consequences, evolving fronts—remains brittle without some explicit data model and retrieval strategy. Most current implementations punt to a vector DB of blobs and hope.

- Tone and genre discipline.
AI Dungeon–style systems are famous for tonal whiplash. A real “system” would probably bake in genre constraints, pacing rules, and maybe an underlying dramatic structure (e.g., story beats or clocks) and let the LLM color inside those lines.

- Multi‑player dynamics.
Most “LLM GM” tools are optimized for solo play. Handling 3–5 PCs, spotlight balance, and cross‑player dependencies is still underexplored.

If you’re thinking about building one

Given your background, you’re exactly the kind of person who could turn this from “prompt hack” into an actual system. The pattern that seems most promising to me is:

1. Rules and world as explicit data + code.
Think: JSON/YAML definitions for entities and moves, plus a deterministic rules engine (maybe a little ECS‑ish).

2. LLM as interface + narrative layer.
It interprets player natural language into intents/actions against that engine, and then turns the engine’s outcomes back into rich prose.

3. Theater‑of‑the‑mind abstractions baked into the model of space.
Zones, ranges (“close / near / far”), soft clocks for escalating danger, fronts, etc., instead of grids and coordinates.

4. Campaign memory as first‑class.
A structured log of scenes, flags, and relationship changes that the LLM can query, not just raw transcript embeddings.

You’d end up with something that feels closer to a story‑game engine (think PbtA, Fate, etc.) than to 5e, but with a very human‑ish “GM” living in the gaps.

