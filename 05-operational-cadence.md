# 05 — Operational Cadence

## Weekly review cycle

Once the system is running, maintain quality through a weekly review cycle. This was a core part of the `coc_agent_process` methodology — without it, specs drift from reality and agent output quality degrades.

### Step 1: Process Health Review (15 min)

Collect metrics:
- Work completed (PRs, tasks, features)
- Lead time (intent → completed)
- Escalation count by type
- Manual intervention rate
- Build/test pass rates

Use the metrics scoreboard template to track week-over-week trends.

### Step 2: Drift and Hygiene Pass (30 min)

Check for:
- Documentation that no longer matches code behavior
- Repeated anti-patterns in agent-generated code
- Missing tests or weak evidence packaging
- Stale spec sections
- Unused or dead code

For each issue found:
- Open a small fix task
- Or update the relevant spec/AGENTS.md section

### Step 3: Escalation Pattern Analysis (15 min)

For each escalation in the past week:
- Was it appropriate? (Should it have been a rule instead?)
- Could the ambiguity be codified? (Add to spec or checklist)
- Should we add a new invariant or gate?

The goal: reduce escalations by encoding resolutions into the system.

### Step 4: Process Tuning (15 min)

Based on the week's data, update any of:
- Agent prompts or AGENTS.md
- Checklists and acceptance gates
- Merge gates or escalation criteria
- Evidence templates
- Engineering best practices

### Step 5: Decision Log (5 min)

Record:
- What changed in process this week
- Why it changed
- Expected impact
- Owner

### Exit criteria

The weekly review is complete when:
- [ ] Metrics scoreboard updated
- [ ] Improvement actions identified and assigned
- [ ] Next week focus defined

---

## Monthly review

Once per month, do a deeper review:

1. **Metric trends** — are lead times improving? Are escalations decreasing?
2. **Spec freshness** — read each spec and verify it still matches reality
3. **Agent effectiveness** — are agents producing higher quality output over time?
4. **Process overhead** — is the scaffold adding value or just bureaucracy? Simplify where needed.
5. **Phase planning** — define or refine the next phase based on current gaps

---

## Continuous improvement principles

### Encode once, enforce forever

When you discover a pattern (good or bad), don't just fix the instance — encode the rule:

- **Good pattern** → add to engineering best practices or AGENTS.md
- **Bad pattern** → add detection to checklists or acceptance gates
- **Recurring question** → add to spec, reducing future ambiguity

### Small improvements compound

A 2% improvement per week compounds to 2.8x improvement per year. Prioritize:
1. Changes that eliminate entire classes of errors
2. Changes that reduce human intervention frequency
3. Changes that make specs clearer for agents
4. Changes that speed up feedback loops

### When to break the process

This scaffold is a tool, not a religion. Skip or simplify when:
- The task is genuinely trivial (< 30 minutes total)
- You're prototyping and will discard the result
- The urgency of a production fix outweighs process rigor

But always: retroactively apply the process after the fire is out. Add the missing spec, the missing test, the missing gate.
