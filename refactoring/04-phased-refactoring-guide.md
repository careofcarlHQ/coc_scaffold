# 04 — Phased Refactoring Guide

## The stage pattern

Every refactoring phase follows a safety-first pattern. Unlike greenfield where you build up, refactoring decomposes and reconstructs — so every stage has both a safety gate (behavior preserved?) and a progress gate (closer to target?).

```
Stage 0   Pre-flight — verify baseline is green
Stage 1   Characterize — capture current behavior
Stage 2   Protect — add missing tests
Stage 3   Prepare — create target structure
Stage 4   Migrate — move code to new structure
Stage 5   Redirect — update callers
Stage 6   Verify — full regression check
Stage 7   Clean up — remove old code and scaffolding
Stage 8   Document — update docs and maps
Stage 9   Measure — compare metrics before/after
Stage 10  Sign-off — phase complete
```

## Stage design rules

### 0. Understand what an "atomic change" is

An atomic change is the smallest code edit that can be independently verified. Each atomic change should:
- Be completable in a single step (one function move, one caller redirect, one import update)
- Leave the codebase in a green state (all tests pass after the change)
- Be revertible with a single `git revert`

Examples of atomic changes:
- Move one function from file A to file B
- Update one caller to import from the new location
- Delete one now-unused re-export from the old file
- Add one characterization test for one function

Examples of NON-atomic changes:
- Move 5 functions and update all callers in one step
- "Reorganize" an entire module
- Fix a bug while also moving code

### 1. Each stage should be completable in 1–4 hours

If a stage takes longer, the refactoring target is too large. Split the target into smaller pieces and apply the stage pattern to each piece.

### 2. Each stage has a safety gate

A safety gate verifies **no behavior has changed**:

```markdown
# ✅ Good safety gates
- All existing tests pass (zero new failures)
- Test coverage has not decreased
- Application starts and health check passes
- Key API endpoints return same responses for same inputs
- No new lint or type-check errors

# ❌ Bad safety gates
- "Code looks correct"
- "Should still work"
- "Tests mostly pass"
```

### 3. Never skip Stage 0

Stage 0 establishes your green baseline. If the baseline isn't green, you can't distinguish new failures from pre-existing ones. Fix the baseline before starting any refactoring.

### 4. Stages 1–2 are mandatory, even if tedious

The temptation is to skip straight to moving code. Don't. Characterization tests are the safety net that catch regressions. Without them, you're refactoring blind.

**Difficulty tiers for characterization tests:**
| Tier | Description | Strategy | Typical effort |
|------|-------------|----------|----------------|
| Easy | Pure functions: no DB, no I/O | Capture I/O pairs | Minutes per function |
| Medium | DB access, fixtures needed | Snapshot or contract tests | 15–30 min per function |
| Hard | External APIs, file I/O, async | Mocking + side-effect verification | 30–60 min per function |

Start with easy functions to build coverage quickly. For hard functions, assess whether characterization testing is cost-effective — if a function has 3 callers and is clearly mechanical, manual review may be faster than building a mock harness.

---

## Phase 0 — Test Infrastructure (Confirm the Harness Works)

Before writing characterization tests, verify the test infrastructure itself is functional. Agents often waste hours writing tests that fail for infrastructure reasons, not logic reasons.

```
Stage 0  — Verify pytest runs
           Run `pytest --co` (collect only) to confirm test discovery works.
           Gate: pytest discovers existing tests without errors.

Stage 1  — Verify fixtures exist
           Check that DB fixtures, test clients, and factories are available:
           - Can you create a test DB session?
           - Can you create a test HTTP client?
           - Do existing factory/fixture helpers work?
           Gate: A trivial test using the main fixture passes.

Stage 2  — Verify CI runs tests
           Confirm CI/CD pipeline runs the test suite and reports results.
           Gate: CI green on current branch.

Stage 3  — Install missing tools
           Install any tools needed for assessment and validation:
           - `pip install radon` (complexity analysis)
           - `pip install pytest-cov` (coverage)
           - Linter and type checker configured
           Gate: All assessment commands from 02-codebase-assessment-checklist run without errors.
```

Phase 0 is typically 30–60 minutes. If it takes longer, there are infrastructure problems that must be fixed before any refactoring.

---

## Phase 1 — Safety Net (Build the Harness)

The first phase of any refactoring project is building the test coverage needed to refactor safely.

```
Stage 0  — Pre-flight
           Verify all existing tests pass. Record baseline metrics.
           Gate: CI green, coverage report generated, metrics recorded.

Stage 1  — Identify Coverage Gaps
           Map test coverage per module targeted for refactoring.
           List every uncovered code path that will be touched.
           Gate: Coverage gap report complete for all refactoring targets.

Stage 2  — Write Characterization Tests
           For each uncovered path in refactoring targets:
           - Call the function with representative inputs
           - Assert on the actual outputs (even if they seem wrong)
           - Test edge cases and error paths
           Gate: Coverage on refactoring targets ≥ 80%.

Stage 3  — Write Integration Tests
           Test cross-module interactions being restructured:
           - Caller → callee relationships being changed
           - Database queries being moved
           - Side effects being relocated
           Gate: Every cross-module boundary has at least one test.

Stage 4  — Verify Baseline Stability
           Run `./refactor/verify-baseline.ps1 -Stability` to check for flaky tests.
           The script runs the full suite 3 times automatically.
           Gate: Script exits 0 (3 consecutive green runs).

Stage 5  — Sign-off
           Record final baseline: test count, coverage %, build time.
           Gate: Phase 1 metrics recorded. Ready for structural changes.
```

## Phase 2 — Core Restructuring

Apply the refactoring plan to the highest-impact targets. Each target follows the stage pattern.

### Per-target pattern

For each refactoring target in the plan:

```
Stage 0  — Pre-flight
           CI green. Migration map for this target reviewed.
           Gate: Baseline green, target scope confirmed.

Stage 1  — Characterize
           Read the target code. Document:
           - All public functions/methods and their signatures
           - All callers (who imports/calls this code)
           - All side effects (DB writes, API calls, file I/O)
           - All configuration dependencies
           Gate: Characterization documented in refactoring log.

Stage 2  — Protect
           Verify characterization tests cover this specific target.
           Add any missing tests discovered during characterization.
           Gate: Target-specific tests identified and passing.

Stage 3  — Prepare
           Create the new target structure:
           - New files/modules with empty shells or interfaces
           - New test files for the new structure
           Do NOT move code yet — just create the destination.
           Gate: New structure exists. No code moved yet. Tests still pass.

Stage 4  — Migrate
           Move code from old location to new location:
           - Apply the named refactoring pattern
           - Keep old code temporarily as pass-through (strangler fig)
           - Update imports in the moved code
           - **Python `__init__.py` rule**: If the old module is re-exported from
             an `__init__.py`, add a re-export of the new location there too.
             Callers who import from the package (not the file) must keep working.
           Gate: Code exists in new location. Old location delegates to new.
                 Tests pass.

Stage 5  — Redirect
           Update all callers to use the new location:
           - Change imports one caller at a time
           - Run tests after each caller update
           Gate: All callers use new location. Zero-callers verified (see checklist below).
                 Tests pass.

           **Zero-callers verification checklist** — before deleting old code:
           ```bash
           # 1. Grep for direct imports
           grep -rn "from {old_module} import" {source_root}/ --include="*.py"
           # 2. Grep for module-level imports
           grep -rn "import {old_module}" {source_root}/ --include="*.py"
           # 3. Check test files (often forgotten)
           grep -rn "{old_module}" tests/ --include="*.py"
           # 4. Check scripts and CLI
           grep -rn "{old_module}" scripts/ --include="*.py"
           # 5. Check config files (alembic, celery, pytest, etc.)
           grep -rn "{old_module}" *.ini *.cfg *.toml *.yaml *.yml 2>/dev/null
           # 6. Check dynamic imports / string references
           grep -rn "{old_module_name}" {source_root}/ --include="*.py"
           # 7. Check CI/CD configs
           grep -rn "{old_module}" .github/ .gitlab-ci.yml Dockerfile docker-compose.yml 2>/dev/null
           ```
           All 7 checks must return empty before old code is deleted.

Stage 6  — Verify
           Run full regression suite:
           - All tests pass
           - Coverage has not decreased
           - No new lint or type errors
           - Quick smoke test of key user flows
           Gate: Full suite green. Coverage ≥ baseline.

Stage 7  — Clean Up
           Remove the old code:
           - Delete old files/functions
           - Remove pass-through shims
           - Remove any temporary imports
           Gate: Old code deleted. Tests still pass. No dead imports.

Stage 8  — Document
           Update docs to reflect new structure:
           - Migration map entry marked complete
           - Module descriptions updated
           - Architecture docs updated (if applicable)
           Gate: No doc references the old structure.

Stage 9  — Measure
           Compare metrics before/after:
           - Lines of code (per module)
           - Cyclomatic complexity
           - Number of importers (coupling)
           - Test coverage
           Gate: Metrics show improvement on target dimensions.

Stage 10 — Sign-off
           Refactoring target complete. Log results.
           Gate: All stages passed. Merged to main.
```

## Phase 3 — Secondary Cleanup (optional)

Apply the same per-target pattern to lower-priority targets from the assessment. Common Phase 3 targets:

```
- Consolidate remaining code duplication
- Improve naming consistency
- Extract reusable utilities
- Add type annotations to clarified interfaces
- Simplify over-engineered abstractions
- Remove dead code
```

Phase 3 is optional — only proceed if Phase 2 completed within budget and the team agrees the remaining targets are worth pursuing.

---

## Tracking progress

Use the refactoring log template to track each target:

```markdown
### Target: {name} — {pattern}

- Status: not-started / characterizing / protected / migrating / verifying / done
- Baseline metrics:
  - Lines: ___
  - Complexity: ___
  - Coverage: ___%
  - Importers: ___
- Current metrics:
  - Lines: ___
  - Complexity: ___
  - Coverage: ___%
  - Importers: ___
- Stages completed: 0 / 1 / 2 / 3 / 4 / 5 / 6 / 7 / 8 / 9 / 10
- Decisions made:
- Bugs discovered (not fixed):
- Rollback needed: yes / no
```

## Common pitfalls

| Pitfall | Consequence | Prevention |
|---------|-------------|------------|
| Skipping Phase 1 (safety net) | Can't verify behavior preserved | Phase 1 is mandatory, no exceptions |
| Moving code and fixing bugs at once | Can't isolate regressions | Log bugs, fix in separate PR |
| Deleting old code before redirecting all callers | Runtime errors | Only delete when zero callers remain |
| Refactoring 5+ targets in parallel | Merge conflicts, confusion | One target at a time unless independent |
| Not measuring before/after | Can't prove improvement | Record metrics at Stage 0 and Stage 9 |
| Continuing past Phase 2 without reassessing | Diminishing returns | Re-evaluate impact before Phase 3 |
