# 02 — Coverage Baseline Checklist

> You cannot improve what you haven't measured. This guide helps you take an honest snapshot of the current testing reality.

---

## Step 1: Inventory existing tests

Before running anything, find out what exists.

### Quick commands

```bash
# Count test files
find . -name "test_*.py" -o -name "*_test.py" | wc -l

# Count test functions
grep -r "def test_" tests/ --include="*.py" | wc -l

# List test files by directory
find . -name "test_*.py" -o -name "*_test.py" | sort

# Check for fixtures
grep -r "@pytest.fixture" tests/ --include="*.py" | wc -l

# Check for conftest files
find . -name "conftest.py" | sort
```

### Test inventory table

Fill this out for each test directory/module:

| Directory | Test files | Test functions | Type | Last modified | Notes |
|-----------|-----------|---------------|------|--------------|-------|
| tests/unit/ | {N} | {N} | Unit | {date} | {notes} |
| tests/integration/ | {N} | {N} | Integration | {date} | {notes} |
| tests/ (root) | {N} | {N} | Mixed | {date} | {notes} |

---

## Step 2: Run existing tests

Run everything and record results honestly. Don't fix anything yet.

```bash
# Run with verbose output
pytest -v 2>&1 | tee test-results-baseline.txt

# Run with coverage
pytest --cov=app --cov-report=term-missing --cov-report=html 2>&1 | tee coverage-baseline.txt
```

### Record the results

| Metric | Value |
|--------|-------|
| Total tests | {N} |
| Passed | {N} |
| Failed | {N} |
| Errors | {N} |
| Skipped | {N} |
| Warnings | {N} |
| Duration | {seconds} |
| Overall coverage | {N}% |

### Failing tests

| Test | Error | Probably why | Worth fixing? |
|------|-------|-------------|---------------|
| {test name} | {error} | {guess} | {yes/no/later} |

---

## Step 3: Coverage by module

Break coverage down to the module level. This is where the real picture emerges.

```bash
# Coverage by file (sorted by coverage ascending — worst first)
pytest --cov=app --cov-report=term-missing | sort -t'%' -k2 -n
```

### Module coverage table

| Module | Lines | Covered | Coverage | Critical? | Changes (6mo) |
|--------|-------|---------|----------|-----------|---------------|
| app/services/billing.py | {N} | {N} | {N}% | Yes | {N commits} |
| app/api/routes.py | {N} | {N} | {N}% | Yes | {N commits} |
| app/core/auth.py | {N} | {N} | {N}% | Yes | {N commits} |
| ... | | | | | |

---

## Step 4: Test infrastructure assessment

Understanding the testing *infrastructure* matters as much as the tests themselves.

### Framework and tooling

| Question | Answer |
|----------|--------|
| Test framework? | {pytest / unittest / other} |
| Configuration file? | {pyproject.toml / pytest.ini / setup.cfg} |
| Coverage tool? | {pytest-cov / coverage.py / none} |
| Fixture management? | {conftest.py / custom / none} |
| Test database strategy? | {in-memory / test DB / shared DB / none} |
| Factory library? | {factory-boy / custom / none} |
| Mock library? | {unittest.mock / pytest-mock / none} |
| API test client? | {TestClient / httpx / requests / none} |
| CI runs tests? | {yes — tool / no} |
| CI blocks on failure? | {yes / no / no CI} |

### Test ergonomics

| Question | Answer |
|----------|--------|
| Can you run tests with one command? | {yes / no — what's needed?} |
| Do tests require external services? | {list} |
| Do tests require specific env vars? | {list} |
| How long does the full suite take? | {seconds} |
| Are there flaky tests? | {yes — which / no} |
| Is there a test README or guide? | {yes / no} |

---

## Step 5: Gap analysis

List every source module and its test status.

```bash
# List all source files
find app/ -name "*.py" ! -name "__init__.py" | sort

# List all test files
find tests/ -name "test_*.py" | sort

# Find source files with no corresponding test
# (manual comparison of the two lists above)
```

### Gap table

| Source module | Has test file? | Has any tests? | Coverage | Priority |
|--------------|---------------|---------------|----------|----------|
| app/services/billing.py | No | No | 0% | **Critical** |
| app/core/auth.py | Yes | 2 tests | 12% | **High** |
| app/api/routes.py | No | No | 0% | **High** |
| app/db/models.py | No | No | 0% | Medium |
| app/utils/helpers.py | Yes | 8 tests | 65% | Low |

---

## Step 6: Compile the baseline document

Using the `coverage-baseline.md.template`, compile everything into a single document that becomes the reference point for all retrofit work. This document answers: "Where were we when we started?"

Store it at: `testing/coverage-baseline.md`

---

## Baseline quality gate

You've completed the baseline when you can answer all of these:

- [ ] I know exactly how many tests exist and how many pass
- [ ] I have module-level coverage numbers
- [ ] I know which modules have zero coverage
- [ ] I understand the test infrastructure (or lack thereof)
- [ ] I've documented the gap between source modules and test modules
- [ ] The baseline document is committed to the repo
