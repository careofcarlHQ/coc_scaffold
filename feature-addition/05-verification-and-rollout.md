# 05 — Verification and Rollout

## Purpose

A feature isn't done when the code works locally. Verification confirms correctness and compatibility. Rollout confirms safe production deployment.

## Verification checklist

### Regression verification

- [ ] Full existing test suite passes with zero new failures
- [ ] No existing test was modified to accommodate the feature (unless spec required it)
- [ ] Test count has increased (new tests were added, none removed)

### Feature verification

- [ ] All acceptance criteria from the feature spec are met
- [ ] Happy path works end-to-end
- [ ] Error paths return expected responses
- [ ] Edge cases from the spec are covered by tests

### Backward compatibility

- [ ] **API compatibility**: Existing endpoints return the same response shape
  - New fields may be added (additive change is OK)
  - No existing fields removed or renamed
  - No existing status codes changed
- [ ] **Data compatibility**: Existing database queries work unchanged
  - New nullable columns don't break existing reads
  - Existing foreign keys are preserved
- [ ] **UI compatibility**: Existing pages render correctly
  - No layout breaks from new navigation items
  - No broken links from route changes
- [ ] **Configuration compatibility**: Existing environment works without new required env vars
  - New env vars have defaults or are optional
  - Existing config files don't need manual changes

### Migration safety

- [ ] Migration runs forward (up) without error
- [ ] Migration runs backward (down) without error
- [ ] Migration preserves existing data
- [ ] Migration doesn't require downtime (for production systems)
  - No table locks on large tables
  - No data backfills that take > 30 seconds
  - If downtime is required, it's documented in the rollout plan

---

## Rollout strategy

### Pre-deployment

1. **Document the rollout plan**: What happens, in what order, with what checks
2. **Identify rollback trigger**: What condition means you roll back?
3. **Prepare rollback steps**: How to undo (migration down, feature flag off, revert deploy)
4. **Verify staging/preview** (if available): Deploy to non-production first

### Deployment order

```
1. Database migration (if any)
   └── Verify: tables/columns exist, no errors
2. Backend deployment
   └── Verify: health check passes, existing endpoints work
3. Frontend deployment (if applicable)
   └── Verify: app loads, existing flows work
4. Feature verification
   └── Verify: new feature works in production
5. Monitor
   └── Watch error logs/metrics for 24 hours
```

### Feature flags

For medium-to-large features, consider a feature flag:

```python
# Simple feature flag pattern
if settings.FEATURE_EXPORTS_DOWNLOAD:
    router.include_router(download_router)
```

Benefits:
- Deploy code without exposing the feature
- Enable for testing in production before full rollout
- Instant disable if problems emerge
- No code revert needed

When to use:
- Feature affects existing user flows
- Feature has external dependencies (third-party APIs)
- Feature involves data migration that might need monitoring
- You want to separate "deploy" from "release"

### Post-deployment verification

- [ ] Health check endpoint returns OK
- [ ] Existing API endpoints return expected responses
- [ ] New feature endpoint works with production data
- [ ] No error spikes in logs
- [ ] No performance degradation
- [ ] Migration completed successfully (check DB state)

### Rollback plan

Every feature deployment must have a documented rollback:

```markdown
## Rollback Plan

### Trigger
Roll back if any of these occur within 24 hours:
- Error rate increases by > 2x baseline
- New endpoint returns 500 errors
- Existing endpoints affected
- Data integrity concerns

### Steps
1. Revert backend deployment to previous version
2. Run migration down: `alembic downgrade -1`
3. Verify existing functionality restored
4. Disable feature flag (if used)

### Data considerations
- New rows created in [table] will be orphaned — acceptable / needs cleanup
- No irreversible data changes in this feature
```

---

## Verification evidence template

After verification, capture evidence:

```markdown
## Feature Verification Evidence

### Feature: [name]
### Date: [date]
### Verified by: [human/agent]

### Test results
- Existing tests: X passed, 0 failed, 0 skipped
- New tests: Y passed, 0 failed
- Total test count change: +Y

### Compatibility
- API backward compatibility: ✅ confirmed
- Data backward compatibility: ✅ confirmed
- UI backward compatibility: ✅ confirmed / N/A
- Config backward compatibility: ✅ confirmed

### Acceptance criteria
- [ ] Criterion 1: ✅ met
- [ ] Criterion 2: ✅ met
- [ ] Criterion N: ✅ met

### Migration
- Up migration: ✅ clean
- Down migration: ✅ clean
- Data preservation: ✅ verified

### Deployment
- Deployed to: production / staging
- Rollback plan: documented in [link]
- Feature flag: enabled / N/A
```
