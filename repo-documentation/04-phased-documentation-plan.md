# 04 — Phased Documentation Plan

## The layer pattern

Documenting a repo works in layers, from structural understanding to operational depth. Each layer has a completion gate — an objective way to know when you're done.

```
Layer 0   Reconnaissance — inventory what exists
Layer 1   Architecture — system shape and components
Layer 2   Interfaces — API, CLI, data model
Layer 3   Configuration — environment, secrets, settings
Layer 4   Operations — run, deploy, troubleshoot, observe, secure
Layer 5   Domain knowledge — business logic, decisions
Layer 6   Gap analysis — what’s still missing (MANDATORY capstone)
Layer 7   Agent entry point — AGENTS.md
```

## Layer design rules

### 1. Each layer should take 1–4 hours

If a layer takes longer, the repo is large enough to split that layer. For example, split Layer 2 into "API documentation" and "data model documentation" and track them separately.

### 2. Each layer has a completion gate

A completion gate is an **objective condition** that tells you the layer is done:

```markdown
# ✅ Good completion gates
- Every top-level module has a one-line description
- Every API endpoint is listed with method, path, and purpose
- Every database table is listed with columns and types
- A new developer can go from clone to running in <15 minutes using only the docs

# ❌ Bad completion gates
- "Documentation looks complete"
- "Most things are covered"
- "Good enough for now"
```

### 3. Layers build on each other

You need the reconnaissance before you can write the architecture. You need the architecture before you can document the API. Don't skip layers.

### 4. Mark unfinished work explicitly

If you move to the next layer with known gaps, mark them with `[TODO]` in the current layer's docs and capture them in the gap analysis.

---

## Layer 0 — Reconnaissance

**Time**: 1–2 hours  
**Input**: Repository access  
**Output**: Completed [02-reconnaissance-checklist.md](02-reconnaissance-checklist.md)

Activities:
- [ ] Map directory structure
- [ ] Identify tech stack from config files
- [ ] List all entry points
- [ ] Inventory existing documentation
- [ ] Note any immediate questions or surprises

**Completion gate**: Every section of the reconnaissance checklist is filled in. You can answer: "What is this system, what stack does it use, how many processes run, and what docs exist?"

---

## Layer 1 — Architecture

**Time**: 2–4 hours  
**Input**: Reconnaissance findings  
**Output**: Two documents

- [ ] `docs/architecture-overview.md` — system shape, component roles, data flow
- [ ] `docs/service-map.md` — every module/package with purpose and key files

Activities:
- [ ] Read main entry points to understand request flow
- [ ] Trace a request from ingestion to completion
- [ ] Identify all runtime processes and their roles
- [ ] Map inter-process communication
- [ ] Draw system diagram (text-based)
- [ ] List every top-level module with its purpose

**Completion gate**: A developer unfamiliar with the repo can read the architecture overview and correctly answer:
1. What does this system do?
2. What are the main components?
3. How do they communicate?
4. What runs in production?

---

## Layer 2 — Interfaces

**Time**: 3–6 hours  
**Input**: Architecture documents  
**Output**: Two documents

- [ ] `docs/api-surface.md` — all endpoints, CLI commands, scripts
- [ ] `docs/data-model.md` — all tables, schemas, state machines

Activities:
- [ ] List every API endpoint with method, path, auth, and purpose
- [ ] Document request/response shapes for key endpoints
- [ ] List every CLI command and script with purpose
- [ ] List every database table with columns and types
- [ ] Document state machines and allowed transitions
- [ ] Document enum values and their meaning

**Completion gate**: Every endpoint returns the expected response shape as documented. Every table's columns match the documentation. State machine transitions are verified against code.

---

## Layer 3 — Configuration

**Time**: 1–2 hours  
**Input**: Code inspection + .env files  
**Output**: Two documents

- [ ] `docs/configuration-guide.md` — all env vars with purpose, type, and defaults
- [ ] `docs/dependency-inventory.md` — all external dependencies and integrations

Activities:
- [ ] List every environment variable with type, default, and purpose
- [ ] Group variables by category (database, security, external APIs, etc.)
- [ ] Document which variables are required vs optional
- [ ] List all Python/Node/etc. package dependencies with versions
- [ ] List all external service integrations with their purpose

**Completion gate**: A developer can configure a new environment using only the configuration guide. No environment variable is undocumented.

---

## Layer 4 — Operations

**Time**: 2–4 hours  
**Input**: Configuration + architecture docs  
**Output**: Three documents

- [ ] `docs/codebase-onboarding.md` — clone to running in <15 minutes
- [ ] `docs/deployment-and-infra.md` — deployment process and infrastructure
- [ ] `docs/operational-runbook.md` — common operations and troubleshooting

Activities:
- [ ] Write step-by-step local development setup
- [ ] Test the setup instructions on a clean environment (or mentally trace)
- [ ] Document the deployment pipeline and targets
- [ ] Document infrastructure components (databases, caches, etc.)
- [ ] Write runbooks for common operations:
  - How to deploy
  - How to rollback
  - How to restart services
  - How to check logs
  - How to handle common errors
  - How to run migrations

**Completion gate**: A new developer can follow the onboarding guide and have the system running locally without asking questions. The runbook covers the 5 most common operational tasks.

---

## Layer 5 — Gap Analysis

**Time**: 1–2 hours  
**Input**: All documentation produced  
**Output**: One document

- [ ] `docs/documentation-gap-analysis.md` — what's documented, what's missing, priorities

Activities:
- [ ] Walk through every module: is it covered in docs?
- [ ] Search all docs for `[UNVERIFIED]`, `[TODO]`, `[ASK]` markers
- [ ] Identify business logic that's only in code (no docs)
- [ ] Identify security concerns that aren't documented
- [ ] Prioritize gaps: P0 (blocks effectiveness) vs P1 (nice to have)
- [ ] Create action items for each gap

**Completion gate**: Every module is either documented or listed as a gap with priority. All `[TODO]` markers from other docs appear in the gap analysis.

---

## Layer 6 — Agent Entry Point

**Time**: 1 hour  
**Input**: Complete documentation set  
**Output**: One document

- [ ] `AGENTS.md` — agent orientation file at repo root

Activities:
- [ ] Write mission statement (one sentence)
- [ ] Create reading order for docs (must match Layer order)
- [ ] List non-negotiable constraints (at least 3)
- [ ] Point to bootstrap/configuration docs
- [ ] Define coding conventions
- [ ] Add safety guardrails (required: secrets policy, escalation triggers, data-loss protection)

**Completion gate**: AGENTS.md is under 150 lines. Every file it references actually exists. An agent reading only AGENTS.md knows where to find any information it needs. Safety guardrails include at least: secrets policy, never-commit rules, and escalation triggers.

---

## Full document checklist

All documents produced across all layers:

| Layer | Document | Template |
|-------|----------|----------|
| 1 | `docs/architecture-overview.md` | `architecture-overview.md.template` |
| 1 | `docs/service-map.md` | `service-map.md.template` |
| 2 | `docs/api-surface.md` | `api-surface.md.template` |
| 2 | `docs/data-model.md` | `data-model.md.template` |
| 3 | `docs/configuration-guide.md` | `configuration-guide.md.template` |
| 3 | `docs/dependency-inventory.md` | `dependency-inventory.md.template` |
| 4 | `docs/codebase-onboarding.md` | `codebase-onboarding.md.template` |
| 4 | `docs/deployment-and-infra.md` | `deployment-and-infra.md.template` |
| 4 | `docs/operational-runbook.md` | `operational-runbook.md.template` |
| 4 | `docs/testing-and-quality.md` | `testing-and-quality.md.template` |
| 4 | `docs/observability-monitoring.md` | `observability-monitoring.md.template` |
| 4 | `docs/security-compliance.md` | `security-compliance.md.template` |
| 5 | `docs/business-logic.md` | `business-logic.md.template` |
| 5 | `docs/decision-log.md` | `decision-log.md.template` |
| 6 | `docs/documentation-gap-analysis.md` | `documentation-gap-analysis.md.template` |
| 7 | `AGENTS.md` | `AGENTS.md.template` |
| 7 | `docs/documentation-index.md` | `documentation-index.md.template` |

---

## Tracking progress

Use this tracker for each layer:

```markdown
### Layer N — [Name]

- Status: not-started / in-progress / done
- Documents produced:
- Time spent:
- Completion gate result: pass / fail
- Open questions:
- Gaps deferred to Layer 5:
```

## Common pitfalls

| Pitfall | Consequence | Prevention |
|---------|-------------|------------|
| Starting with deep dives | Surface gaps remain | Do Layer 0–1 before any deep dives |
| Documenting intent, not behavior | Docs don't match code | Read the code, verify claims |
| Documents too long | Nobody reads them | Split at 300 lines |
| No source citations | Can't verify or update | Always cite file paths |
| Skipping the gap analysis | Think you’re done when you’re not | Layer 6 is mandatory — never skip it |
| Writing AGENTS.md first | Points to docs that don’t exist yet | AGENTS.md is Layer 7, not Layer 0 |
| Ignoring [ASK] markers | Business context lost, docs stay shallow | Track all [ASK] items in gap analysis |
