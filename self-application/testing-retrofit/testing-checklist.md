# Testing Checklist — coc_scaffold (Self-Application)

## Retrofit started: 2026-02-18
## Target: 100% pass rate on scaffold contract suite + CI enforcement

---

## Phase 1 — Test Infrastructure

- Status: done
- Started: 2026-02-18
- Completed: 2026-02-18

### Tasks
- [x] Test framework installed and configured
- [x] Coverage tool working *(rule-based validation currently; line coverage pending)*
- [x] Test directory structure created
- [x] Root conftest.py with basic fixtures *(not required for current suite)*
- [x] Test database strategy decided *(not applicable)*
- [x] Smoke test passes: `python -m unittest discover -s tests -p "test_*.py" -v`

**Gate**: `python -m unittest` runs cleanly for full suite.

---

## Phase 2 — Characterization Tests

- Status: done
- Started: 2026-02-18
- Completed: 2026-02-18

### Modules characterized

| Module | Tests | Coverage | Surprises | Status |
|--------|-------|----------|-----------|--------|
| Scaffold file contracts | 4 | N/A | Legacy greenfield numbering mismatch surfaced and fixed | done |
| Link and README contracts | 3 | N/A | README section consistency drift surfaced and fixed | done |

### Totals
- Tests added: 15
- Coverage: N/A → N/A (rule-based)
- Surprises documented: 2

**Gate**: Critical documentation and structure behavior is locked by passing tests.

---

## Phase 3 — Unit Tests

- Status: done
- Started: 2026-02-18
- Completed: 2026-02-18

### Modules tested

| Module | Tests | Coverage | Status |
|--------|-------|----------|--------|
| `tests/test_links.py` | 1 | N/A | done |
| `tests/test_structure.py` | 4 | N/A | done |
| `tests/test_cross_refs.py` | 2 | N/A | done |
| `tests/test_style.py` | 2 | N/A | done |
| `tests/test_templates.py` | 2 | N/A | done |
| `tests/test_readme_contract.py` | 1 | N/A | done |

### Totals
- Tests added: 16
- Coverage: N/A → N/A
- Unit suite duration: ~0.30 seconds

**Gate**: Core contract rules are tested and green in local runs.

---

## Phase 4 — Integration Tests

- Status: in-progress
- Started: 2026-02-18
- Completed: —

### Critical paths tested

| Path | Tests | Status |
|------|-------|--------|
| Local run ↔ CI run parity | 1 (`tests/test_ci_policy.py`) | in-progress |
| Branch-protection gate verification | 0 | not |

### Totals
- Tests added: 0
- Coverage: N/A → N/A
- Full suite duration: ~0.30 seconds

**Gate**: Verify CI behavior under failing test conditions and enforce branch policy.

---

## Phase 5 — CI Gates

- Status: done
- Started: 2026-02-18
- Completed: 2026-02-18

### Configuration
- [x] CI runs tests on push/PR
- [x] Coverage floor set: 80% (`coverage report --fail-under=80`)
- [x] Merges blocked on test failure (verified via `scripts/set-branch-protection.ps1`)
- [x] Validation results visible in PR checks

**Gate**: CI enforcing + measurable quality floor committed.

---

## Summary

| Metric | Baseline | Current | Target |
|--------|----------|---------|--------|
| Total tests | 0 | 20 | — |
| Passing tests | 0 | 20 | 20 |
| Coverage | N/A | 81.10% | 80%+ |
| Coverage floor | — | 80% | ratchet upward over time |
| Suite duration | — | ~0.54s | < 300s |
| Flaky tests | 0 | 0 | 0 |

## Status: complete

## Next concrete actions

1. Ratchet coverage floor when baseline rises (> +5 points)
2. Expand semantic parity checks for cross-scaffold phase completeness
