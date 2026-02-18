# 08 — Post-Fix Quality

## Purpose

A bug fix isn't done when the symptom disappears. Quality ensures the fix is permanent, traceable, and contributes to systemic improvement.

## Regression guard requirements

Every bug fix MUST produce a regression test that:

1. **Reproduces the exact trigger**: Same inputs/conditions that caused the bug
2. **Fails without the fix**: Confirms the test actually tests the bug
3. **Passes with the fix**: Confirms the fix works
4. **Is specific**: Unrelated changes shouldn't affect it
5. **Has a descriptive name and docstring**: Future readers should understand what bug it guards against

```python
def test_export_download_null_storage_key():
    """Regression: completed exports with NULL storage_key caused TypeError.
    
    Root cause: Migration 20260215 added storage_key column but didn't
    backfill existing rows. Service assumed non-NULL.
    Fix: Return 409 when storage_key is NULL.
    See: bugfix/root-cause-analysis-export-download.md
    """
    export = create_export(state="completed", storage_key=None)
    response = client.get(f"/api/v1/exports/{export.id}/download")
    assert response.status_code == 409
```

## Post-fix review checklist

- [ ] Regression test exists and is descriptive
- [ ] Regression test fails without the fix (verified)
- [ ] Regression test passes with the fix
- [ ] Full test suite passes (zero new failures)
- [ ] Fix matches the fix spec (no scope creep)
- [ ] Root cause is documented
- [ ] Sibling bugs checked (same pattern elsewhere)
- [ ] Prevention items logged

## Prevention backlog

After every bug fix, add at least one prevention item:

```markdown
## Prevention Items from [Bug Title]

| Item | Type | Effort | Impact | Status |
|------|------|--------|--------|--------|
| Add NOT NULL constraint to storage_key for completed exports | Data fix | Small | Prevents this exact bug | To do |
| Add linter rule: no unguarded attribute access on Optional fields | Tooling | Medium | Prevents class of bugs | Backlog |
| Add characterization tests for all export state transitions | Testing | Medium | Broader coverage | Backlog |
```

Prevention items feed into:
- [testing-retrofit scaffold](../testing-retrofit/) — for adding test coverage
- [refactoring scaffold](../refactoring/) — for structural improvements
- Sprint/weekly planning — for prioritization

## Bug metrics

Track over time to identify systemic issues:

### Per-bug metrics
| Metric | Value |
|--------|-------|
| Time to reproduce | {minutes} |
| Time to diagnose | {minutes} |
| Time to fix | {minutes} |
| Total time | {minutes} |
| Hypotheses tested | {count} |
| Dead ends | {count} |
| Sibling bugs found | {count} |
| Prevention items | {count} |

### Aggregate patterns (monthly review)
| Pattern | Count | Trend |
|---------|-------|-------|
| Null/undefined access | {N} | ↑ ↓ → |
| Race condition | {N} | ↑ ↓ → |
| State violation | {N} | ↑ ↓ → |
| Missing validation | {N} | ↑ ↓ → |
| Configuration error | {N} | ↑ ↓ → |
| External service | {N} | ↑ ↓ → |

If a pattern is trending up, invest in prevention (linter rules, type annotations, test patterns).

## Bug investigation retrospective

For medium+ severity bugs, brief retrospective:

```markdown
## Retrospective — [Bug Title]

### What went well
- {Investigation was fast because hypothesis log kept focus}
- {Regression test was easy to write because reproduction was clear}

### What could improve
- {Should have checked data state earlier — spent time on wrong hypothesis}
- {No existing test for this code path — testing-retrofit candidate}

### Systemic learnings
- {Migrations should always include data backfill for NOT NULL semantics}
- {Services should use type annotations for Optional fields}
```
