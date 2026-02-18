# 03 — Reproduction and Isolation

## Purpose

Reproduction turns a vague bug report into a concrete, testable fact. Isolation narrows the search space from "somewhere in the codebase" to "this specific code path."

## Reproduction

### The reproduction protocol

1. **Start with the reported conditions**: Try to trigger the bug exactly as described
2. **If it reproduces**: Minimize — strip away unnecessary steps until you have the smallest trigger
3. **If it doesn't reproduce**: Investigate the gap — what's different about your environment?

### Minimal reproduction

A minimal reproduction has:
- The fewest possible steps
- The smallest possible data
- No unnecessary context
- A deterministic outcome (same input → same bug, every time)

```markdown
# ❌ Non-minimal
1. Log in as admin
2. Create a new project
3. Add 5 team members
4. Create an export
5. Wait for export to complete
6. Click download → 500 error

# ✅ Minimal
1. Create export with id=123 (or any export in "completed" state with NULL storage_key)
2. GET /api/v1/exports/123/download → 500 error

The bug is: completed exports with NULL storage_key hit an unguarded attribute access.
```

### When reproduction fails

If you can't reproduce the bug, investigate these factors:

| Factor | Check | Example |
|--------|-------|---------|
| **Data state** | Does the bug depend on specific data? | "Only exports created before Feb 15 have NULL storage_key" |
| **Environment** | Different versions, config, or state? | "Production has 3 workers; local has 1 — race condition?" |
| **Timing** | Is it time-dependent or order-dependent? | "Only fails when two requests arrive simultaneously" |
| **External state** | Does it depend on external service behavior? | "S3 returns 403 for expired credentials" |
| **Accumulated state** | Does it need many operations to trigger? | "Fails after 1000+ exports due to counter overflow" |

### Reproduction artifact

Document the reproduction as a test-like artifact:

```markdown
## Reproduction

### Prerequisites
- Database with at least one export in "completed" state where storage_key IS NULL

### Steps
1. GET /api/v1/exports/{id}/download where {id} is the export above
2. Observe: 500 Internal Server Error

### Expected
200 with download URL, or 409 if export is not downloadable

### Actual
500 with TypeError: 'NoneType' object has no attribute 'key'

### Environment
- Python 3.13, FastAPI 0.115, PostgreSQL 16
- Local dev environment
- Reproducible 100% of the time with the above prerequisites
```

---

## Isolation

### Purpose

Once you can reproduce the bug, narrow down exactly where in the code things go wrong.

### Binary search technique

The most efficient isolation technique: check the midpoint of the code path.

```
Request comes in → [auth] → [validation] → [service] → [storage] → [response]
                                                 ↑
                                     Is the bug before or after this point?
```

1. Add a log statement at the midpoint of the suspected code path
2. Trigger the bug
3. If the log shows correct data: bug is after this point
4. If the log shows incorrect data: bug is before this point
5. Repeat, halving the search space each time

### Isolation by layer

For web applications, isolate by stack layer:

```markdown
## Layer isolation

### Database layer
- Query: SELECT * FROM exports WHERE id = 123
- Result: storage_key IS NULL
- ❓ Is this correct? Should completed exports have a storage_key?

### Service layer
- Input: export_id = 123
- Observation: service calls export.storage_key without checking for NULL
- ✅ Bug is here: no NULL guard on storage_key

### API layer
- Input: GET /exports/123/download
- Observation: Passes export_id to service, gets TypeError back
- ❓ Should the API handle this case before calling the service?
```

### Isolation by data

Sometimes the bug only affects specific data:

```markdown
## Data isolation

| Export ID | State | storage_key | Bug triggers? |
|-----------|-------|-------------|---------------|
| 123 | completed | NULL | ✅ Yes |
| 124 | completed | "s3://..." | ❌ No |
| 125 | pending | NULL | ❌ No (different code path) |

Pattern: Bug triggers when state=completed AND storage_key IS NULL
```

### Isolation by time (git bisect)

If the bug is a regression (worked before, broken now):

```bash
# Find the commit that introduced the bug
git bisect start
git bisect bad          # Current commit has the bug
git bisect good v1.5.0  # This version was known-good
# Git checks out a midpoint commit
# Test for the bug, then tell git:
git bisect good  # or
git bisect bad
# Repeat until git finds the introducing commit
```

### Isolation output

After isolation, you should know:

```markdown
## Isolation Result

- **Exact location**: app/services/export.py, line 45
- **Code**: `url = export.storage_key.replace("s3://", "https://...")`
- **Problem**: export.storage_key is None for some completed exports
- **Condition**: Completed exports created before storage_key column was added
- **Data scope**: ~15 exports in production have this condition
```
