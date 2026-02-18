# 06 — How to Write an Effective AGENTS.md

## Purpose

AGENTS.md is the first file an AI agent reads when working in your repository. It orients the agent: what is this project, where are the rules, how should work be done.

## Key principle: map, not manual

Keep AGENTS.md under 150 lines. It is a **table of contents** pointing to deeper sources of truth, not a comprehensive instruction manual.

### Why short?

- Agent context windows are finite — a huge AGENTS.md crowds out the actual task
- When everything is "important," the agent can't prioritize
- Large files rot faster and are harder to verify
- Agents work better with progressive disclosure (start small, drill deeper)

## Structure template

```markdown
# AGENTS.md — {project_name}

## Mission
One-sentence description of what this project does.

## Source of Truth (read in this order)
0. Read agent instructions: this file
   `spec/bootstrap-local.md`
1. `spec/PROCESS_INDEX.md`
2. `spec/phase-N-implementation-checklist.md` (current phase)
3. `spec/implementation-architecture.md`
4. `spec/api-contract.md`
5. `spec/data-model.md`
6. ... (additional specs)

## Non-Negotiable Constraints
- Constraint 1
- Constraint 2
- Constraint 3

## Execution Order
Describe what phase/stage is current and the order to follow.

## Required Deliverables Per Stage
- What artifacts must be produced

## Coding Rules
- Minimal, scoped changes
- Testing expectations
- Documentation expectations

## Safety
- Where to find secrets config
- What must never be committed
- When to halt and escalate

## Done Criteria
What "complete" looks like for each phase.
```

## What to include

| Section | Purpose | Example |
|---------|---------|---------|
| Mission | Orient the agent in one line | "Build a Postgres-backed job queue for multi-agent PR flows" |
| Source of Truth | Reading order for specs | Numbered list of spec files |
| Constraints | Hard rules that cannot be violated | "Human approval required before merge" |
| Execution Order | What to work on now | "Phase 2, stages defined in checklist" |
| Deliverables | What each stage must produce | "Code, docs, gate evidence, risk notes" |
| Coding Rules | How to write code in this repo | "Prefer deterministic checks over model calls" |
| Safety | How to handle secrets and risk | "Use .env.local, never commit secrets" |
| Done Criteria | How to know when to stop | Stage 10 acceptance criteria |

## What NOT to include

- Detailed implementation instructions (put in spec files)
- API endpoint documentation (put in api-contract.md)
- Database schema details (put in data-model.md)
- Long code examples (put in engineering best practices)
- Historical decisions or changelog (put in implementation log)

## Evolution

AGENTS.md evolves as the project evolves:

1. **Day 1**: Minimal — mission, constraints, initial spec pointers
2. **Phase 1 complete**: Add execution order, deliverables, done criteria
3. **Phase 2+**: Update current phase, add new specs to source of truth
4. **Operational**: Mostly stable, updated during weekly reviews

## Validation checklist

- [ ] Under 150 lines
- [ ] Mission is one sentence
- [ ] Source of truth is a numbered list
- [ ] Every referenced file actually exists
- [ ] Constraints are rules, not suggestions
- [ ] Done criteria are objective and testable
- [ ] No implementation details that belong in specs
