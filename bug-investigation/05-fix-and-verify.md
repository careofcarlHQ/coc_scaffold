# 05 — Fix and Verify

## Purpose

Once you know the root cause, plan the fix before implementing it. A well-planned fix is small, targeted, and includes a regression guard.

## Fix planning

### Write a fix spec

Before touching code, write a brief fix specification:

```markdown
## Fix Spec

### Root cause
Migration 20260215_add_storage_key adds nullable column without backfilling existing rows.
Service function assumes storage_key is always non-NULL.

### The fix
1. Add a NULL check in export_download_service() before accessing storage_key
2. Return a clear error (409 Conflict) when storage_key is NULL for completed exports
3. Add a data migration to backfill storage_key for existing completed exports

### What changes
- app/services/export.py: Add NULL guard (3 lines changed)
- alembic/versions/20260218_backfill_storage_key.py: New data migration
- tests/test_export_download.py: New regression test

### What does NOT change
- API contract (new 409 response is additive)
- Existing migrations
- Other service functions

### Risk
- Low: NULL guard is a simple conditional
- Low: Data migration is UPDATE with WHERE clause, affects ~15 rows
- No backward compatibility concerns

### Regression test
Test: Create an export with state=completed and storage_key=NULL,
request download, expect 409 with descriptive error message.
```

### Fix categories

| Category | Approach | Example |
|----------|----------|---------|
| **Guard fix** | Add validation/null check | `if not export.storage_key: raise ...` |
| **Logic fix** | Correct wrong logic | `>=` should be `>` |
| **Data fix** | Repair bad data | Backfill missing values |
| **State fix** | Correct state machine | Add missing transition validation |
| **Config fix** | Correct configuration | Fix environment variable |
| **Dependency fix** | Update or pin dependency | `library==1.2.3` |

Most bugs need a guard fix (immediate protection) AND a deeper fix (prevent recurrence).

## Implementation

### Rule 1: Write the regression test FIRST

```python
# This test should FAIL before the fix and PASS after
def test_download_export_with_null_storage_key():
    """Regression test for bug: TypeError on exports with NULL storage_key.
    
    Root cause: exports created before 2026-02-15 have NULL storage_key.
    Fix: return 409 instead of crashing.
    """
    export = create_export(state="completed", storage_key=None)
    response = client.get(f"/api/v1/exports/{export.id}/download")
    assert response.status_code == 409
    assert "storage_key" in response.json()["detail"].lower()
```

### Rule 2: Apply the minimal fix

Change only what's necessary. Resist improvements.

```python
# ✅ Minimal fix
def get_download_url(export: Export) -> str:
    if not export.storage_key:
        raise HTTPException(
            status_code=409, 
            detail="Export does not have a downloadable file"
        )
    return generate_signed_url(export.storage_key)

# ❌ Over-engineering during a bug fix
def get_download_url(export: Export) -> str:
    # Refactored to use new StorageService with caching...
    # (This is feature work, not a bug fix)
```

### Rule 3: Run the full test suite

After applying the fix:
1. Run the new regression test → should PASS
2. Run the full existing test suite → should have zero new failures
3. Run the reproduction steps → bug should be gone

### Rule 4: Log other bugs found during investigation

```markdown
## Bugs discovered during investigation (NOT fixed in this PR)

1. **Similar NULL guard missing in export_list_service()** — storage_key 
   accessed without guard. Lower risk (list doesn't crash, returns None in JSON).
   Filed as: [link or description]

2. **No index on exports.state column** — queries filtering by state do 
   full table scan. Performance concern, not a bug. Filed for optimization.
```

## Verification

### Verification checklist

- [ ] Regression test fails BEFORE the fix (confirm it tests the right thing)
- [ ] Regression test passes AFTER the fix
- [ ] Original reproduction steps no longer trigger the bug
- [ ] Full existing test suite passes (zero new failures)
- [ ] Fix matches the fix spec (no scope creep)
- [ ] No unrelated changes included

### Verification evidence

Capture evidence for the record:

```markdown
## Fix Verification

### Bug: TypeError on export download for old exports
### Fix: NULL guard + data backfill
### Date: 2026-02-18

### Regression test
- Before fix: FAIL (TypeError as expected)
- After fix: PASS (409 with descriptive error)

### Reproduction
- Before fix: GET /exports/123/download → 500
- After fix: GET /exports/123/download → 409 "Export does not have a downloadable file"
- After backfill: GET /exports/123/download → 200 with download URL

### Test suite
- Before: 142 passed, 0 failed
- After: 143 passed, 0 failed (+1 regression test)

### Scope
- 15 exports in production affected by NULL storage_key
- Data migration will backfill all 15
```

## Deployment notes

### For bug fixes with data migrations

```markdown
## Deployment Order
1. Deploy code fix (NULL guard protects against crash)
2. Run data migration (backfill storage_key values)
3. Verify: zero exports with state=completed AND storage_key IS NULL
```

### For hotfixes (urgent production bugs)

```markdown
## Hotfix Deployment
1. Apply the guard fix (immediate crash protection)
2. Deploy to production (abbreviated review if critical)
3. Root cause fix → normal development flow
4. Verify in production
5. Post-mortem (if severity warrants it)
```
