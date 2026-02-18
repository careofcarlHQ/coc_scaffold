# 04 — Phased Testing Guide

> Build the safety net from the bottom up: first understand what exists, then protect the most critical paths, then expand outward.

---

## Stage 1: Test Infrastructure

Before writing any tests, make sure the testing infrastructure works.

### Checklist

- [ ] Test framework installed and configured (pytest + plugins)
- [ ] `pytest` runs successfully (even with 0 tests)
- [ ] Coverage tool works: `pytest --cov=app`
- [ ] Test database strategy decided and working
- [ ] Root `conftest.py` exists with basic fixtures
- [ ] Test directory structure created (unit / integration / characterization)
- [ ] `.env.test` or test configuration exists
- [ ] CI pipeline runs tests (or is ready to)

### Essential pytest configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "unit: Unit tests (fast, no IO)",
    "integration: Integration tests (database, API)",
    "characterization: Behavior-locking tests",
    "slow: Tests that take > 5 seconds",
]
```

### Verify with a smoke test

```python
# tests/test_smoke.py
def test_app_imports():
    """Verify the app module can be imported without errors."""
    import app  # noqa: F401

def test_true():
    """Canary test — if this fails, the testing infrastructure is broken."""
    assert True
```

**Gate**: `pytest` runs, reports results, exits cleanly. Coverage tool generates a report.

---

## Stage 2: Characterization Tests

Lock current behavior for the highest-priority modules from the risk map.

### The characterization test process

For each critical module:

1. **Read the code** — understand what it does (not what it should do)
2. **Identify the public interface** — what functions/methods are called from outside?
3. **Write tests for the happy path** — call the function with typical inputs, assert the actual output
4. **Write tests for edge cases** — empty inputs, None values, boundary conditions
5. **Write tests for error paths** — what happens when things go wrong?
6. **Document surprises** — if the code does something unexpected, note it in the test

### Characterization test pattern

```python
class TestBillingCalculateTotal:
    """Characterization: locks current behavior of calculate_total().
    
    WARNING: These tests document ACTUAL behavior, not necessarily
    CORRECT behavior. See notes on individual tests for known quirks.
    """
    
    def test_calculate_total_with_single_item(self):
        result = calculate_total([{"price": 100, "qty": 1}])
        assert result == 100  # Actual observed behavior
    
    def test_calculate_total_with_empty_list(self):
        # NOTE: Returns 0, but doesn't distinguish between
        # "no items" and "all items free" — potential bug?
        result = calculate_total([])
        assert result == 0
    
    def test_calculate_total_with_discount(self):
        result = calculate_total(
            [{"price": 100, "qty": 2}],
            discount=0.1
        )
        # NOTE: Discount applied AFTER quantity multiplication
        assert result == 180
```

### What to characterize first

Work through the risk map in order. For each module:

| Module | Public functions | Tests written | Surprises found |
|--------|-----------------|--------------|-----------------|
| {module} | {N} | {N} | {description} |

**Gate**: Top 5 critical modules have characterization tests. All pass. Surprises documented.

---

## Stage 3: Unit Tests for Business Logic

Now write proper unit tests for the business logic, informed by what you learned during characterization.

### Focus areas (in order)

1. **Calculations** — anything that computes values (pricing, totals, scores)
2. **Validation** — input validation, authorization checks, constraint enforcement
3. **Transformations** — data mapping, format conversion, serialization
4. **State transitions** — status changes, workflow progression
5. **Decision logic** — branching, filtering, selection

### Unit test pattern

```python
class TestCreateOrder:
    """Unit tests for order creation business logic."""
    
    def test_valid_order_returns_order_with_generated_id(self):
        ...
    
    def test_empty_cart_raises_validation_error(self):
        ...
    
    def test_out_of_stock_item_raises_stock_error(self):
        ...
    
    def test_discount_code_applied_to_total(self):
        ...
    
    def test_tax_calculated_based_on_shipping_address(self):
        ...
```

### Building fixtures

As you write unit tests, build a fixture library:

```python
# tests/unit/conftest.py

@pytest.fixture
def sample_product():
    return Product(id=1, name="Widget", price=Decimal("29.99"), stock=100)

@pytest.fixture
def sample_cart(sample_product):
    return Cart(items=[CartItem(product=sample_product, quantity=2)])

@pytest.fixture
def sample_user():
    return User(id=1, email="test@example.com", role="customer")
```

**Gate**: All business-critical functions have unit tests. Unit test suite runs in < 30 seconds. Coverage increased by at least 15 percentage points.

---

## Stage 4: Integration Tests

Test that components work together correctly along the critical paths.

### Critical path identification

List the flows that would break the product if they failed:

1. {e.g., User signup → email verification → first login}
2. {e.g., Product search → add to cart → checkout → payment}
3. {e.g., API data ingestion → processing → storage → retrieval}

### API endpoint tests

```python
class TestOrderAPI:
    """Integration tests for order endpoints."""
    
    def test_create_order_full_flow(self, client, auth_headers, sample_cart):
        response = client.post(
            "/api/orders",
            json=sample_cart.to_dict(),
            headers=auth_headers
        )
        assert response.status_code == 201
        order = response.json()
        assert "id" in order
        assert order["status"] == "pending"
    
    def test_create_order_unauthenticated_returns_401(self, client):
        response = client.post("/api/orders", json={})
        assert response.status_code == 401
```

### Database integration tests

```python
class TestOrderRepository:
    """Integration tests for order database operations."""
    
    def test_create_and_retrieve_order(self, db_session, sample_order):
        repo = OrderRepository(db_session)
        created = repo.create(sample_order)
        retrieved = repo.get_by_id(created.id)
        assert retrieved.total == sample_order.total
```

**Gate**: All critical paths have integration tests. Integration suite runs in < 3 minutes.

---

## Stage 5: CI Gates

Make the tests part of the workflow so coverage can never go backward.

### CI configuration

```yaml
# Example: GitHub Actions
test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Run tests
      run: pytest --cov=app --cov-fail-under={current_coverage}
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

### Coverage floor strategy

1. **Measure current coverage** after completing stages 2–4
2. **Set the floor at current coverage minus 1%** (allows minor fluctuations)
3. **Ratchet up** the floor every time coverage increases by 5+ percentage points
4. **Never lower** the floor

### Gate rules

| Rule | Enforcement |
|------|-------------|
| All tests pass | CI blocks merge on failure |
| Coverage ≥ floor | CI blocks merge on coverage drop |
| New code has tests | Code review requirement |
| No skipped tests without reason | Periodic audit |

**Gate**: CI pipeline running. Coverage floor set. Merges blocked on test failure.

---

## Stage completion checklist

| Stage | Status | Tests added | Coverage delta | Notes |
|-------|--------|------------|---------------|-------|
| 1. Infrastructure | {done/not} | {N} | — | |
| 2. Characterization | {done/not} | {N} | +{N}% | |
| 3. Unit tests | {done/not} | {N} | +{N}% | |
| 4. Integration tests | {done/not} | {N} | +{N}% | |
| 5. CI gates | {done/not} | — | — | Floor: {N}% |
| **Total** | | **{N}** | **{start}% → {end}%** | |
