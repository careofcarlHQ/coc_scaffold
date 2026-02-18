# 04 — Phased Migration Guide

## The migration stage pattern

Each stage follows the same execution cycle:

```
Announce → Backup → Apply → Verify → Rollback-Test → Record → Advance
```

### 1. Announce
Update the migration checklist. Note what you're about to change and why.

### 2. Backup
If the stage touches data or infrastructure, take a snapshot/backup first.

### 3. Apply
Make the changes defined in the migration plan for this stage.

### 4. Verify
Run the stage-specific verification (tests, smoke tests, manual checks).

### 5. Rollback-test
For high-risk stages, actually execute and verify the rollback. Then re-apply.

### 6. Record
Capture evidence: what changed, verification results, any deviations.

### 7. Advance
Mark the stage complete and move to the next one.

---

## Stage execution rules

### Rule 1: One stage at a time
Never run two stages in parallel (even if they're independent). Serial execution makes failures attributable.

### Rule 2: Green before advancing
The test suite must pass before moving to the next stage. If a test fails:
- Is it a real regression? → Fix before advancing.
- Is it a test that needs updating for the new state? → Update the test, document why.

### Rule 3: Rollback before commitment
Before marking a stage as "done," confirm the rollback works. You may not need it, but you must be able to if you do.

### Rule 4: No scope creep
The stage does exactly what the migration plan says. If you discover something else that needs changing, add it to the plan as a new stage — don't expand the current one.

---

## Stage types

### Type: Dependency update

```markdown
### Stage N — Update {dependency} from {old} to {new}

1. Update version in pyproject.toml / package.json / requirements.txt
2. Run install: `poetry install` / `pip install -r requirements.txt`
3. Fix any import/API errors
4. Run test suite
5. Fix any test failures caused by the update
6. Verify: all tests pass, application starts

Rollback: Revert version in manifest, reinstall.
```

### Type: Database migration

```markdown
### Stage N — {Schema change description}

1. Take database backup: `pg_dump -Fc dbname > backup_YYYYMMDD.dump`
2. Test migration on copy: `alembic upgrade head` (test DB)
3. Verify data integrity on copy
4. Apply to production: `alembic upgrade head`
5. Verify data integrity on production
6. Test application against new schema

Rollback: `alembic downgrade -1` or restore from backup.
```

### Type: Infrastructure change

```markdown
### Stage N — {Infrastructure change description}

1. Document current infrastructure state
2. Apply change (platform config, DNS, etc.)
3. Wait for propagation (DNS: up to 24h; platform: minutes)
4. Verify: health check, endpoint test, data access
5. Monitor error rates for 1 hour

Rollback: Revert infrastructure change. Keep old infrastructure running.
```

### Type: Code adaptation

```markdown
### Stage N — {Code adaptation description}

1. Apply code changes across affected files
2. Maintain backward compatibility (support both old and new)
3. Run test suite
4. Deploy
5. Verify in deployed environment

Rollback: Revert code changes, redeploy.
```

---

## Handling migration-period data

During migration, data may be written to both old and new systems. Plan for this:

### Option 1: Write to both
```
Application → Write to old DB → Sync to new DB
                              → Or: Write to both simultaneously
```

### Option 2: Write to new, read from both
```
Application → Write to new DB
           → Read from new DB (primary)
           → Fallback read from old DB (if missing)
```

### Option 3: Stop writes during cutover
```
Application → Read-only mode (brief)
           → Migrate remaining data
           → Switch to new DB
           → Resume writes
```

Choose based on your downtime tolerance and data volume.

---

## Common pitfalls

| Pitfall | Consequence | Prevention |
|---------|-------------|------------|
| No backup before data migration | Data loss on failure | Mandatory backup step |
| Testing against copy, deploying to production | Production-specific issues missed | Stage-specific production checks |
| Migrating too many things per stage | Can't isolate failures | One layer per stage |
| Forgetting about data created during migration | Data loss or inconsistency | Migration-period data strategy |
| Not testing rollback | Rollback fails when needed | Mandatory rollback verification |
| Removing old system too early | Can't recover from late-discovered issues | 72-hour grace period |
