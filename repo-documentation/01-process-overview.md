# 01 — Process Overview: End-to-End Documentation Workflow

## The documentation lifecycle

Documenting an existing repo follows a predictable lifecycle. Each phase builds on the previous one, starting from surface-level discovery and working toward comprehensive, maintainable documentation.

```
┌─────────────────────────────────────────────────────────┐
│              DOCUMENTATION LIFECYCLE                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. RECONNAISSANCE     Inventory what exists            │
│       │                                                 │
│       ▼                                                 │
│  2. ARCHITECTURE MAP   Understand the system shape      │
│       │                                                 │
│       ▼                                                 │
│  3. SURFACE DOCS       API, data model, config          │
│       │                                                 │
│       ▼                                                 │
│  4. OPERATIONAL DOCS   Deploy, run, troubleshoot        │
│       │                                                 │
│       ▼                                                 │
│  5. GAP ANALYSIS       What's still missing?            │
│       │                                                 │
│       ▼                                                 │
│  6. AGENT ENTRY POINT  Write AGENTS.md                  │
│       │                                                 │
│       ▼                                                 │
│  7. MAINTENANCE        Keep docs fresh                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Phase breakdown

### 1. Reconnaissance (1–2 hours)

**Input**: An existing repository you want to document  
**Output**: Completed reconnaissance checklist with inventory of all components

Activities:
- Map the directory structure
- Read the existing README and any docs/
- Identify the tech stack from config files (package.json, pyproject.toml, etc.)
- List all entry points (main files, CLI commands, API apps)
- List all external dependencies and integrations
- Inventory existing documentation (what's there, what's missing, what's stale)

Key deliverable:
- Completed reconnaissance checklist (see [02-reconnaissance-checklist.md](02-reconnaissance-checklist.md))

**Example (coc_capi)**: Reading `pyproject.toml` revealed FastAPI + SQLAlchemy + Redis + APScheduler. The `render.yaml` exposed the deployment model. The `app/` directory structure showed the service boundaries: api, db, dispatch, ingestion, jobs, services.

### 2. Architecture Map (2–4 hours)

**Input**: Reconnaissance findings  
**Output**: Architecture overview document + service map

Activities:
- Trace the request flow from entry point to response
- Identify service boundaries (web, worker, cron, etc.)
- Map inter-service communication (queues, shared DB, HTTP, etc.)
- Document the deployment topology (what runs where)
- Draw a system diagram (text-based is fine)

Key deliverables:
- `docs/architecture-overview.md` (use [templates/architecture-overview.md.template](templates/architecture-overview.md.template))
- `docs/service-map.md` (use [templates/service-map.md.template](templates/service-map.md.template))

**Example (coc_capi)**: Three runtime processes — web (FastAPI), worker (dispatch), cron jobs (scheduled tasks). All share Postgres and Redis. The web service ingests events, the worker dispatches them to external APIs, cron jobs handle fetch/retry/cleanup.

### 3. Surface Documentation (3–6 hours)

**Input**: Architecture map  
**Output**: API, data model, and configuration docs

Activities:
- Document all API endpoints with request/response shapes
- Document all CLI commands and scripts
- Document all database tables and relationships
- Document all configuration variables and their purpose
- Document external integrations and their contracts

Key deliverables:
- `docs/api-surface.md` (use [templates/api-surface.md.template](templates/api-surface.md.template))
- `docs/data-model.md` (use [templates/data-model.md.template](templates/data-model.md.template))
- `docs/configuration-guide.md` (use [templates/configuration-guide.md.template](templates/configuration-guide.md.template))
- `docs/dependency-inventory.md` (use [templates/dependency-inventory.md.template](templates/dependency-inventory.md.template))

**Example (coc_capi)**: API endpoints in `app/api/` (ingest, admin, health, events, destinations, auth, collect). Database models in `app/db/models/`. Config in `app/core/config.py` and `.env.example`. External integrations: Meta CAPI, TikTok Events API, Google Ads, GA4, Snapchat, Criteo, Askås, Bloomreach.

### 4. Operational Documentation (2–4 hours)

**Input**: Architecture + surface docs  
**Output**: Deployment, operations, and troubleshooting docs

Activities:
- Document how to run the system locally (step-by-step)
- Document the deployment process and environment
- Document monitoring and observability setup
- Write runbooks for common operations (restart, rollback, data fixes)
- Document known failure modes and their resolution

Key deliverables:
- `docs/codebase-onboarding.md` (use [templates/codebase-onboarding.md.template](templates/codebase-onboarding.md.template))
- `docs/deployment-and-infra.md` (use [templates/deployment-and-infra.md.template](templates/deployment-and-infra.md.template))
- `docs/operational-runbook.md` (use [templates/operational-runbook.md.template](templates/operational-runbook.md.template))

**Example (coc_capi)**: Local dev via `docker compose up --build`. Production on Render (web + worker + cron jobs + Postgres + Redis). Monitoring via Prometheus metrics + structured logging. Runbooks for replay, dead-letter retry, destination rollout.

### 5. Gap Analysis (1–2 hours)

**Input**: All documentation produced so far  
**Output**: Prioritized list of documentation gaps

Activities:
- Audit each module/service: is it documented?
- Check each doc for `[UNVERIFIED]` or `[TODO]` markers
- Identify undocumented business logic
- Identify missing error handling documentation
- Identify missing security documentation
- Prioritize gaps: P0 (blocks agent/developer effectiveness), P1 (nice to have)

Key deliverable:
- `docs/documentation-gap-analysis.md` (use [templates/documentation-gap-analysis.md.template](templates/documentation-gap-analysis.md.template))

### 6. Agent Entry Point (1 hour)

**Input**: Complete documentation set  
**Output**: AGENTS.md that orients agents to the repo

Activities:
- Write AGENTS.md as a concise map (<150 lines)
- Define reading order for docs
- List non-negotiable constraints
- Point to bootstrap and configuration docs
- Define coding conventions for the repo

Key deliverable:
- `AGENTS.md` (use [templates/AGENTS.md.template](templates/AGENTS.md.template))

This step comes **last** because you need to know what documentation exists before you can create an effective navigation map.

### 7. Maintenance (ongoing)

**Input**: Completed documentation set  
**Output**: Fresh, accurate documentation

Activities:
- Review docs on a regular cadence (weekly or per-PR)
- Update `Last verified` dates when re-checking docs
- Add documentation updates to PR checklists
- Address `[UNVERIFIED]` and `[TODO]` markers progressively

See [05-maintenance-cadence.md](05-maintenance-cadence.md) for details.

---

## Time estimates

| Phase | Estimated time | Output |
|-------|---------------|--------|
| 1. Reconnaissance | 1–2 hours | Completed inventory checklist |
| 2. Architecture Map | 2–4 hours | Architecture overview + service map |
| 3. Surface Docs | 3–6 hours | API, data model, config, dependencies |
| 4. Operational Docs | 2–4 hours | Onboarding, deployment, runbooks |
| 5. Gap Analysis | 1–2 hours | Prioritized gap list |
| 6. Agent Entry Point | 1 hour | AGENTS.md |
| **Total** | **10–19 hours** | **Complete documentation set** |

For a small repo (< 5k LOC, single service), expect the lower end. For a larger repo (10k+ LOC, multiple services, external integrations), expect the upper end.

## Doing this with an AI agent

This process is well-suited to human-agent collaboration:

| Task | Who | Why |
|------|-----|-----|
| Reconnaissance | Agent | Agents can read file trees and config files systematically |
| Architecture mapping | Human + Agent | Agent reads code; human provides context on intent and history |
| Surface documentation | Agent | Extracting API routes, schemas, config is mechanical |
| Operational docs | Human + Agent | Agent drafts from config; human adds tribal knowledge |
| Gap analysis | Agent | Systematic audit is agent-friendly |
| AGENTS.md | Human | The entry point reflects human priorities |
| Maintenance | Both | Agent flags drift; human decides what matters |
