# 07 — Agent Prompts

> Copy-paste prompts for each phase of the testing retrofit. Each prompt is self-contained — paste it into a fresh agent session with the relevant AGENTS.md.

---

## Prompt 1: Coverage Baseline Assessment

```
Read the AGENTS.md, then perform a coverage baseline assessment for this project.

1. Find all existing test files and count them
2. Run the existing test suite and record: total, passed, failed, errors, skipped
3. Generate a coverage report with per-module breakdown
4. List every source module and whether it has a corresponding test file
5. Assess the test infrastructure (framework, fixtures, CI configuration)

Write the results to testing/coverage-baseline.md using the template.
Do NOT fix any failing tests — just document them.
Do NOT write any new tests — just measure what exists.
```

---

## Prompt 2: Risk Priority Mapping

```
Read the AGENTS.md and testing/coverage-baseline.md.

Create a risk priority map for testing by:

1. List all source modules with zero or low coverage
2. For each, assess risk factors:
   - Does it handle data integrity? (weight: 3x)
   - Does it handle auth/authz? (weight: 3x)
   - Does it call external services? (weight: 2x)
   - Is it on the critical user path? (weight: 2x)
   - Does it have complex logic? (weight: 1x)
3. Check git history for change frequency (last 6 months)
4. Check git history for bug-fix frequency
5. Score each module: risk × change_frequency × coverage_gap
6. Sort by score, highest first

Write the prioritized list to testing/risk-priority-map.md using the template.
The output should be a clear, ordered list of what to test first and why.
```

---

## Prompt 3: Characterization Tests

```
Read the AGENTS.md and testing/risk-priority-map.md.

Write characterization tests for the top {N} modules on the risk map.

For each module:
1. Read the source code carefully
2. Identify all public functions/methods
3. For each public function, write tests that capture ACTUAL behavior:
   - Happy path with typical inputs
   - Edge cases (empty input, None, boundary values)
   - Error paths (what exceptions does it raise?)
4. Note any surprising behavior as comments in the tests
5. Do NOT fix bugs you discover — lock the current behavior

Rules:
- Use fixtures from conftest.py
- One behavior per test function
- Mark all tests with @pytest.mark.characterization
- Tests must pass: they document what IS, not what SHOULD BE
- Run the full test suite after to check for conflicts

When done, report:
- Tests added per module
- Coverage change per module  
- Surprises or potential bugs discovered
```

---

## Prompt 4: Build Test Fixtures

```
Read the AGENTS.md and the existing tests in the tests/ directory.

Build a reusable fixture library for this project:

1. Identify common data objects used across tests
2. Create factories for model/entity creation with sensible defaults
3. Create database session fixtures (if integration tests need them)
4. Create API test client fixtures
5. Create authenticated user fixtures
6. Create any environment/config fixtures needed

Place fixtures in:
- tests/conftest.py (shared across all test types)
- tests/unit/conftest.py (unit-specific, no IO)
- tests/integration/conftest.py (database, API client)

Rules:
- Every fixture must be documented with a docstring
- Factories should accept overrides for all fields
- Database fixtures must clean up after themselves
- No fixture should depend on external services
- Run existing tests after to verify nothing broke
```

---

## Prompt 5: Unit Tests for Module

```
Read the AGENTS.md.

Write unit tests for {module_path}.

1. Read the module source code
2. Read existing characterization tests (if any)
3. For each public function/method, write tests for:
   - Valid inputs → expected outputs
   - Edge cases → expected behavior
   - Invalid inputs → expected errors
   - Boundary conditions
4. Use mocks ONLY for external boundaries (DB, API, filesystem)
5. Do NOT mock the function under test
6. Do NOT mock other functions in the same module unless necessary

Follow the naming convention: test_{action}_{condition}_{result}
Mark all tests with @pytest.mark.unit

Target: ≥ 80% coverage for this module.

When done:
1. Run: pytest tests/unit/test_{module}.py -v (all pass)
2. Run: pytest --cov={module_path} (show coverage)  
3. Run: pytest tests/ -v (full suite, no regressions)
```

---

## Prompt 6: Integration Tests for Critical Path

```
Read the AGENTS.md.

Write integration tests for the following critical path:
{describe the user flow or system path}

1. Set up the necessary test data using fixtures
2. Execute the full flow step by step
3. Assert correct behavior at each step
4. Test the happy path end-to-end
5. Test key failure modes (auth failure, invalid input, missing data)
6. Verify database state where applicable

Rules:
- Use a real test database (not mocks)
- Use the test client for API calls
- Clean up test data after each test
- Each test must be independent
- Mark all tests with @pytest.mark.integration

When done:
1. Run: pytest tests/integration/ -v (all pass)
2. Run: pytest tests/ -v (full suite, no regressions)
3. Report: tests added, critical path coverage
```

---

## Prompt 7: CI Gate Setup

```
Read the AGENTS.md and the current test suite.

Set up CI quality gates:

1. Run the full test suite and record total coverage
2. Set the coverage floor at (current_coverage - 1)%
3. Create or update CI configuration to:
   - Run all tests on push and PR
   - Fail on test failures
   - Fail on coverage below floor
   - Report coverage in PR comments (if possible)
4. Verify the CI configuration is correct by running locally

Output:
- CI configuration file (ready to commit)
- Current coverage: {N}%
- Coverage floor set: {N}%
- Instructions for any manual setup needed (e.g., secrets, services)
```

---

## Prompt 8: Test Quality Audit

```
Read the AGENTS.md and all test files.

Audit the current test suite for quality:

1. Check for empty or trivial assertions (assert True, assert result)
2. Check for tests that never fail (mock everything, assert mock)
3. Check for test interdependencies (shared state, execution order)
4. Check for slow tests (> 5 seconds individually)
5. Check for flaky patterns (timing, external deps, random data)
6. Check for duplicated test code (copy-paste across tests)
7. Check naming consistency

For each issue found:
- File and test name
- Issue type
- Severity (high/medium/low)
- Suggested fix

Do NOT fix the issues — just audit and report.
Write results to testing/test-quality-audit.md.
```
