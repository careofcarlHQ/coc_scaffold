# 01 — Process Overview

> From zero tests to meaningful safety net, in measured steps.

---

## The Testing Retrofit Lifecycle

```
Coverage Baseline → Risk Map → Characterization Tests → Unit Tests → Integration Tests → CI Gates
      │                │              │                      │              │              │
  Understand      Prioritize     Lock behavior         Test logic     Test paths      Prevent
  the reality     the work       before change         in isolation   end-to-end      regression
```

Each phase builds on the previous. You cannot prioritize without a baseline, cannot write focused tests without characterization, and cannot set CI gates without tests to run.

---

## Phase 1: Coverage Baseline

**Goal**: Understand the current testing reality with hard numbers.

**Activities**:
- Run the existing test suite (if any) and record results
- Generate a coverage report
- Inventory existing tests by type (unit / integration / e2e)
- Identify modules with zero coverage
- Document the testing infrastructure (framework, fixtures, CI)

**Output**: `coverage-baseline.md` — a snapshot of where testing stands today.

**Gate**: You have a concrete, measurable starting point.

---

## Phase 2: Risk Map

**Goal**: Prioritize where tests are most valuable.

**Activities**:
- Identify critical business logic (money, auth, data integrity)
- Map the most-changed files (git history analysis)
- Map the most-errored paths (logs, bug reports)
- Cross-reference coverage gaps with risk factors
- Rank modules by: risk × change frequency × coverage gap

**Output**: `risk-priority-map.md` — ordered list of what to test first.

**Gate**: A clear, justified priority list that explains *why* each module matters.

---

## Phase 3: Characterization Tests

**Goal**: Lock the current behavior of critical code before changing anything.

**Activities**:
- For each high-priority module, write tests that capture *what it actually does*
- Include edge cases you discover while exploring the code
- Test the "happy path" and the main error paths
- Don't fix bugs you discover — document them as known behavior
- Build reusable test fixtures and helpers as you go

**Output**: Characterization tests for top-priority modules. `test-pattern-catalog.md` with reusable patterns.

**Gate**: Critical modules have behavior-locking tests. All pass. Coverage increased measurably.

---

## Phase 4: Unit Tests

**Goal**: Test individual components in isolation, starting with the highest-risk code.

**Activities**:
- Write focused unit tests for business logic functions
- Test edge cases, boundary conditions, error handling
- Use mocks/stubs for external dependencies (DB, APIs, filesystem)
- Follow the test pattern catalog for consistency
- Add tests to modules from the risk map, in priority order

**Output**: Unit tests for high-risk business logic. Coverage grows significantly.

**Gate**: All business-critical functions have unit tests. Tests are fast (< 30 seconds for the unit suite).

---

## Phase 5: Integration Tests

**Goal**: Verify that components work together correctly along critical paths.

**Activities**:
- Identify the critical user flows (the paths that make or break the product)
- Write tests that exercise full request-response cycles
- Test the database interaction layer with a real (test) database
- Test API endpoints end-to-end
- Test job/queue/dispatch paths

**Output**: Integration tests for critical paths. Full test suite covers both happy paths and key error scenarios.

**Gate**: Critical flows have integration tests. The full test suite runs in under 5 minutes.

---

## Phase 6: CI Gates

**Goal**: Prevent regression by making tests part of the development workflow.

**Activities**:
- Configure CI to run the full test suite on every push/PR
- Set a coverage threshold (a floor, not a ceiling — start conservative)
- Add a "no new code without tests" policy for new work
- Configure coverage reporting in PRs
- Set up test result reporting and failure notifications

**Output**: CI pipeline with quality gates. `testing-checklist.md` fully completed.

**Gate**: No code merges without passing tests. Coverage can only go up.

---

## Phase Overlap

Phases 3–5 will often overlap in practice. As you write characterization tests, you'll naturally refine some into proper unit tests. As you add unit tests, you'll identify integration test needs. That's fine — the phases give you a direction, not a rigid sequence. But always start with characterization. Always.

---

## What comes after?

Testing retrofit is never "done." After the initial retrofit:

- Every new feature includes tests (use the **feature-addition** scaffold)
- Every bug fix includes a regression test (use the **bug-investigation** scaffold)
- Every refactoring is preceded by characterization tests (use the **refactoring** scaffold)
- Coverage threshold ratchets up gradually as coverage grows
- Test infrastructure improves over time (speed, reliability, ergonomics)
