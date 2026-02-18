# 06 — Writing AGENTS.md for Existing Repos

## How this differs from new-project AGENTS.md

For a new project, AGENTS.md is written early and evolves as the project grows. For an existing repo, AGENTS.md is written **after** the documentation exists — it's a navigation layer over an already-built system.

Key differences:

| Aspect | New project | Existing repo |
|--------|-------------|---------------|
| When to write | Day 1 (inception) | After documentation layers are complete |
| Primary purpose | Guide what to build | Guide how to navigate and modify |
| Source of truth | Specs and checklists | Docs and code |
| Key sections | Build phases, acceptance gates | Module map, conventions, gotchas |
| Evolves with | Implementation progress | Code changes and doc updates |

## Structure template for existing repos

```markdown
# AGENTS.md — {project_name}

## Mission
One-sentence description of what this system does.

## Repository Map (read in this order)
1. This file — agent orientation
2. `docs/architecture-overview.md` — system shape and components
3. `docs/service-map.md` — module responsibilities
4. `docs/api-surface.md` — all endpoints and commands
5. `docs/data-model.md` — database schema and state machines
6. `docs/configuration-guide.md` — environment variables
7. `docs/codebase-onboarding.md` — how to run locally

## System Architecture (quick reference)
- Brief description of runtime processes
- Brief description of how they communicate
- Brief description of where it's deployed

## Key Modules
Short table: module → purpose → key files

## Non-Negotiable Constraints
- Constraint 1 (e.g., "All API changes must update docs/api-surface.md")
- Constraint 2 (e.g., "Never commit secrets or .env files")
- Constraint 3 (e.g., "Database changes require Alembic migration")

## Coding Conventions
- Style/formatting rules
- Import conventions
- Error handling patterns
- Testing expectations

## Common Tasks
- How to add a new endpoint
- How to add a database migration
- How to add a new destination/integration
- How to run tests

## Known Gotchas
- Things that aren't obvious from the code
- Historical decisions that might seem wrong but are intentional
- Areas of tech debt to be aware of

## Safety
- Where secrets are configured
- What must never be committed
- When to stop and ask a human
```

## What to include

### Module map (essential)

This is the most valuable section for an existing repo — it tells the agent where things are:

```markdown
## Key Modules
| Module | Purpose | Key files |
|--------|---------|-----------|
| app/api/ | HTTP endpoints | ingest.py, admin.py, health.py |
| app/core/ | Configuration and utilities | config.py, security.py, redis.py |
| app/db/ | Database models and queries | models/, repository.py, session.py |
| app/dispatch/ | Event dispatch worker | worker.py |
| app/ingestion/ | Event ingestion pipeline | pipeline.py |
| app/jobs/ | Scheduled cron jobs | fetch_askas_orders.py, retry_dead_letters.py |
| app/schemas/ | Pydantic schemas | event.py, admin.py, destination.py |
| app/services/ | Business logic | dispatch.py, replay.py, stats.py |
```

### Common tasks (highly valuable)

Agents frequently need to make specific kinds of changes. Document the pattern:

```markdown
## How to add a new API endpoint
1. Create route function in `app/api/{module}.py`
2. Add Pydantic schema in `app/schemas/{module}.py`
3. Register router in `app/main.py`
4. Add endpoint to `docs/api-surface.md`
5. Add test in `tests/test_{module}.py`

## How to add a database migration
1. Modify model in `app/db/models/{model}.py`
2. Run `poetry run alembic revision --autogenerate -m "description"`
3. Review generated migration in `app/db/migrations/versions/`
4. Update `docs/data-model.md`
5. Test with `poetry run alembic upgrade head`
```

### Known gotchas (prevents wasted time)

These save agents (and humans) from stumbling into known issues:

```markdown
## Known Gotchas
- The `dispatch_queue` table uses polling, not LISTEN/NOTIFY. Don't try to
  add PG notifications — it was tried and reverted due to connection issues.
- The `FERNET_KEY` must be exactly 32 url-safe base64 bytes. Use
  `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`.
- Redis is optional for local dev — the worker falls back to DB-only mode.
  But tests assume Redis is available.
```

## What NOT to include

| Don't include | Why | Where it belongs |
|---------------|-----|-----------------|
| Full API documentation | Too long, duplicates api-surface.md | docs/api-surface.md |
| Database schema details | Too long, duplicates data-model.md | docs/data-model.md |
| Step-by-step deployment instructions | Too long, changes frequently | docs/deployment-and-infra.md |
| Historical decision log | Not relevant to current work | docs/ or ADR directory |
| Long code examples | Crowds out navigation | docs/ or inline code comments |

## Validation checklist

- [ ] Under 150 lines
- [ ] Mission is one sentence
- [ ] Repository map lists docs in reading order
- [ ] Every referenced file actually exists
- [ ] Module map covers all top-level packages
- [ ] Common tasks cover the 3–5 most frequent changes
- [ ] Gotchas include at least the top 3 non-obvious things
- [ ] Constraints are rules, not suggestions
- [ ] Safety section mentions secrets handling

## Evolution

AGENTS.md for existing repos evolves differently than for new projects:

1. **Initial**: Written after Layer 6 of the documentation plan
2. **Per-PR**: Updated when modules are added/renamed or conventions change
3. **Monthly**: Quick review — do all links resolve? Are gotchas still relevant?
4. **Major refactor**: Full rewrite if architecture changes significantly
