# Cicadas Agents

This file registers the agents and subagents of the Cicadas SDD methodology for this project. Antigravity uses these definitions to route tasks to specialized roles.

## Core Agents

### Chorus
**Role**: The Cicadas Orchestrator.
**Focus**: Branch registration, intent tracking, snapshot synthesis, and project lifecycle management.
**Entry Point**: [CHORUS.md](file:///Users/dan/dev/code/ai/totm/scripts/chorus/CHORUS.md)
**Instructions/Skills**: Uses the `chorus` skill in [SKILL.md](file:///Users/dan/dev/code/ai/totm/scripts/chorus/SKILL.md).

## Emergence Subagents (The Forward Path)

These agents handle the progressive refinement of ideas into actionable specifications in the project's incubator.

### Clarify
**Role**: Rigorous Product Manager.
**Focus**: Defining "What" and "Why". Transforms vague ideas into Product Requirement Documents (PRD).
**Prompt**: [clarify.md](file:///Users/dan/dev/code/ai/totm/scripts/chorus/emergence/clarify.md)

### UX
**Role**: Interaction Designer.
**Focus**: Experience and interaction flows.
**Prompt**: [ux.md](file:///Users/dan/dev/code/ai/totm/scripts/chorus/emergence/ux.md)

### Tech
**Role**: Software Architect.
**Focus**: Technical design, data flow, and schemas.
**Prompt**: [tech-design.md](file:///Users/dan/dev/code/ai/totm/scripts/chorus/emergence/tech-design.md)

### Approach
**Role**: Strategy Lead.
**Focus**: Implementation strategy, risks, and migration paths.
**Prompt**: [approach.md](file:///Users/dan/dev/code/ai/totm/scripts/chorus/emergence/approach.md)

### Tasks
**Role**: Technical Executor.
**Focus**: Transforming design into an ordered, testable checklist.
**Prompt**: [tasks.md](file:///Users/dan/dev/code/ai/totm/scripts/chorus/emergence/tasks.md)
