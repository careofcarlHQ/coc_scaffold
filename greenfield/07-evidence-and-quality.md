# 07 — Evidence and Quality

## Why evidence matters

In agent-first development, code changes are cheap and fast. The bottleneck is **human review and approval**. Structured evidence makes human review fast and reliable — the reviewer sees a checklist and key artifacts, not raw diffs.

## Evidence package structure

Every completed task should produce a dual-format evidence package:

### A) Compact checklist (for fast approval)

```markdown
- [ ] Task contract linked
- [ ] Acceptance criteria all mapped to changes
- [ ] Reviewer approved
- [ ] Validator evidence attached
- [ ] CI green
- [ ] Escalations resolved or not applicable
- [ ] Rollback documented

### Snapshot
- Task ID: {id}
- Repo: {repo}
- Change class: {class}
- Risk tier: {tier}
```

### B) Detailed evidence (for deep review when needed)

1. **Task contract** — objective, constraints, acceptance criteria
2. **Changed-file map** — each file, why it changed, which AC it maps to
3. **Validation commands and results** — command, purpose, pass/fail, output
4. **Reviewer report** — decision, findings, fixes applied
5. **Validator report** — build, lint, test results
6. **Risk and rollback** — primary risk, blast radius, rollback steps
7. **Escalation log** — triggers, context, resolution
8. **Open questions** — unresolved items for follow-up
9. **Merge recommendation** — merge or hold, with reasoning

## Quality tracking

### Metrics scoreboard (weekly)

Track these metrics weekly to measure process health:

**Delivery:**
- Tasks completed
- Median lead time (intent → done)
- No-manual-edit rate (%)

**Quality:**
- CI pass rate at completion (%)
- Post-completion regressions
- Reverts or hotfixes

**Escalations:**
- Total escalations
- By type (security, data, API, cost)
- Average resolution time

**Process compliance:**
- Tasks with complete evidence (%)
- Tasks with acceptance criteria coverage (%)
- Gate violations

### Trend analysis

Look for:
- **Improving lead times** → process is working, agents are effective
- **Increasing escalations** → specs may be unclear, add more guidance
- **Declining CI pass rates** → tests may be insufficient, add coverage
- **Rising manual edit rate** → agent output quality declining, review prompts/specs

## Task intake quality

The quality of output is directly proportional to the quality of intake. A good task intake includes:

| Field | Purpose | Bad example | Good example |
|-------|---------|-------------|--------------|
| Problem statement | What to solve | "Fix the API" | "POST /tasks returns 500 when task_id contains special characters" |
| Acceptance criteria | How to verify | "It should work" | "POST /tasks with task_id 'test-123' returns 201" |
| Risk tier | How careful to be | (omitted) | "medium — touches state machine transitions" |
| Change class | What kind of change | (omitted) | "bugfix" |
| Constraints | What not to do | (omitted) | "Do not change the database schema" |

## Escalation records

When escalation is required, capture structured information:

```markdown
- Trigger type: security / data-model / external-api / cost
- Context: What was being done when the trigger fired
- Current assumption: What the agent assumed
- Impact if wrong: What breaks if the assumption is incorrect
- Options considered: What alternatives exist
- Recommended option: Agent's recommendation
- Decision owner: Who decides
- Decision status: pending / approved / rejected
```

## Definition of done for a task

A task is done only when:
1. All acceptance criteria are covered by changes
2. Evidence package is complete (both formats)
3. Reviewer decision is captured
4. Validation evidence is reproducible
5. Risk and rollback are documented
6. All escalations are resolved
7. Human approval is granted (if required)
