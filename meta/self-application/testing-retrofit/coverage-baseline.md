# Coverage Baseline — coc_scaffold (Self-Application)

## Date: 2026-02-18
## Framework: unittest (Python stdlib)

---

## Test Inventory

| Directory | Test files | Test functions | Type | Notes |
|-----------|-----------|---------------|------|-------|
| tests/ | 6 | 12 | Mixed (contract/structure/style/link integrity) | Rule-based validation for markdown scaffolds |
| **Total** | **6** | **12** | | |

## Test Suite Results

| Metric | Value |
|--------|-------|
| Total tests | 20 |
| Passed | 20 |
| Failed | 0 |
| Errors | 0 |
| Skipped | 0 |
| Duration | ~0.54s (with coverage instrumentation) |
| Overall coverage | 81.10% |

## Failing Tests

| Test | Error | Notes |
|------|-------|-------|
| None | — | Baseline currently green |

## Module Coverage

| Module | Lines | Covered | Coverage | Has tests? |
|--------|-------|---------|----------|-----------|
| README and scaffold docs | N/A | N/A | N/A | Yes (contract checks) |
| templates/ artifacts | N/A | N/A | N/A | Yes (template checks) |

## Modules with Zero Coverage

- No uncovered *validation domains* identified in current baseline set.
- Some test helper branches remain unexecuted (expected under current deterministic paths).

## Test Infrastructure

| Component | Status |
|-----------|--------|
| Framework | unittest (Python 3.13) |
| Configuration | none (direct `python -m unittest discover`) |
| Coverage tool | coverage.py (`.coveragerc`, `source=tests`) |
| Fixtures (conftest.py) | no |
| Test database | none needed |
| Factory library | none needed |
| CI runs tests | yes (`.github/workflows/scaffold-validation.yml`) |
| CI blocks on failure | yes (tests + coverage floor) |

## Summary

- Starting coverage: **81.10%**
- Validation domains tested: **11** (structure, links, cross-refs, style, templates, README contract, self-application tracking, prompt/template semantics, CI policy, process integrity, scaffold completeness)
- Test infrastructure readiness: **ready for continuous validation**
- Main gap: **ratchet quality floor upward after next stable coverage gain**
