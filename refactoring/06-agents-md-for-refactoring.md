# 06 — Writing AGENTS.md for a Refactoring Project

## Purpose

When an agent works on a refactoring project, it needs different orientation than a greenfield build or documentation effort. The agent must understand:

1. What the code does today (don't break it)
2. What the target structure looks like (where we're going)
3. What refactoring patterns to apply (how to get there)
4. What safety checks to run (how to verify)

## Key difference from other scaffolds

- **Greenfield AGENTS.md**: "Here's the spec, build it"
- **Documentation AGENTS.md**: "Here's the code, describe it"
- **Refactoring AGENTS.md**: "Here's the code, here's the plan, transform it safely"

The refactoring AGENTS.md must simultaneously describe the current reality AND the target state.

## Structure template

```markdown
# AGENTS.md — {PROJECT_NAME} (Refactoring)

## Mission
{One-sentence description of the refactoring goal.}

## Current State
{Brief description of the system as it exists today.}

## Target State
{Brief description of what the system should look like after refactoring.}

## Source of Truth (read in this order)
0. Read agent instructions: this file
1. `refactor/refactoring-log.md`
2. `refactor/refactoring-plan.md`
3. `refactor/migration-map.md`
4. `refactor/current-phase-checklist.md`
5. `refactor/refactoring-log.md`
6. Existing docs (architecture, API, data model)

## Resumption Protocol (New Session / New Agent)
If you are starting fresh or picking up from a previous session:
1. Read `refactor/refactoring-log.md` last 3 entries for context
2. Confirm current phase/stage matches log
3. Run `pytest -x` to verify baseline is green
4. Check `git log --oneline -5` to confirm log matches commits
5. Do not re-assess code that was already characterized — trust the log

## Non-Negotiable Constraints
- Constraint 1
- Constraint 2
- Constraint 3

## Current Phase
{Which phase and stage is active.}

## Refactoring Rules
- Rules for how to execute

## Safety Rules
- What validation to run
- When to stop

## Done Criteria
What "complete" looks like.
```

## What to include

| Section | Purpose | Example |
|---------|---------|---------|
| Mission | One-line refactoring goal | "Reduce coupling in app/services/ by splitting god modules and fixing layering violations" |
| Current State | Where we are now (point to log) | "Phase 2 in progress, 3/6 targets done — see refactoring log for metrics" |
| Target State | Measurable end state | "Service files ≤ 200 lines, zero circular dependencies, clean layer separation" |
| Source of Truth | Reading order for refactoring docs | Numbered list of refactor/ files |
| Constraints | Hard rules for refactoring | "Never change behavior — only structure" |
| Current Phase | What to work on now | "Phase 2, Target: app/services/orders.py, Stage 4 (Migrate)" |
| Refactoring Rules | How to work | "One named pattern per PR, run tests after every change" |
| Safety Rules | When to stop | "Halt if any test fails that you can't explain in 5 minutes" |
| Done Criteria | When to stop the project | Phase 2 metrics targets |

## Non-negotiable constraints for refactoring

Every refactoring AGENTS.md must include these constraints:

```markdown
## Non-Negotiable Constraints
- **Never change behavior** — refactoring changes structure, not functionality
- **Tests must pass** — if tests fail and you can't explain why within one change, revert
- **One pattern per PR** — each PR applies exactly one named refactoring pattern
- **No mixed changes** — never combine refactoring with features, bugfixes, or config changes
- **Coverage must not decrease** — if coverage drops, add tests before proceeding
- **Log all discovered bugs** — if you find a bug during refactoring, log it; don't fix it
- **Follow the migration map** — don't make ad-hoc structural decisions
```

## Safety rules for refactoring

```markdown
## Safety
- Run `pytest -x` after every code change
- Run `ruff check app/ && mypy app/` before committing
- If tests fail and the cause isn't obvious: **stop, revert, log the issue**
- If you discover a behavior change is needed: **stop, log it, ask the human**
- If a migration map entry is ambiguous: **stop, ask for clarification**
- Never delete old code until all callers are redirected (strangler fig)
```

## Evolution during a refactoring project

AGENTS.md should be updated as the refactoring progresses:

1. **Before Phase 1**: Mission, current state assessment summary, plan pointers
2. **During Phase 1** (safety net): Update with baseline metrics and test strategy
3. **During Phase 2** (core restructuring): Update current phase/stage, point to active migration map
4. **After each target**: Update current state description to reflect changes made
5. **After completion**: Transition to a standard operational AGENTS.md

## Validation checklist

- [ ] Under 150 lines
- [ ] Mission is one sentence describing the refactoring goal
- [ ] Current state points to refactoring log (not embedded metrics that go stale)
- [ ] Target state describes measurable end state
- [ ] Source of truth lists refactoring-specific documents
- [ ] Constraints include all non-negotiable safety rules
- [ ] Current phase and stage are explicitly stated
- [ ] Every referenced file actually exists
- [ ] Done criteria are objective and measurable
