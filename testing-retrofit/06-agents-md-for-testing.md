# 06 — AGENTS.md for Testing

> How to orient an agent for test-writing work. Testing requires careful scoping — without guidance, agents will either write trivial tests or try to test everything at once.

---

## Why AGENTS.md matters for testing

Test work is deceptively unbounded. An agent told to "add tests" without constraints will either:
- Write 200 trivial assertion-free tests to inflate coverage numbers
- Try to test the entire codebase in one session and run out of context
- Write tests that depend on each other or on external services
- Mock so aggressively that tests pass regardless of code correctness

A well-written AGENTS.md focuses the agent on the *right* tests for the *current* stage.

---

## Testing brief structure

The testing AGENTS.md should include:

### 1. Current testing phase

Tell the agent exactly where you are in the retrofit:

```markdown
## Current phase
Phase 3 — Unit tests for business logic

## Previous phases completed
- Phase 1: Infrastructure ✓ (pytest configured, fixtures built)
- Phase 2: Characterization ✓ (22 tests locking critical behavior)
```

### 2. What to test now

Specific scope for this session:

```markdown
## This session's scope
Write unit tests for `app/services/billing.py`:
- `calculate_total()` — all input combinations
- `apply_discount()` — valid codes, expired codes, invalid codes
- `generate_invoice()` — happy path + missing data cases

Do NOT test:
- Database operations (that's integration phase)
- API endpoints (that's integration phase)
- Other service modules (not in scope yet)
```

### 3. Test patterns to follow

Reference the test pattern catalog:

```markdown
## Test patterns
Follow the patterns in `testing/test-pattern-catalog.md`.

Key rules:
- One assertion per test (roughly)
- Use fixtures from conftest.py, don't create data inline
- Name tests: test_{action}_{condition}_{expected_result}
- Mark with @pytest.mark.unit
- No database, no network, no filesystem in unit tests
```

### 4. Quality constraints

```markdown
## Quality constraints
- Every test must be independent (runs alone, runs in any order)
- Every test must be fast (< 100ms individually)
- No mocking of the function under test
- Mock only external boundaries (DB, API, filesystem)
- Tests must pass on clean run: `pytest tests/unit/ -v`
- Run the full suite after adding tests to check for conflicts
```

### 5. Verification

```markdown
## When done
1. Run: `pytest tests/unit/test_billing.py -v`
2. All tests pass
3. Run: `pytest --cov=app/services/billing.py` 
4. Coverage for this module ≥ 80%
5. Run: `pytest tests/ -v` (full suite, check for conflicts)
6. All tests still pass
```

---

## Anti-patterns in agent test work

Watch for these in the AGENTS.md constraints:

| Anti-pattern | Prevention rule |
|-------------|----------------|
| Empty assertions (`assert True`) | "Every test must assert a meaningful condition about the function's output or side effects" |
| Testing mocks instead of code | "Never assert on mock call counts unless testing dispatch logic" |
| One test doing everything | "Each test function should test exactly one behavior" |
| Copy-pasting test bodies | "Extract shared setup into fixtures" |
| Ignoring error paths | "Include at least one test for each documented exception" |
| Tests coupled to implementation | "Test the return value and side effects, not how the function computes them" |

---

## Session size guidance

For testing work, keep sessions focused:

| Session type | Scope | Expected output |
|-------------|-------|-----------------|
| **Characterization** | 1–2 modules | 5–15 tests per module |
| **Unit test** | 1 module | 10–30 tests |
| **Integration test** | 1 critical path | 5–10 tests |
| **Fixture building** | Cross-cutting | conftest.py + factories |

Don't try to test more than 2 modules per session. Context limits make it tempting to go wide — resist. Go deep on fewer modules.

---

## Template

See `templates/AGENTS.md.template` for a ready-to-fill testing orientation document.
