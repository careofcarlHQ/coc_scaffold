# 08 — Progress and Quality

## Progress tracking

### Feature-level tracking

```markdown
## Feature: [Name]

- **Status**: scoping / analyzing / speccing / implementing / verifying / rolling out / done
- **Started**: [date]
- **Completed**: [date]
- **Spec**: feature/feature-spec.md
- **Impact**: feature/impact-analysis.md
```

### Stage-level tracking

```markdown
### Stage 1 — Database Layer
- Status: not-started / in-progress / done / blocked
- Started: [date]
- Completed: [date]
- Work:
  - Created migration 20260218_add_export_storage_key.py
- Tests added: 2
- Gate: ✅ migration up/down clean, existing tests pass
- Deviations: none

### Stage 2 — Service Layer
- Status: in-progress
- Work:
  - Implemented generate_download_url()
  - Implemented log_download_attempt()
- Tests added: 6
- Gate: pending
```

## Quality metrics

### Per-feature metrics

| Metric | Target | How to measure |
|--------|--------|---------------|
| Existing test regressions | 0 | Full test suite before/after |
| New test coverage | 100% of new code paths | Coverage report on changed files |
| Spec-to-implementation match | 100% of acceptance criteria | Checklist verification |
| Deviations from spec | Documented, all justified | Deviation log in checklist |
| Time estimate accuracy | Within 50% of estimate | Actual vs. estimated |

### Quality gates

Each stage must pass its gate before advancing. Gates are cumulative — every later stage includes all earlier gates.

```
Stage 1 gate: migration clean + existing tests pass
Stage 2 gate: + service tests pass + existing tests pass
Stage 3 gate: + endpoint tests pass + existing tests pass
Stage 4 gate: + UI renders + existing tests pass
Stage 5 gate: + job tests pass + existing tests pass
Stage 6 gate: + end-to-end flow works + all tests pass + acceptance criteria met
```

### Regression detection

After each stage, compare test results:

```markdown
## Regression Check — Stage N

- Existing tests before: 142 passed, 0 failed
- Existing tests after:  142 passed, 0 failed
- New tests added: 6
- Total tests after: 148 passed, 0 failed

Regression status: ✅ Clean
```

## Follow-up tracking

During implementation, capture ideas and issues for later:

```markdown
## Follow-up Items

| Item | Priority | Discovered during | Action |
|------|----------|-------------------|--------|
| Could add bulk download | P2 | Stage 3 | Separate feature |
| Error message could be more specific | P3 | Stage 2 | Polish pass |
| Consider caching signed URLs | P2 | Stage 3 | Performance feature |
```

Follow-up items become inputs for future feature additions or the next weekly review cycle.

## Definition of done

A feature is complete when:

- [ ] All acceptance criteria from the spec are met
- [ ] All stages pass their gates
- [ ] Zero regressions in existing tests
- [ ] Feature works end-to-end in the target environment
- [ ] Rollout plan is documented
- [ ] Follow-up items are captured
- [ ] Feature brief / temporary AGENTS.md section is cleaned up
- [ ] Any affected documentation is updated
