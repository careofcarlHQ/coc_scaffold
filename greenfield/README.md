# Greenfield Project Scaffold

A reusable scaffold specification for building software projects from scratch using the agent-first development process pioneered in `coc_agent_process`.

The methodology was developed over the course of building a multi-agent PR pipeline from zero — starting with process documentation, then layering in specs, implementation checklists, acceptance gates, and operational tooling — all driven by human-agent collaboration.

## Who is this for?

Any solo developer or small team that wants to:

- Build software using AI coding agents as primary implementers
- Maintain production-grade quality without large teams
- Move from ad-hoc "chat and paste" coding to structured delivery
- Scale throughput without scaling headcount

## What makes this approach different?

1. **Spec-first, code-second** — write the contracts before touching code
2. **Phased checklists with acceptance gates** — no stage advances without evidence
3. **Human steers, agent executes** — humans define intent and constraints, agents write code
4. **Repository is the system of record** — everything the agent needs lives in the repo
5. **Built-in safety** — escalation policies, cost caps, and merge gates by default

## How to use this scaffold

1. Read [00-philosophy.md](00-philosophy.md) to understand the principles
2. Read [01-process-overview.md](01-process-overview.md) for the end-to-end workflow
3. Copy files from [templates/](templates/) into your new project
4. Follow [02-project-kickoff-checklist.md](02-project-kickoff-checklist.md) to bootstrap
5. Use [03-spec-writing-guide.md](03-spec-writing-guide.md) to write your specs
6. Build using [04-phased-implementation-guide.md](04-phased-implementation-guide.md)
7. Operate using [05-operational-cadence.md](05-operational-cadence.md)

## Document Index

| File | Purpose |
|------|---------|
| [00-philosophy.md](00-philosophy.md) | Core principles and lessons learned |
| [01-process-overview.md](01-process-overview.md) | End-to-end development workflow |
| [02-project-kickoff-checklist.md](02-project-kickoff-checklist.md) | Bootstrap a new project from zero |
| [03-spec-writing-guide.md](03-spec-writing-guide.md) | How to write specs that agents can execute |
| [04-phased-implementation-guide.md](04-phased-implementation-guide.md) | Phased build with acceptance gates |
| [05-operational-cadence.md](05-operational-cadence.md) | Weekly review and continuous improvement |
| [06-agents-md-guide.md](06-agents-md-guide.md) | How to write an effective AGENTS.md |
| [07-evidence-and-quality.md](07-evidence-and-quality.md) | Evidence templates and quality tracking |
| [templates/](templates/) | Copy-paste starter templates |

## Origin

This scaffold is distilled from the `coc_agent_process` project — a Postgres-backed multi-agent engineering support system built entirely through human-agent collaboration between February 2026 and onwards. The project went from an empty repository to a working system with API, worker, database, UI, and live GitHub/OpenAI integrations across three implementation phases.
