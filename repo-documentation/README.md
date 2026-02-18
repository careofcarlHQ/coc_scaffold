# Repo Documentation Scaffold

A reusable framework for systematically documenting existing codebases — the reverse companion to the [greenfield project scaffold](../greenfield/).

Where the project scaffold goes **forward** (design → build), this framework works **backward** (code → document). It gives you a repeatable process for turning an undocumented or partially documented repository into an agent-readable, human-navigable knowledge base.

## Who is this for?

Any developer or team that:

- Has an existing codebase with incomplete or scattered documentation
- Wants to make their repo usable by AI coding agents
- Needs to onboard new developers (human or AI) quickly
- Wants to understand what they actually have before planning the next phase
- Needs a documentation audit process that doesn't take months

## What makes this approach different?

1. **Code-first, docs-second** — the code is the source of truth; docs describe what exists, not what was planned
2. **Phased discovery** — systematic layers from structure → architecture → API → data → operations
3. **Agent-oriented output** — documentation structured so agents can navigate and use the repo effectively
4. **Evidence-based** — every claim in the docs should trace back to actual code or config
5. **Living documents** — built-in maintenance cadence to prevent rot

## How to use this scaffold

1. Read [00-philosophy.md](00-philosophy.md) to understand the principles
2. Read [01-process-overview.md](01-process-overview.md) for the end-to-end workflow
3. Run the [02-reconnaissance-checklist.md](02-reconnaissance-checklist.md) against your repo
4. Use [03-documentation-writing-guide.md](03-documentation-writing-guide.md) to write your docs
5. Follow [04-phased-documentation-plan.md](04-phased-documentation-plan.md) to work through layers
6. Set up [05-maintenance-cadence.md](05-maintenance-cadence.md) for ongoing freshness
7. Use [06-agents-md-for-existing-repos.md](06-agents-md-for-existing-repos.md) to write the agent entry point
8. Feed your agent [07-agent-prompts.md](07-agent-prompts.md) for automated extraction
9. Validate results with [08-verification-and-quality.md](08-verification-and-quality.md)

## Document Index

| File | Purpose |
|------|---------|
| [00-philosophy.md](00-philosophy.md) | Core principles for documenting existing code |
| [01-process-overview.md](01-process-overview.md) | End-to-end documentation workflow |
| [02-reconnaissance-checklist.md](02-reconnaissance-checklist.md) | Systematic audit with extraction commands |
| [03-documentation-writing-guide.md](03-documentation-writing-guide.md) | How to write docs that agents and humans can use |
| [04-phased-documentation-plan.md](04-phased-documentation-plan.md) | Layered documentation with completion gates |
| [05-maintenance-cadence.md](05-maintenance-cadence.md) | Keeping docs fresh over time |
| [06-agents-md-for-existing-repos.md](06-agents-md-for-existing-repos.md) | Writing AGENTS.md for a repo that already has code |
| [07-agent-prompts.md](07-agent-prompts.md) | Concrete extraction prompts for automated doc generation |
| [08-verification-and-quality.md](08-verification-and-quality.md) | Quality scoring, verification checks, drift detection |
| [templates/](templates/) | Copy-paste starter templates |

## Templates

| Template | Layer | Purpose |
|----------|-------|---------|
| [AGENTS.md.template](templates/AGENTS.md.template) | 7 | Agent entry point for an existing repo |
| [architecture-overview.md.template](templates/architecture-overview.md.template) | 1 | Reverse-engineered architecture doc |
| [service-map.md.template](templates/service-map.md.template) | 1 | Module/service responsibilities |
| [api-surface.md.template](templates/api-surface.md.template) | 2 | Endpoint/CLI/interface inventory |
| [data-model.md.template](templates/data-model.md.template) | 2 | Schema and state machine documentation |
| [configuration-guide.md.template](templates/configuration-guide.md.template) | 3 | Environment variables and settings |
| [dependency-inventory.md.template](templates/dependency-inventory.md.template) | 3 | External dependencies and integrations |
| [codebase-onboarding.md.template](templates/codebase-onboarding.md.template) | 4 | New contributor quick-start |
| [deployment-and-infra.md.template](templates/deployment-and-infra.md.template) | 4 | Where and how the system runs |
| [operational-runbook.md.template](templates/operational-runbook.md.template) | 4 | Common operations and troubleshooting |
| [testing-and-quality.md.template](templates/testing-and-quality.md.template) | 4 | Test strategy, coverage, quality tooling |
| [observability-monitoring.md.template](templates/observability-monitoring.md.template) | 4 | Metrics, logs, alerts, dashboards |
| [security-compliance.md.template](templates/security-compliance.md.template) | 4 | PII, auth, encryption, compliance |
| [business-logic.md.template](templates/business-logic.md.template) | 5 | Domain rules, workflows, data transformations |
| [decision-log.md.template](templates/decision-log.md.template) | 5 | Discovered architectural decisions (ADR-style) |
| [documentation-gap-analysis.md.template](templates/documentation-gap-analysis.md.template) | 6 | What's documented, what's missing (MANDATORY capstone) |
| [documentation-index.md.template](templates/documentation-index.md.template) | 7 | Master index for all docs |

## Relationship to the Project Scaffold

```
Project Scaffold (forward)          Repo Documentation (backward)
─────────────────────────           ────────────────────────────
PRD → Specs → Code                  Code → Discovery → Docs
"What should we build?"             "What do we actually have?"
Design-first                        Evidence-first
Creates new repos                   Documents existing repos
```

Both frameworks share the same core values:
- Repository as system of record
- AGENTS.md as navigation entry point
- Progressive disclosure over front-loading
- Objective quality gates over subjective judgment

## Origin

Built as a companion to the agent-first project scaffold, based on the experience of documenting `coc_capi` — a production FastAPI service with API, worker, cron jobs, admin UI, and multiple external integrations that needed systematic documentation for agent-assisted development.
