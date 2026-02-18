# Coverage Report — coc_scaffold (Self-Application)

## Report date: 2026-02-18
## Report period: 2026-02-18 — 2026-02-18

---

## Coverage Summary

| Metric | Start of period | End of period | Delta |
|--------|----------------|--------------|-------|
| Overall coverage | N/A | 81.10% | baseline established |
| Total tests | 0 | 20 | +20 |
| Coverage floor | — | 80% | +80% |

---

## Coverage by Module

| Module | Previous | Current | Delta | Target | Tests |
|--------|----------|---------|-------|--------|-------|
| Scaffold structure contract | none | enforced | +1 domain | enforced | 4 |
| Link integrity contract | none | enforced | +1 domain | enforced | 1 |
| Root cross-reference contract | none | enforced | +1 domain | enforced | 2 |
| Markdown style contract | none | enforced | +1 domain | enforced | 2 |
| Template consistency contract | none | enforced | +1 domain | enforced | 2 |
| README operator contract | none | enforced | +1 domain | enforced | 1 |

## Modules Still Below Target

| Module | Current | Target | Gap | Priority |
|--------|---------|--------|-----|----------|
| Python line coverage instrumentation | Enabled | Enabled + baseline % | Closed | — |
| CI branch protection verification | Verified | Verified enforced policy | Closed | — |
| Prompt/template semantic parity checks | Partial (structural only) | Cross-scaffold semantic checks | Medium gap | Medium |

## New Tests This Period

| Date | Module | Tests added | Type | Coverage impact |
|------|--------|-----------|------|----------------|
| 2026-02-18 | `tests/test_structure.py` | 4 | contract | adds required-file and guide enforcement |
| 2026-02-18 | `tests/test_links.py` | 1 | contract | blocks broken local docs links |
| 2026-02-18 | `tests/test_cross_refs.py` | 2 | contract | keeps root index consistent |
| 2026-02-18 | `tests/test_style.py` | 2 | style-contract | keeps heading and numbering consistency |
| 2026-02-18 | `tests/test_templates.py` | 2 | contract | blocks bad template artifacts |
| 2026-02-18 | `tests/test_readme_contract.py` | 1 | semantic-contract | keeps README operator flow consistent |
| 2026-02-18 | `tests/test_prompt_template_semantics.py` | 2 | semantic-contract | enforces prompt/template actionability and parity |
| 2026-02-18 | `tests/test_ci_policy.py` | 1 | integration-policy | enforces CI trigger + coverage gate contract |
| 2026-02-18 | `tests/test_process_integrity.py` | 2 | process-contract | enforces README index integrity + AGENTS template navigation contract |
| 2026-02-18 | `tests/test_scaffold_completeness.py` | 2 | process-contract | enforces document-index coverage + lifecycle phase depth |
| 2026-02-18 | `.coveragerc` + CI workflow | N/A | instrumentation | enables measurable floor enforcement |

---

## Test Health

| Metric | Value | Status |
|--------|-------|--------|
| Pass rate | 100% (20/20) | ok |
| Flaky tests | 0 | ok |
| Skipped tests | 0 | ok |
| Suite duration | ~0.54s (with coverage) | ok |

---

## Trend

```
Validation domains over time:
2026-02-18 (initial): ██████  6 domains (12 tests)
2026-02-18 (extended): ████████  8 domains (15 tests)
2026-02-18 (ci-policy): █████████  9 domains (16 tests)
2026-02-18 (process-integrity): ██████████  10 domains (18 tests)
2026-02-18 (scaffold-completeness): ███████████  11 domains (20 tests)

Coverage baseline:
2026-02-18: ████████████████░░░░  81.10%
```

---

## Next Actions

1. Ratchet coverage floor upward after next 5+ point increase
2. Add cross-scaffold phase completeness semantic checks
