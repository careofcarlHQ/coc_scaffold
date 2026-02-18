# AGENTS.md — Testing Retrofit Self-Application (coc_scaffold)

## What we're testing
The scaffold framework itself: markdown structure, links, templates, and operator contract consistency.

## Current phase
Phase 5 — CI Gates (in progress)

## Read these files (in order)
1. `self-application/testing-retrofit/testing-checklist.md`
2. `self-application/testing-retrofit/coverage-baseline.md`
3. `self-application/testing-retrofit/risk-priority-map.md`
4. `self-application/testing-retrofit/coverage-report.md`
5. `tests/test_*.py`

## Scope for this session
- Expand and maintain scaffold contract validation rules
- Keep all tests green while tightening meaningful quality gates
- Update self-application artifacts after each significant process change

Do NOT do:
- Untracked framework edits (every change must map to checklist state)
- Cosmetic rewrites unrelated to a surfaced risk

## Test rules
- Keep tests deterministic and fast (< 1s target)
- Prefer rule-based contract checks for markdown repo invariants
- Fail with actionable messages tied to file paths
- Use strict local-link resolution outside fenced code blocks

## When done
1. Run: `python -m unittest discover -s tests -p "test_*.py" -v`
2. Update self-application artifacts with current state and next actions
3. Ensure root README links to self-application workspace
