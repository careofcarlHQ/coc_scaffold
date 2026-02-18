# Agent-First Development Scaffolds

Reusable frameworks for agent-first software development — covering the full lifecycle from building something new to handling production emergencies.

## Repository layout

- Framework scaffolds (core content):
	- `greenfield/`, `repo-documentation/`, `refactoring/`, `feature-addition/`, `bug-investigation/`, `testing-retrofit/`, `migration/`, `incident-response/`, `spike/`
- Repository automation:
	- `scripts/` and `AGENTS.md`
- Validation harness:
	- `tests/`, `.github/workflows/`, `.coveragerc`
- Internal self-application artifacts:
	- `meta/self-application/`

## Scaffolds

### Core scaffolds

| Scaffold | Purpose | Start here |
|----------|---------|------------|
| [greenfield/](greenfield/) | Build a new project from scratch using spec-first, agent-driven development | [greenfield/README.md](greenfield/README.md) |
| [repo-documentation/](repo-documentation/) | Systematically document an existing codebase for humans and agents | [repo-documentation/README.md](repo-documentation/README.md) |
| [refactoring/](refactoring/) | Systematically refactor an existing codebase with safety gates and behavior preservation | [refactoring/README.md](refactoring/README.md) |

### Day-to-day scaffolds

| Scaffold | Purpose | Start here |
|----------|---------|------------|
| [feature-addition/](feature-addition/) | Add a feature to an existing codebase with impact analysis and verification | [feature-addition/README.md](feature-addition/README.md) |
| [bug-investigation/](bug-investigation/) | Diagnose and fix bugs with hypothesis-driven investigation and regression guards | [bug-investigation/README.md](bug-investigation/README.md) |
| [testing-retrofit/](testing-retrofit/) | Add meaningful test coverage to an under-tested codebase | [testing-retrofit/README.md](testing-retrofit/README.md) |

### Operational scaffolds

| Scaffold | Purpose | Start here |
|----------|---------|------------|
| [migration/](migration/) | Move between technologies, versions, or platforms with rollback safety | [migration/README.md](migration/README.md) |
| [incident-response/](incident-response/) | Handle production incidents with structured triage, mitigation, and post-mortems | [incident-response/README.md](incident-response/README.md) |
| [spike/](spike/) | Time-boxed technical exploration to answer questions before committing to implementation | [spike/README.md](spike/README.md) |

## Which scaffold do I need?

```
"I need to build something new"              → greenfield/
"I need to understand existing code"         → repo-documentation/
"I need to reshape existing code"            → refactoring/
"I need to add a feature"                    → feature-addition/
"Something is broken and I need to fix it"   → bug-investigation/
"I need to add tests to untested code"       → testing-retrofit/
"I need to change technologies/versions"     → migration/
"Production is on fire RIGHT NOW"            → incident-response/
"Should we build this? Is this feasible?"    → spike/
```

## How they relate

```
spike/ ──────────→ greenfield/          "Should we?" → "Let's build it"
spike/ ──────────→ feature-addition/    "Should we?" → "Let's add it"
spike/ ──────────→ migration/           "Should we?" → "Let's move"

repo-documentation/ → refactoring/      "What is this?" → "Let's improve it"
refactoring/ ←────── testing-retrofit/  Tests first, then refactor safely

feature-addition/ ──→ bug-investigation/ Feature shipped, bug found
bug-investigation/ ──→ testing-retrofit/ Bug found, need more tests

incident-response/ ──→ bug-investigation/ Mitigated, now fix properly
incident-response/ ──→ testing-retrofit/  Post-mortem: need test coverage
```

## Self-application

The framework is being applied to itself with durable tracking artifacts in:

- [meta/self-application/README.md](meta/self-application/README.md)
- [meta/self-application/testing-retrofit/testing-checklist.md](meta/self-application/testing-retrofit/testing-checklist.md)
- [meta/self-application/solo-copilot-process.md](meta/self-application/solo-copilot-process.md)
- [meta/self-application/gold-standard/README.md](meta/self-application/gold-standard/README.md)

## Solo + Copilot merge automation

For this repository, merge automation is standardized via:

- [AGENTS.md](AGENTS.md)
- [scripts/solo-merge-pr.ps1](scripts/solo-merge-pr.ps1)

When asked to merge a PR (for example: "Merga PR#3"), run:

- `./scripts/solo-merge-pr.ps1 -PullNumber <PR_NUMBER>`

This flow temporarily enables solo mode, merges, restores team mode, verifies branch protection, then syncs local `main` and cleans up the local feature branch.

## Shared principles

All scaffolds share the same core values:

- **Repository as system of record** — everything the agent needs lives in the repo
- **AGENTS.md as navigation entry point** — agents know where to start
- **Progressive disclosure over front-loading** — layer in detail as needed
- **Objective quality gates over subjective judgment** — evidence, not opinions
- **Human steers, agent executes** — humans define intent, agents write code

## Origin

These scaffolds are distilled from the `coc_agent_process` project — a Postgres-backed multi-agent engineering support system built entirely through human-agent collaboration between February 2026 and onwards.
