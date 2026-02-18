# Risk Priority Map — coc_scaffold (Self-Application)

## Date: 2026-02-18

---

## Scoring Method

Risk score is adapted for documentation scaffolds:

`Risk = impact_on_agent_execution × drift_probability × detectability_gap`

### Risk factor weights
| Factor | Weight |
|--------|--------|
| Broken navigation/links | 3x |
| Missing scaffold contract file | 3x |
| Ambiguous README operator flow | 2x |
| Template inconsistency | 2x |
| Naming/style drift | 1x |
| Historical/legacy variance | 1x |

---

## Priority 1 — Critical (test immediately)

| Module | Risk factors | Change freq | Current coverage | Score | Test type |
|--------|-------------|-------------|-----------------|-------|-----------|
| Root + scaffold markdown links | Broken navigation/links, high impact | High | Covered by `test_links.py` | 9 | Contract |
| Scaffold required file structure | Missing scaffold contract file | High | Covered by `test_structure.py` | 9 | Contract |
| Root README scaffold index consistency | Wrong entry point mapping | Medium | Covered by `test_cross_refs.py` | 8 | Contract |

## Priority 2 — High (test in next phase)

| Module | Risk factors | Change freq | Current coverage | Score | Test type |
|--------|-------------|-------------|-----------------|-------|-----------|
| Scaffold README operator sections | Ambiguous operator flow | High | Covered by `test_readme_contract.py` | 8 | Contract |
| Template extension and non-empty checks | Template inconsistency | Medium | Covered by `test_templates.py` | 7 | Contract |

## Priority 3 — Medium (test after high-priority)

| Module | Risk factors | Change freq | Current coverage | Score | Test type |
|--------|-------------|-------------|-----------------|-------|-----------|
| Heading and numbered guide conventions | Naming/style drift | Medium | Covered by `test_style.py` | 5 | Lint-style contract |

## Priority 4 — Low (test as time permits)

| Module | Risk factors | Change freq | Current coverage | Score | Test type |
|--------|-------------|-------------|-----------------|-------|-----------|
| Deep semantic equivalence between prompts/templates across scaffolds | Historical variance, lower immediate breakage | Medium | Not yet explicit | 4 | Comparative audit |

---

## Change Frequency Data

Current iteration touched:

| File category | Relative churn | Notes |
|---------------|---------------|-------|
| `README.md` files | High | Frequent alignment updates while adding new scaffolds |
| `tests/*.py` | High | Actively expanding self-validation coverage |
| `templates/*.template` | Medium | Stable but still maturing |

---

## Recommended Test Order

1. Link integrity and scaffold structure (already implemented)
2. README operator contract consistency (implemented)
3. Template consistency checks (implemented)
4. Coverage instrumentation and floor policy (next)
5. Comparative semantic audit of prompt/template parity (next)
