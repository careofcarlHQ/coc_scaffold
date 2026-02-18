# Regression Test Plan — PR merge blocked despite green CI

## Date: 2026-02-18
## Bug reference: `meta/self-application/gold-standard/executions/bug-investigation/run-001/root-cause-analysis.md`

---

## Primary Regression Test

### Purpose
Prevent branch-protection required context drift from blocking merges despite green CI.

### Test case
```python
def test_branch_protection_required_context_matches_ci_check():
    """Regression: merge blocked by required status context mismatch.

    Root cause: branch protection required context used a display label instead
    of real check-run context.
    Fix: enforce `validate-scaffolds` context in protection automation.
    """
    # Setup: configure branch protection with script defaults

    # Action: read branch protection required contexts and latest check-runs

    # Assert: required context includes validate-scaffolds and merge is allowed
```

### Verification
- [x] Failure mode reproduced before fix (merge returned 405 required check expected)
- [x] Flow succeeded after fix with green `validate-scaffolds`
- [x] Safety path validated (team mode restored after failures)
- [x] Check is independent of unrelated scaffold content

---

## Sibling Regression Tests

### Purpose
Prevent the same class of mismatch in other process automation paths.

| Test | Protects | Priority |
|------|----------|----------|
| `test_pr_template_uses_current_ci_context` | human operator checklist alignment | P1 |
| `test_solo_process_doc_uses_current_ci_context` | operator runbook alignment | P1 |

---

## Broader Prevention Tests

### Purpose
Strengthen coverage around operational safety and reproducibility.

| Test category | Description | Priority | Status |
|---------------|-------------|----------|--------|
| effectiveness runbook checks | require evidence that required context equals active check-run context | P0 | written (manual run evidence) |
| repeatability checks | run merge automation on multiple PRs and confirm stable behavior | P1 | written (observed across PR #3-#5) |

---

## Test Results

### Before fix
```
Merge rejected: Required status check "Scaffold Validation" is expected (405)
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
