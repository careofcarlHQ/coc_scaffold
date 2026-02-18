# 05 — Rollback and Safety

## Purpose

Every migration stage must be reversible. This document covers rollback planning, risk management, and safety protocols.

## Rollback plan requirements

### Every stage needs a rollback

No exceptions. Even "low-risk" stages need documented rollback steps.

```markdown
## Stage Rollback Plan

### Stage: {name}
### Risk: {low / medium / high}

### Rollback trigger
Execute rollback if ANY of these occur:
- Test suite failures that can't be explained
- Application won't start
- Data integrity check fails
- Error rate increases by > 2x baseline
- Performance degrades by > 50%

### Rollback steps
1. {Step 1 — specific command or action}
2. {Step 2}
3. {Step 3}

### Rollback verification
After rollback, confirm:
- [ ] Application starts and passes health check
- [ ] Test suite passes
- [ ] Data integrity check passes
- [ ] Error rates return to baseline

### Rollback time estimate
{minutes/hours}

### Data considerations
- Data created during this stage: {preserved / lost / needs cleanup}
- Data modified during this stage: {reversible / irreversible — backup exists}
```

## Rollback techniques by layer

### Code rollback
```bash
# Revert to previous version
git revert {commit}
# Or: redeploy previous known-good commit
git checkout {good-commit}
```

### Dependency rollback
```bash
# Revert version in manifest
git checkout HEAD~1 -- pyproject.toml poetry.lock
poetry install
```

### Database rollback
```bash
# Alembic downgrade
alembic downgrade -1

# Or: restore from backup
pg_restore -d dbname backup_YYYYMMDD.dump
```

### Infrastructure rollback
```
# Platform-specific: revert config, DNS, routing
# Keep old infrastructure running until cutover is confirmed
```

## Risk management

### Risk classification

| Risk level | Criteria | Required precautions |
|-----------|----------|---------------------|
| **Low** | No data changes, easy revert, no production impact | Document rollback steps |
| **Medium** | Configuration changes, dependency updates, minor schema changes | Backup + tested rollback |
| **High** | Data migration, platform move, major version upgrade | Full backup + tested rollback + monitoring plan + grace period |

### Risk mitigation strategies

| Strategy | When to use | Example |
|----------|------------|---------|
| **Feature flag** | Gradual rollout | `if settings.USE_NEW_DB:` |
| **Canary deployment** | Production verification | Deploy to 1 instance before all |
| **Blue-green** | Zero-downtime cutover | Run old and new simultaneously |
| **Shadow traffic** | Performance validation | Mirror requests to new system |
| **Backup checkpoint** | Data safety | Snapshot before each stage |

### Abort criteria

Define upfront when to abandon the migration entirely:

```markdown
## Abort Criteria

Abandon this migration and return to current state if:
1. More than 3 stages require unplanned rollback
2. Total timeline exceeds 2x the estimate
3. Data integrity issue discovered that affects production
4. Critical bug in target version with no workaround
5. Business priority change makes migration non-urgent
```

## Safety checklist per stage

Before applying any stage:
- [ ] Backup taken (if data-touching)
- [ ] Rollback steps documented
- [ ] Rollback tested (for medium/high risk stages)
- [ ] Monitoring in place
- [ ] Communication sent (if user-facing)
- [ ] Grace period defined (how long old system stays available)

After applying any stage:
- [ ] Verification checks pass
- [ ] Error rates normal
- [ ] Performance normal
- [ ] Rollback still possible
- [ ] Evidence captured

## Post-cutover safety

After the final cutover:
1. **Monitor intensely for 24 hours** — watch error rates, latency, error logs
2. **Keep old system on standby for 72 hours** — ready for emergency rollback
3. **Capture any migration-period anomalies** — data gaps, configuration drift
4. **Confirm with stakeholders** — everything working as expected?

Only decommission the old system after the grace period passes with no issues.
