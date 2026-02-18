# Regression Test Plan — PR merge blocked by branch divergence (`dirty`)

## Date: 2026-02-18
## Bug reference: `meta/self-application/gold-standard/executions/bug-investigation/run-002/root-cause-analysis.md`

---

## Primary Regression Test

### Purpose
Ensure non-mergeable dirty PR states are handled predictably and safely.

### Test case
```python
def test_dirty_pr_requires_conflict_resolution_before_merge():
    """Regression: dirty PR merge rejection.

    Root cause: branch conflict against main.
    Fix: resolve conflicts, rerun checks, rerun merge automation.
    """
    # Setup: prepare dirty PR head

    # Action: call merge automation

    # Assert: fails safely, restores protections, succeeds after conflict fix
```

### Verification
- [x] Dirty-state failure observed (`Pull Request is not mergeable`)
- [x] Team protection restored after failure
- [x] Merge succeeded after conflict resolution and green checks
- [x] Runbook remains deterministic and reproducible

---

## Sibling Regression Tests

### Purpose
Catch related lifecycle issues before merge attempt.

| Test | Protects | Priority |
|------|----------|----------|
| `test_update_branch_failure_reports_conflict` | explicit conflict visibility | P1 |
| `test_merge_script_finally_restores_team_mode` | safety contract on failures | P0 |

---

## Broader Prevention Tests

### Purpose
Improve reliability for future high-churn PRs.

| Test category | Description | Priority | Status |
|---------------|-------------|----------|--------|
| preflight mergeability checks | detect dirty state before mode toggle | P1 | proposed |
| conflict-heavy scenario runbook test | validate operator steps under branch churn | P1 | executed in run-002 |

---

## Test Results

### Before fix
```
Merge rejected: Pull Request is not mergeable (405)
```

### After fix
```
MERGED=True
MESSAGE=Pull Request successfully merged
```

### Full suite after fix
```
Ran 20 tests ... OK
```
