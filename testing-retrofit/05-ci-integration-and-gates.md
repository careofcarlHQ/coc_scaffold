# 05 — CI Integration and Gates

> Tests only work if they run automatically. CI gates turn tests from optional documentation into mandatory safety nets.

---

## CI Pipeline Design

### Minimum viable CI for testing retrofit

```
Push/PR → Install deps → Run tests → Report coverage → Block if failing
```

At minimum, your CI should:
1. Run the full test suite on every push and PR
2. Report pass/fail clearly
3. Block merges on failure
4. Report coverage numbers

### Test stage ordering

Run tests in order of speed and value:

```
Lint → Unit tests → Integration tests → Coverage report
 (seconds)  (seconds)    (minutes)         (seconds)
```

If unit tests fail, don't waste time on integration tests. Fail fast.

---

## Coverage Floor Strategy

### Setting the initial floor

After completing the characterization and unit test phases, your coverage will have increased from the baseline. Set the floor:

```
initial_floor = current_coverage - 1
```

The minus-1 buffer prevents CI from flapping on minor fluctuations (e.g., adding an untested utility function temporarily).

### Ratcheting up

Every time you complete a test phase or coverage increases significantly:

1. Check current coverage
2. If current > floor + 5, raise the floor to current - 1
3. Commit the updated floor to the CI config
4. Never lower the floor

### Example progression

| Date | Coverage | Floor | Event |
|------|----------|-------|-------|
| Jan 1 | 8% | — | Baseline (no gate) |
| Jan 15 | 22% | 21% | Gate activated after characterization |
| Feb 1 | 38% | 37% | After unit tests phase |
| Feb 15 | 45% | 44% | After integration tests |
| Mar 1 | 48% | 44% | Organic growth (not ratcheted yet) |
| Apr 1 | 52% | 51% | Ratcheted after 5+ point gain |

---

## CI Configuration Examples

### GitHub Actions

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -e ".[test]"
      
      - name: Run unit tests
        run: pytest tests/unit/ -v --tb=short
      
      - name: Run integration tests
        run: pytest tests/integration/ -v --tb=short
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test_db
      
      - name: Coverage report
        run: pytest --cov=app --cov-report=term --cov-fail-under=38
```

### Coverage reporting in PRs

Add coverage reporting so every PR shows the impact:

```yaml
      - name: Coverage comment
        uses: py-cov-action/python-coverage-comment-action@v3
        with:
          GITHUB_TOKEN: ${{ github.token }}
```

---

## Quality Gates

### Gate 1: Tests must pass

**Rule**: All tests must pass before merge.
**Enforcement**: CI required status check.
**Exception**: None. Fix the test or fix the code.

### Gate 2: Coverage floor

**Rule**: Total coverage must meet or exceed the floor.
**Enforcement**: `--cov-fail-under={floor}` flag.
**Exception**: Only raised, never lowered.

### Gate 3: New code has tests

**Rule**: New modules and significant logic changes must include tests.
**Enforcement**: Code review (human or agent).
**Guideline**: New files should have at least 50% coverage. New business logic should have at least 80%.

### Gate 4: No test rot

**Rule**: Skipped tests must have a documented reason and a ticket to re-enable.
**Enforcement**: Periodic audit (monthly).
**Metric**: Number of `@pytest.mark.skip` decorators should trend to zero.

---

## Test Result Monitoring

### What to track

| Metric | Where to find it | Frequency |
|--------|------------------|-----------|
| Total tests | CI output | Every build |
| Pass rate | CI output | Every build |
| Coverage % | Coverage report | Every build |
| Test duration | CI timing | Every build |
| Flaky test count | CI history | Weekly |
| Coverage by module | Coverage report | Weekly |

### Warning signs

| Signal | What it means | Action |
|--------|--------------|--------|
| Test suite getting slower | Too many integration tests or test data growing | Profile and optimize |
| Same test fails intermittently | Flaky test (timing, state, external dep) | Fix or quarantine immediately |
| Coverage dropping despite new code | New code isn't being tested | Enforce Gate 3 more strictly |
| Tests pass but bugs still ship | Tests are shallow or testing the wrong things | Review test quality, add integration tests |

---

## Flaky Test Protocol

Flaky tests are poison. They teach everyone to ignore test failures.

### When a test is flaky:

1. **Quarantine immediately** — move to a `tests/quarantine/` directory or mark with `@pytest.mark.flaky`
2. **Don't delete it** — the test is telling you something
3. **Fix within one week** — flaky tests that linger become permanent skips
4. **Root cause** — usually one of:
   - Timing dependency (async, sleep, timeout)
   - Shared state between tests (database, global variable)
   - External service dependency (API, network)
   - Order dependency (test assumes another test ran first)
5. **Add the fix to the pattern catalog** — so you don't repeat the mistake

---

## Maintenance checklist

Run this monthly:

- [ ] Coverage floor still set correctly: {N}%
- [ ] No skipped tests without documented reason
- [ ] No quarantined tests older than 2 weeks
- [ ] Test suite still runs in under {N} minutes
- [ ] CI is still blocking merges on failure
- [ ] Coverage report is still being generated
- [ ] No new modules added without tests
