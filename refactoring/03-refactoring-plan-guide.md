# 03 — Refactoring Plan Guide

## Why a plan matters for agent-driven refactoring

Refactoring without a plan is how agents produce chaos. They'll happily restructure everything they touch — and without a plan, they'll restructure differently each time. A good refactoring plan gives the agent a clear target, named patterns, and stopping criteria.

## The refactoring plan hierarchy

```
Assessment (what's wrong)
  └── Refactoring Plan (what to do about it)
       ├── Phase 1 — Safety Net (tests first)
       ├── Phase 2 — Core Restructuring (highest-impact targets)
       ├── Phase 3 — Secondary Cleanup (lower-priority improvements)
       └── Migration Maps (old → new, per target)
```

## Writing rules

### 1. Every target must trace to assessment evidence

```markdown
# ❌ Bad
Refactor the ingestion module — it's messy.

# ✅ Good
Refactor app/ingestion/ — 3 files over 400 lines, cyclomatic complexity
average 15, changed 47 times in last 6 months, 12% test coverage.
Primary problem: business logic mixed with HTTP handling.
```

### 2. Name the refactoring patterns explicitly

```markdown
# ❌ Bad
Clean up the service layer.

# ✅ Good
Phase 2, Stage 3 — Service layer restructuring:
1. Extract function: move validation logic from route handlers to validators
2. Move module: relocate shared utilities from app/api/utils.py to app/core/
3. Introduce protocol: create OrderProcessor protocol to decouple dispatch from services
4. Consolidate duplicates: merge 3 copies of price calculation into app/core/pricing.py
```

### 3. Define migration maps with precision

A migration map tells the agent exactly what moves where. **Always anchor to function/class names, never line numbers** — line numbers go stale the moment any earlier line is edited.

```markdown
### Migration: Split app/services/orders.py (450 lines)

| Current location | New location | Pattern | What moves |
|-----------------|--------------|---------|------------|
| app/services/orders.py::create_order(), validate_order_input() | app/services/order_creation.py | Extract module | Order creation logic |
| app/services/orders.py::fulfill_order(), schedule_shipment() | app/services/order_fulfillment.py | Extract module | Fulfillment workflow |
| app/services/orders.py::calculate_price(), apply_discount() | app/core/pricing.py | Move function | Price calculation |
| app/services/orders.py::get_order(), list_orders(), search_orders() | app/services/order_queries.py | Extract module | Read-only queries |
| app/services/orders.py::OrderStateMachine, transition_state() | app/services/order_state.py | Extract module | State machine transitions |

Callers to update:
- app/api/routes/orders.py — imports order creation and queries
- app/jobs/fulfillment_worker.py — imports fulfillment workflow
- app/api/routes/admin.py — imports order queries
```

> **Why function names, not line numbers?** An agent that reads `orders.py:15-85` must count lines to find the code. If a previous refactoring step added 3 lines above line 15, the anchor is already wrong. `orders.py::create_order()` is self-healing — the agent can `grep` for it regardless of surrounding changes.

### 4. Specify test requirements per target

```markdown
### Pre-refactoring test requirements for app/services/orders.py

Current coverage: 35%
Required before restructuring: 80%

Tests needed:
- [ ] Order creation — valid input → 201 with order ID
- [ ] Order creation — duplicate order_id → 409
- [ ] Order creation — missing required fields → 422
- [ ] Price calculation — standard items → correct total
- [ ] Price calculation — discounted items → discount applied
- [ ] State transition — valid transition → success
- [ ] State transition — invalid transition → 409
- [ ] State transition — terminal state → blocked
```

### 5. Define stopping criteria for each phase

```markdown
# ❌ Bad
Phase 2 complete when code is clean.

# ✅ Good
Phase 2 complete when:
1. No file in app/services/ exceeds 200 lines
2. No function in refactored modules exceeds 30 lines
3. Zero circular dependencies in app/services/
4. All tests pass (including new characterization tests)
5. Test coverage on refactored modules ≥ 80%
6. Cyclomatic complexity average < 8 in refactored modules
```

### 6. Document rollback strategy per change

Every structural change should have a rollback plan:

```markdown
### Rollback: Split orders.py

Rollback trigger: Test failures that can't be resolved within 2 hours

Steps:
1. Revert the split PR
2. Verify tests pass on reverted code
3. Log the failure reason in refactoring log
4. Re-assess the migration map before retrying
```

## Refactoring plan structure

### 1. Scope and motivation

- What problem are we solving?
- What does "better" look like concretely?
- What's explicitly out of scope?
- What's the expected benefit? (faster development, fewer bugs, easier onboarding)

### 2. Phases overview

| Phase | Focus | Targets | Estimated effort |
|-------|-------|---------|-----------------|
| Phase 1 | Safety net | Tests for refactoring targets | X days |
| Phase 2 | Core restructuring | Highest-impact modules | X days |
| Phase 3 | Secondary cleanup | Lower-priority improvements | X days |

### 3. Per-phase details

For each phase:
- Stages with named refactoring patterns
- Migration maps
- Test requirements
- Acceptance gates
- Stopping criteria
- Rollback strategy

### 4. Dependency order

Some refactoring must happen in order:

```
1. Write characterization tests (Phase 1) — enables everything else
2. Split god modules (Phase 2, Stage 1) — unblocks layer cleanup
3. Fix layering violations (Phase 2, Stage 2) — requires modules to exist
4. Consolidate duplicates (Phase 2, Stage 3) — easier after layers are clean
5. Rename for clarity (Phase 3) — do last to avoid unnecessary churn
```

### 5. Risk register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Characterization tests miss edge cases | Medium | High | Run tests against production-like data |
| Refactoring introduces subtle behavior change | Medium | High | Compare I/O pairs before/after |
| Team needs code during refactoring (merge conflicts) | High | Medium | Coordinate timing, keep PRs small |
| Scope creep (finding more to fix during execution) | High | Medium | Log discoveries, don't act until planned |

## Common mistakes

| Mistake | Why it fails | Fix |
|---------|-------------|-----|
| Refactoring without tests | Can't verify behavior preserved | Phase 1 exists specifically for this |
| Too many patterns in one PR | Hard to review, risky to merge | One named pattern per PR |
| Mixing refactoring with features | Can't isolate regressions | Separate branches, separate PRs |
| No stopping criteria | Refactoring never ends | Define concrete "done" metrics |
| Starting with renames | Causes unnecessary churn early | Rename as the final step |
| No migration map | Agent makes ad-hoc decisions | Map every move before executing |
