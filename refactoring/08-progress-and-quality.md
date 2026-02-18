# 08 — Progress and Quality

## Why tracking matters for refactoring

Refactoring is uniquely dangerous to track poorly because:
- It produces no visible features — stakeholders can't see progress
- It's easy to lose momentum ("we refactored for 3 weeks and nothing changed")
- Without metrics, you can't prove the refactoring was worth doing
- Without a log, a new agent can't pick up where the last one left off

## Session resumption

Refactoring projects span multiple agent sessions. Every new session starts with:

```markdown
## Resumption Checklist (start of every session)

1. Read `refactor/refactoring-log.md` — last 3 entries
2. Confirm: what target and stage am I on?
3. Run `pytest -x` — is the baseline green?
4. Run `git log --oneline -5` — do recent commits match the log?
5. Resume from the exact stage recorded in the log

Do NOT:
- Re-read files that were already characterized
- Re-run assessment on modules already assessed
- Start over from Phase 1 if Phase 2 is in progress
```

The refactoring log is the single source of truth for "where we left off." If AGENTS.md says Phase 2, Stage 4, but the log says Stage 5 was completed — trust the log.

## Metrics to track

### Before/after comparison (per target)

Track these metrics for every refactoring target at Stage 0 (before) and Stage 9 (after):

| Metric | Why | How to measure |
|--------|-----|---------------|
| Lines of code | Size reduction | `wc -l` on target files |
| Max function length | Readability | Longest function in target |
| Cyclomatic complexity (avg) | Maintainability | `radon cc` or equivalent |
| Cyclomatic complexity (max) | Worst spots | Highest-rated function |
| Number of importers | Coupling | `grep -r "from {module}"` count |
| Number of imports | Fan-out | Count of internal imports in target |
| Test coverage (%) | Safety | `pytest --cov` on target |
| Circular dependencies | Design quality | `pydeps` or manual check |

### Phase-level metrics

Track these across the entire refactoring effort:

| Metric | Target |
|--------|--------|
| Total targets planned | ___ |
| Targets completed | ___ |
| Targets deferred / abandoned | ___ |
| PRs merged | ___ |
| PRs reverted | ___ |
| Test failures during refactoring | ___ (should be 0) |
| Coverage trend | ↑ or → (never ↓) |
| Average complexity trend | ↓ or → (never ↑) |

### Effort tracking

| Metric | Value |
|--------|-------|
| Total elapsed time | ___ |
| Phase 1 (safety net) effort | ___ |
| Phase 2 (core restructuring) effort | ___ |
| Phase 3 (cleanup) effort | ___ |
| Human review time | ___ |
| Agent execution time | ___ |
| Blocked time (waiting for decisions) | ___ |

## Quality gates

### Per-PR quality gate

Every refactoring PR must pass:

- [ ] Single named refactoring pattern applied
- [ ] No behavior changes
- [ ] All tests pass
- [ ] Coverage ≥ baseline
- [ ] No new lint or type errors
- [ ] Migration map entry satisfied
- [ ] Refactoring log updated

### Per-target quality gate

A refactoring target is complete when:

- [ ] All migration map entries for this target are satisfied
- [ ] Before/after metrics show improvement
- [ ] All tests pass (including new characterization tests)
- [ ] No callers reference the old structure
- [ ] Old code is deleted
- [ ] Docs updated to reflect new structure

### Per-phase quality gate

A refactoring phase is complete when:

- [ ] All targets in the phase pass their quality gates
- [ ] Phase-level metrics meet stopping criteria
- [ ] No pending rollbacks
- [ ] Documentation freshness check passed
- [ ] Decision to proceed / stop Phase 3 is made and recorded

## Progress tracking format

### Scoreboard (update weekly or per-target)

```markdown
# Refactoring Scoreboard — {project_name}

Last updated: {date}

## Phase Summary

| Phase | Status | Targets | Completed | Remaining |
|-------|--------|---------|-----------|-----------|
| Phase 1 — Safety Net | {status} | {n} | {n} | {n} |
| Phase 2 — Core Restructuring | {status} | {n} | {n} | {n} |
| Phase 3 — Cleanup | {status} | {n} | {n} | {n} |

## Current Target

Target: {name}
Pattern: {refactoring pattern}
Stage: {N} / 10
Blocker: {none / description}

## Metrics Trend

| Metric | Baseline | Current | Trend |
|--------|----------|---------|-------|
| Avg complexity | {n} | {n} | ↓ / → / ↑ |
| Max file length | {n} | {n} | ↓ / → / ↑ |
| Circular deps | {n} | {n} | ↓ / → / ↑ |
| Test coverage | {n}% | {n}% | ↑ / → / ↓ |
| Total tests | {n} | {n} | ↑ / → |

## PRs

| PR | Target | Pattern | Status |
|----|--------|---------|--------|
| #{n} | {target} | {pattern} | merged / reverted / open |
```

## When to stop refactoring

Refactoring has diminishing returns. Use these signals to decide when to stop:

### Stop signals (positive — mission accomplished)

- All P0 targets from the assessment are complete
- Metrics meet the stopping criteria defined in the plan
- New features can be added by touching 1–3 files instead of 10+
- Team reports reduced pain in the refactored areas
- Coverage on refactored areas > 80%

### Stop signals (negative — diminishing returns)

- Remaining targets are P2 (cosmetic improvements)
- Each target takes 3x longer than the previous one
- Targets are deeply intertwined and can't be isolated
- The team needs to ship features and refactoring is blocking
- More bugs are being introduced than structural improvements made

### Decision log entry for stopping

```markdown
### Decision: Stop / Continue Refactoring

Date: {date}
Phase completed: {N}
Reason: {why stopping or continuing}
Metrics at stop:
- Complexity: {before} → {after}
- Coverage: {before} → {after}
- File sizes: {before} → {after}
Remaining targets: {list with priority}
Recommendation: Ship / Continue Phase {N+1} / Revisit in {timeframe}
```

## Post-refactoring maintenance

After refactoring is complete:

1. **Update AGENTS.md** — transition from refactoring-mode to operational-mode
2. **Archive refactor/ directory** — or keep as historical record
3. **Set up drift detection** — add lint rules or CI checks that prevent the patterns you just fixed from recurring
4. **Schedule 30-day review** — check if the refactoring is holding or reverting to old patterns
5. **Share learnings** — document what worked and what didn't for the next refactoring effort
