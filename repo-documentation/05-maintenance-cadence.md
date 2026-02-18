# 05 — Maintenance Cadence

## Why docs rot

Documentation doesn't go stale all at once. It rots incrementally:

1. A new endpoint is added — API docs don't mention it
2. An env var is renamed — config guide still uses the old name
3. A table gets a new column — data model doc is missing it
4. Deployment moves from Heroku to Render — deploy docs still say Heroku

Each change is small. The cumulative effect is documentation that actively misleads.

## The freshness model

Every document has a **freshness window** — how long it stays reliable without re-verification.

| Document type | Freshness window | Why |
|---------------|-----------------|-----|
| Architecture overview | 3 months | Architecture changes slowly |
| Service map | 2 months | Modules occasionally added/renamed |
| API surface | 2 weeks | Endpoints change frequently |
| Data model | 1 month | Schema changes with migrations |
| Configuration guide | 1 month | Env vars added/changed with features |
| Dependency inventory | 2 months | Dependencies change with updates |
| Onboarding guide | 1 month | Setup steps change with tooling |
| Deployment guide | 2 months | Infrastructure changes are infrequent |
| Operational runbook | 2 months | Operations are relatively stable |
| AGENTS.md | 1 month | Should reflect current project state |

## Maintenance strategies

### Strategy 1: PR-triggered updates (recommended)

Add documentation checks to your PR process:

```markdown
## PR Checklist
- [ ] If I added/changed an API endpoint: updated `docs/api-surface.md`
- [ ] If I added/changed a DB table/column: updated `docs/data-model.md`
- [ ] If I added/changed an env var: updated `docs/configuration-guide.md`
- [ ] If I changed deployment config: updated `docs/deployment-and-infra.md`
- [ ] If I added a new module: updated `docs/service-map.md`
```

This is lightweight and catches changes at the source. It doesn't work for everything (architecture-level changes, subtle behavior shifts), but it catches the most common drift.

### Strategy 2: Scheduled review (weekly or bi-weekly)

Set a recurring task to review one documentation layer per cycle:

| Week | Review target |
|------|--------------|
| 1 | API surface + data model |
| 2 | Configuration + dependencies |
| 3 | Operations + deployment |
| 4 | Architecture + service map + AGENTS.md |

For each review:
1. Open the document
2. Scan for obviously stale information
3. Spot-check 2–3 claims against the code
4. Update `Last verified` date if everything checks out
5. Fix any issues found
6. Add new `[TODO]` markers for things you can't verify quickly

### Strategy 3: Agent-assisted audit

Use an AI agent to periodically scan for drift:

```
Prompt: "Compare docs/api-surface.md against the actual API routes defined
in app/api/. List any endpoints that exist in code but not in the docs,
or that are documented differently than implemented."
```

This is especially effective for:
- API surface vs actual routes
- Data model docs vs actual migrations
- Config docs vs actual .env.example
- AGENTS.md references vs actual file paths

### Strategy 4: Verification markers

Use `Last verified` dates as a passive freshness indicator:

```markdown
# API Surface

> Last verified: 2026-02-15
```

When a date is older than the document's freshness window, it's a signal that re-verification is needed. You can grep for stale dates:

```bash
# Find docs not verified in the last 30 days
grep -r "Last verified:" docs/ | while read line; do
  date=$(echo "$line" | grep -oP '\d{4}-\d{2}-\d{2}')
  if [[ "$date" < "$(date -d '30 days ago' +%Y-%m-%d)" ]]; then
    echo "STALE: $line"
  fi
done
```

## What to do when docs are wrong

When you find incorrect documentation:

1. **Fix it immediately** if the fix is small and obvious
2. **Add `[OUTDATED]` marker** if you don't have time to fix it now
3. **File a gap item** in the gap analysis if it needs investigation
4. **Never leave it unmarked** — a known lie is better than an unknown one

## Measuring documentation health

Track these metrics in your gap analysis:

| Metric | How to measure | Target |
|--------|---------------|--------|
| Coverage | % of modules with docs | > 90% |
| Freshness | % of docs within freshness window | > 80% |
| Open markers | Count of `[TODO]` + `[UNVERIFIED]` + `[OUTDATED]` | < 10 |
| Agent usability | Can an agent complete a task using only repo docs? | Yes |

## Minimum viable maintenance

If you do nothing else, do these two things:

1. **Update docs when you change code** (PR checklist)
2. **Re-verify `Last verified` dates monthly** (5 minutes per doc)

This catches 80% of documentation rot with minimal effort.
