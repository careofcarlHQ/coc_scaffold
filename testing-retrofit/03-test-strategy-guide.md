# 03 — Test Strategy Guide

> Choosing *what* to test and *how* is the most important decision in a testing retrofit. This guide helps you make those decisions systematically.

---

## The Risk Priority Matrix

Not all code deserves the same test investment. Prioritize by crossing two axes:

```
                    HIGH CHANGE FREQUENCY
                    │
        ┌───────────┼───────────┐
        │ Monitor   │ Test      │
        │ closely   │ FIRST     │
        │           │           │
LOW ────┼───────────┼───────────┼──── HIGH
RISK    │           │           │    RISK
        │ Test      │ Test      │
        │ last      │ second    │
        │           │           │
        └───────────┼───────────┘
                    │
                    LOW CHANGE FREQUENCY
```

### Risk factors (score 1–5 for each)

| Factor | Description | Weight |
|--------|------------|--------|
| **Data integrity** | Touches persistent data, financial calculations, user records | 3x |
| **Authentication/authorization** | Guards access, handles credentials | 3x |
| **External integrations** | Calls third-party APIs, webhooks | 2x |
| **User-facing critical path** | Part of the main user journey | 2x |
| **Complex logic** | Multiple branches, state machines, calculations | 1x |
| **Error handling** | Failure modes, retry logic, fallbacks | 1x |

### Change frequency

```bash
# Most-changed files in the last 6 months
git log --since="6 months ago" --name-only --pretty=format: | \
  sort | uniq -c | sort -rn | head -30

# Files with the most authors (complexity proxy)
git log --since="6 months ago" --name-only --pretty=format:%ae | \
  sort | uniq -c | sort -rn | head -30
```

### Bug frequency

```bash
# Files mentioned in bug fix commits (if you tag commits)
git log --all --oneline --grep="fix" --name-only --pretty=format: | \
  sort | uniq -c | sort -rn | head -20
```

---

## Test type selection

Different code needs different test types. Here's a decision guide:

### When to use characterization tests
- Code with unclear or undocumented behavior
- Code you're about to refactor
- Code with complex side effects
- Legacy code where the "spec" is the code itself

### When to use unit tests
- Pure functions with clear inputs and outputs
- Business logic calculations
- Validation rules
- Data transformation functions
- Utility functions with edge cases

### When to use integration tests
- API endpoints (request → response)
- Database operations (query → result)
- Service layer functions that coordinate multiple components
- Background job execution
- Authentication/authorization flows

### When to use end-to-end tests (sparingly)
- Critical user flows where integration tests aren't sufficient
- Flows that cross system boundaries
- Only after unit and integration coverage is solid

---

## Test architecture for the codebase

Before writing tests, establish the testing architecture.

### Directory structure
```
tests/
├── conftest.py              # Shared fixtures
├── unit/
│   ├── conftest.py          # Unit-specific fixtures
│   ├── test_services.py
│   ├── test_validators.py
│   └── test_utils.py
├── integration/
│   ├── conftest.py          # DB fixtures, test client
│   ├── test_api_endpoints.py
│   ├── test_db_operations.py
│   └── test_jobs.py
└── characterization/
    ├── conftest.py
    └── test_legacy_behavior.py
```

### Fixture strategy

Establish reusable fixtures early — they're the foundation for all future tests.

**Essential fixtures to build first**:
1. **Database session** — clean test database per test or per module
2. **Test client** — configured HTTP client for API tests
3. **Authenticated user** — pre-built user with token/session
4. **Sample data factories** — functions that create valid test objects
5. **Environment configuration** — test-specific settings

### Naming conventions

Establish and document naming conventions in the test pattern catalog:

```python
# Test files: test_{module_name}.py
# Test classes: Test{Component}{Behavior}
# Test functions: test_{action}_{condition}_{expected_result}

def test_create_order_with_valid_data_returns_order():
    ...

def test_create_order_with_missing_email_raises_validation_error():
    ...

def test_create_order_when_out_of_stock_returns_409():
    ...
```

---

## Prioritized test plan

After risk mapping and strategy decisions, create a prioritized plan:

### Priority 1 — Characterize critical code (do first)
| Module | Why | Test type | Estimated tests |
|--------|-----|----------|----------------|
| {module} | {risk reason} | Characterization | {N} |

### Priority 2 — Unit test business logic (do second)
| Module | Why | Test type | Estimated tests |
|--------|-----|----------|----------------|
| {module} | {risk reason} | Unit | {N} |

### Priority 3 — Integration test critical paths (do third)
| Module | Why | Test type | Estimated tests |
|--------|-----|----------|----------------|
| {module} | {risk reason} | Integration | {N} |

### Priority 4 — Fill remaining gaps (ongoing)
| Module | Why | Test type | Estimated tests |
|--------|-----|----------|----------------|
| {module} | {reason} | {type} | {N} |

---

## Anti-patterns to avoid

| Anti-pattern | Why it's bad | Instead |
|-------------|-------------|---------|
| Testing implementation details | Tests break on refactor | Test behavior and contracts |
| Excessive mocking | Tests pass but code is broken | Mock at boundaries, not everywhere |
| One giant test per module | Hard to diagnose failures | One assertion per test (roughly) |
| Testing framework behavior | Wasted effort | Test your logic only |
| Copy-paste test code | Hard to maintain | Extract fixtures and helpers |
| Ignoring test speed | Nobody runs slow tests | Keep unit tests under 30 seconds |
| 100% coverage as target | Gaming the metric | Cover the *right* code at any percentage |
