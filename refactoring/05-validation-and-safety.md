# 05 — Validation and Safety

## Core principle: prove it, don't promise it

Every refactoring change must produce evidence that behavior is preserved. "I didn't change any logic" is not evidence — passing tests are evidence.

## The validation pyramid for refactoring

```
                    ┌──────────────┐
                    │   Smoke Test │  ← Key user flows still work
                    ├──────────────┤
                    │  Integration │  ← Cross-module interactions preserved
                    ├──────────────┤
                    │     Unit     │  ← Individual functions behave the same
                    ├──────────────┤
                    │    Static    │  ← Types, lint, complexity checks pass
                    └──────────────┘
```

Every refactoring PR should pass all four levels.

## Pre-refactoring validation

Before touching any code, establish the safety baseline:

### 1. Record the green baseline

```bash
# Run full test suite and save output
pytest --tb=short > refactor/baseline-test-output.txt 2>&1
echo "Exit code: $?" >> refactor/baseline-test-output.txt

# Record coverage
pytest --cov=app --cov-report=term > refactor/baseline-coverage.txt 2>&1

# Record lint
ruff check app/ > refactor/baseline-lint.txt 2>&1

# Record type check
mypy app/ > refactor/baseline-typecheck.txt 2>&1
```

### 2. Verify baseline stability

Run `./refactor/verify-baseline.ps1 -Stability` which executes tests 3 times automatically. If any test fails intermittently, fix it before starting refactoring. Flaky tests make it impossible to distinguish refactoring regressions from pre-existing noise.

> The verify-baseline script (from `templates/verify-baseline.ps1.template`) is your single-command stability check. Bake flaky-test detection into automation instead of relying on agents to remember to run tests multiple times.

### 3. Identify high-risk areas

For each refactoring target, assess:

| Factor | Question | Risk level |
|--------|----------|-----------|
| Test coverage | Is the area above 80%? | Low: >80%, Medium: 50-80%, High: <50% |
| Callers | How many callers exist? | Low: <5, Medium: 5-15, High: >15 |
| Side effects | Does it write to DB, call APIs, send emails? | Low: pure logic, Medium: DB only, High: external effects |
| Complexity | Cyclomatic complexity? | Low: <10, Medium: 10-20, High: >20 |
| Concurrency | Is it called from async/threaded contexts? | Low: sync only, Medium: async, High: shared state |

For high-risk areas, add extra validation steps:
- Compare I/O pairs before and after refactoring
- Run against production-like data
- Have a human review the specific behavioral claims

## During-refactoring validation

### After every atomic change

An **atomic change** is the smallest edit that can be independently verified: one function move, one caller redirect, one import update. Run tests after each.

```bash
# Minimum validation (run after every atomic change)
pytest -x              # Stop on first failure
ruff check app/        # Lint
mypy app/              # Type check
```

### After every PR

```bash
# Full validation (run before merging any refactoring PR)
pytest --tb=short                              # All tests
pytest --cov=app --cov-report=term             # Coverage (must not decrease)
ruff check app/                                 # Lint
mypy app/                                       # Type check
radon cc app/ -a -nc                           # Complexity (should improve)
```

### Comparison report template

```markdown
### Validation Report: {PR title}

| Metric | Before | After | Status |
|--------|--------|-------|--------|
| Tests passing | ___ / ___ | ___ / ___ | ✅ / ❌ |
| Test coverage | ___% | ___% | ✅ / ❌ |
| Lint errors | ___ | ___ | ✅ / ❌ |
| Type errors | ___ | ___ | ✅ / ❌ |
| Avg complexity | ___ | ___ | ✅ / ❌ |
| Max file length | ___ | ___ | ✅ / ❌ |

Behavior preservation evidence:
- [ ] All characterization tests pass
- [ ] No new test failures
- [ ] Coverage did not decrease
- [ ] Key user flows verified
```

## Rollback strategy

### When to rollback

Rollback immediately if:
- Tests fail and the cause isn't obvious within 30 minutes
- Coverage decreased by more than 2%
- A behavior change is detected that wasn't intentional
- The refactoring is taking 3x longer than estimated

### How to rollback

The beauty of small, incremental refactoring: rollback is just a git revert.

```bash
# Revert the last refactoring commit
git revert HEAD

# Or revert an entire PR
git revert -m 1 <merge-commit-sha>

# Verify tests pass after revert
pytest --tb=short
```

### Post-rollback process

1. Log why the rollback happened
2. Analyze: was the migration map wrong? Were tests insufficient?
3. Update the refactoring plan to address the root cause
4. Re-attempt only after the root cause is fixed

## Characterization testing strategies

### Strategy 1: Capture I/O pairs

For pure functions, record what goes in and what comes out:

```python
# Before refactoring, capture behavior
def test_capture_price_calculation():
    """Characterization test: captures current behavior of calculate_price."""
    test_cases = [
        ({"items": [{"price": 10, "qty": 2}], "discount": 0}, 20.0),
        ({"items": [{"price": 10, "qty": 2}], "discount": 10}, 18.0),
        ({"items": [], "discount": 0}, 0.0),
    ]
    for input_data, expected in test_cases:
        result = calculate_price(**input_data)
        assert result == expected, f"Input: {input_data}, Expected: {expected}, Got: {result}"
```

### Strategy 2: Snapshot testing

For complex outputs, snapshot the entire response:

```python
def test_snapshot_order_response(snapshot):
    """Characterization test: snapshot of create_order response shape."""
    response = client.post("/api/v1/orders", json=valid_order)
    snapshot.assert_match(response.json())
```

### Strategy 3: Contract testing

For cross-module boundaries being restructured:

```python
def test_order_service_contract():
    """The order service must accept this input shape and return this output shape."""
    result = order_service.create(
        customer_id="cust-123",
        items=[{"sku": "ABC", "qty": 1}],
    )
    assert "order_id" in result
    assert result["status"] == "pending"
    assert isinstance(result["total"], float)
```

### Strategy 4: Side-effect verification

For functions with side effects, verify the effects:

```python
def test_order_creation_side_effects(db_session):
    """Characterization: creating an order writes to orders AND audit_log tables."""
    order_service.create(customer_id="cust-123", items=[...])

    # Verify primary effect
    orders = db_session.query(Order).filter_by(customer_id="cust-123").all()
    assert len(orders) == 1

    # Verify side effect
    audit_entries = db_session.query(AuditLog).filter_by(entity_type="order").all()
    assert len(audit_entries) == 1
```

## Safety checklist for refactoring PRs

Before approving any refactoring PR:

- [ ] PR applies exactly one named refactoring pattern
- [ ] PR does not change behavior (no feature additions, no bug fixes)
- [ ] All tests pass (zero new failures)
- [ ] Coverage did not decrease
- [ ] No new lint or type errors
- [ ] Migration map entry is satisfied
- [ ] Rollback is possible via simple revert
- [ ] Any bugs discovered are logged, not fixed in this PR
- [ ] If old code is deleted: zero-callers verification completed (grep for imports in source, tests, scripts, config, CI)
