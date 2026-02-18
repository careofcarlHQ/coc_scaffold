# 06 — Writing AGENTS.md for Migrations

## Purpose

Migration work requires precise agent instructions because mistakes can affect data and infrastructure. The migration brief tells the agent exactly what stage to execute and what the guardrails are.

## Migration brief

Create `migration/AGENTS-BRIEF.md`:

```markdown
# Migration Brief — {Migration Name}

## What we're migrating
{One sentence: from what to what.}

## Current stage
Stage {N} — {name}

## Read these files (in order)
1. `AGENTS.md` (project-level rules)
2. `migration/current-state-snapshot.md` (where we started)
3. `migration/target-state-definition.md` (where we're going)
4. `migration/migration-checklist.md` (all stages, current progress)
5. `migration/rollback-plan.md` (how to undo)

## Non-negotiable constraints
- ALWAYS take a backup before any data-touching stage
- ALWAYS verify rollback works before marking a stage complete
- NEVER combine two migration stages into one operation
- NEVER delete old data/config/code until cleanup phase
- Run the full test suite after every stage
- If ANY verification fails, STOP and report — do NOT proceed

## Stage instructions
{Specific instructions for the current stage — what to do, in what order}

## Rollback for this stage
{Exact rollback steps — the agent must know these before starting}
```

## When to update the brief
- Before each new stage: update "Current stage" and "Stage instructions"
- After each stage: capture evidence in migration-checklist.md
- Only during cleanup: allow deleting old artifacts

## Key differences from other scaffolds

Migration briefs require extra caution compared to feature or refactoring briefs:

| Concern | Migration approach |
|---------|-------------------|
| Backup | Mandatory before data stages (not just recommended) |
| Rollback | Must be verified, not just documented |
| Scope | Strict — never expand a stage mid-execution |
| Monitoring | Check error rates and performance after each stage |
| Timing | Some stages need off-peak execution |
