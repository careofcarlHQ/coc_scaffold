# 01 — Process Overview: End-to-End Refactoring Workflow

## The refactoring lifecycle

Refactoring with this scaffold follows a predictable lifecycle. Each phase builds on the previous one, and every transition has an explicit safety gate.

```
┌─────────────────────────────────────────────────────────┐
│                  REFACTORING LIFECYCLE                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. ASSESSMENT         Measure code health              │
│       │                                                 │
│       ▼                                                 │
│  2. PRIORITIZATION     Rank problems by impact          │
│       │                                                 │
│       ▼                                                 │
│  3. PLANNING           Design transformation strategy   │
│       │                                                 │
│       ▼                                                 │
│  4. SAFETY NET         Characterization tests + CI      │
│       │                                                 │
│       ▼                                                 │
│  5. EXECUTION          Phased refactoring with gates    │
│       │                                                 │
│       ▼                                                 │
│  6. VERIFICATION       Prove behavior preserved         │
│       │                                                 │
│       ▼                                                 │
│  7. STABILIZATION      Update docs, close gaps          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Phase breakdown

### 1. Assessment (Day 1–2)

**Input**: A working codebase with suspected structural problems
**Output**: Quantified code health report

Activities:
- Run complexity metrics (cyclomatic complexity, file length, function length)
- Map dependency graph (what imports what)
- Identify hotspots (files changed most often in git history)
- Measure test coverage per module
- Catalog known pain points from the team
- Identify code duplication

Key documents:
- `refactor/codebase-assessment.md`

### 2. Prioritization (Day 2)

**Input**: Assessment data
**Output**: Ranked list of refactoring targets

Activities:
- Score each problem area by: impact × frequency × risk
- Classify as P0 (blocks progress), P1 (slows progress), P2 (cosmetic)
- Estimate effort for each target
- Identify dependencies between targets (must do A before B)

Scoring matrix:

| Factor | Low (1) | Medium (2) | High (3) |
|--------|---------|------------|----------|
| Impact | Cosmetic or convenience | Slows development | Blocks features or causes bugs |
| Frequency | Rarely touched | Touched monthly | Touched weekly |
| Risk | Isolated, well-tested | Some coupling | Deeply coupled, under-tested |

Priority = Impact × Frequency. Start with highest score, adjusted for dependencies.

### 3. Planning (Day 2–3)

**Input**: Prioritized targets
**Output**: Refactoring plan with phases and migration maps

Activities:
- Group related targets into phases (1–3 phases typical)
- For each phase, define concrete stages with acceptance gates
- Create migration maps: old structure → new structure
- Define "done" criteria for each phase
- Identify what tests need to exist before restructuring begins
- Define rollback strategy for each structural change

Key documents:
- `refactor/refactoring-plan.md`
- `refactor/migration-map.md`
- `refactor/risk-register.md`

### 4. Safety Net (Day 3–5)

**Input**: Refactoring plan + existing test suite
**Output**: Characterization tests covering refactoring targets

This is the most important phase. Without adequate tests, refactoring is guesswork.

**Pre-requisite (Phase 0):** Before writing any tests, confirm the test infrastructure works:
- `pytest --co` discovers tests without errors
- DB fixtures and test clients are functional
- CI runs tests and reports results
- Assessment tools (radon, pytest-cov) are installed

If Phase 0 fails, fix infrastructure before proceeding.

Activities:
- Audit test coverage on areas targeted for refactoring
- Write characterization tests for uncovered behavior
- Write integration tests for cross-module interactions being changed
- Verify CI pipeline catches regressions
- Establish baseline metrics (test count, coverage %, build time)

Key documents:
- `refactor/characterization-test-plan.md`

Characterization tests capture **what the code does**, not what it should do:

```python
# ❌ Prescriptive test (describes intent)
def test_order_total_excludes_tax():
    assert calculate_total(items) == 100.00

# ✅ Characterization test (describes actual behavior)
def test_order_total_current_behavior():
    # Captures that calculate_total currently INCLUDES tax
    # This may be a bug, but we're preserving behavior during refactoring
    assert calculate_total(items) == 108.50
```

### 5. Execution (Day 5+)

**Input**: Safety net in place + refactoring plan
**Output**: Restructured code with passing tests

See [04-phased-refactoring-guide.md](04-phased-refactoring-guide.md) for the stage pattern.

Rules during execution:
- One named refactoring pattern per PR
- Full test suite passes after every change
- No feature changes mixed with structural changes
- Log every decision and deviation from plan
- Stop if test failures can't be explained

### 6. Verification (After each phase)

**Input**: Completed phase
**Output**: Evidence that behavior is preserved

Activities:
- Run full test suite and compare results to baseline
- Compare metrics: coverage should not decrease
- Run smoke tests / integration tests
- Review dependency graph: did coupling decrease?
- Spot-check key user flows manually

### 7. Stabilization (After all phases)

**Input**: Completed refactoring
**Output**: Updated documentation, closed gaps

Activities:
- Update AGENTS.md to reflect new structure
- Update architecture docs and module maps
- Update onboarding guides
- Archive the migration map (mark as completed)
- Write decision log entry: what changed and why
- Run the [repo-documentation](../repo-documentation/) freshness check

---

## Task-level workflow

Within execution, individual refactoring tasks follow this lifecycle:

```
Identify → Characterize → Protect → Transform → Verify → Document → Merge
```

### Identify (Human)
- Name the specific refactoring pattern
- Define the scope (which files, which functions)
- State the motivation (why this change)
- State the stopping criteria (what "done" looks like)

### Characterize (Agent)
- Read the code being changed
- Document current behavior (inputs, outputs, side effects)
- Identify all callers / dependents

### Protect (Agent)
- Write or verify characterization tests
- Confirm CI is green before starting

### Transform (Agent)
- Apply the named refactoring pattern
- Keep the change minimal and mechanical
- Don't fix bugs found during refactoring (log them instead)

### Verify (Agent)
- Run full test suite
- Confirm no behavior change
- Compare complexity metrics before/after

### Document (Agent)
- Update any docs that reference changed code
- Log the change in the refactoring log
- Note any bugs discovered (but not fixed)

### Merge (Human)
- Review the change against the refactoring plan
- Confirm the migration map entry is satisfied
- Approve and merge
