# 08 — Progress and Quality

## Migration tracking

### Migration-level status

```markdown
## Migration: {Name}

- **Status**: planning / executing / cutover / cleanup / complete
- **Started**: {date}
- **Target completion**: {date}
- **Actual completion**: {date}
- **Stages**: {completed}/{total}
- **Rollbacks executed**: {count}
- **Deviations from plan**: {count}
```

### Stage-level tracking

```markdown
### Stage N — {Name}

- Status: not-started / in-progress / done / rolled-back / skipped
- Started: {date}
- Completed: {date}
- Changes:
  - {change 1}
  - {change 2}
- Verification:
  - Tests before: {N} passed, {F} failed
  - Tests after: {N} passed, {F} failed
  - Stage-specific checks: ✅ / ❌
- Rollback tested: yes / no
- Deviations: {none or description}
- Evidence: {links to logs, screenshots, etc.}
- **Gate**: {pass / fail}
```

## Quality gates

### Per-stage gates
- [ ] Changes applied as planned
- [ ] Test suite passes (zero new failures)
- [ ] Stage-specific verification passes
- [ ] Rollback verified
- [ ] Evidence captured

### Pre-cutover gates
- [ ] ALL stages complete with passing gates
- [ ] Full test suite passes on migrated state
- [ ] Performance is within acceptable range (< 20% regression from baseline)
- [ ] Rollback plan tested for critical stages
- [ ] Monitoring in place
- [ ] Old system on standby

### Post-cutover gates
- [ ] 24-hour monitoring: no error spikes
- [ ] Performance within acceptable range
- [ ] No data integrity issues
- [ ] All consumers working correctly

### Post-cleanup gates
- [ ] No references to old state remain
- [ ] All documentation updated
- [ ] Test suite passes
- [ ] Migration artifacts archived

## Metrics

### Migration health metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Stages completed on first attempt | > 80% | {N}% |
| Stages requiring rollback | < 20% | {N}% |
| Total timeline vs estimate | < 1.5x | {ratio} |
| Test regressions introduced | 0 | {N} |
| Post-cutover incidents | 0 | {N} |

### Comparison: before vs after

| Metric | Before migration | After migration | Acceptable? |
|--------|-----------------|-----------------|-------------|
| Test count | {N} | {N} | ✅ / ❌ |
| Test pass rate | {N}% | {N}% | ✅ / ❌ |
| Build time | {seconds} | {seconds} | ✅ / ❌ |
| Avg response time | {ms} | {ms} | ✅ / ❌ |
| P99 response time | {ms} | {ms} | ✅ / ❌ |
| Memory usage | {MB} | {MB} | ✅ / ❌ |

## Post-migration retrospective

```markdown
## Migration Retrospective — {Name}

### Summary
- Duration: {days/weeks}
- Stages: {N} total, {M} completed on first attempt, {K} required rollback
- Timeline: {planned} vs {actual}

### What went well
- {Item 1}
- {Item 2}

### What could improve
- {Item 1}
- {Item 2}

### Surprises
- {Unexpected issue 1 and how it was resolved}

### Lessons for next migration
- {Lesson 1}
- {Lesson 2}
```
