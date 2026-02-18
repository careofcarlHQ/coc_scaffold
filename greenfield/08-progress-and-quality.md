# 08 — Progress and Quality

## Purpose

This guide defines how to track progress and quality in a greenfield project so that agent output stays measurable, reviewable, and safe to merge.

Without explicit tracking, greenfield work drifts into "looks done" rather than "is done."

---

## Progress model

Track progress at three levels:

1. **Phase progress** — are we advancing through the planned phases?
2. **Stage progress** — are stage gates passing with evidence?
3. **Task progress** — are individual work items moving from intake to merge?

### Phase dashboard

| Phase | Goal | Status | Gate evidence |
|------|------|--------|---------------|
| Phase 1 | Core backend + data model | {not started / in progress / done} | {link} |
| Phase 2 | Operator UX + hardening | {status} | {link} |
| Phase 3 | Integrations + production polish | {status} | {link} |

### Stage checklist discipline

Each stage in each phase must include:

- [ ] Scope statement
- [ ] Acceptance gate criteria
- [ ] Evidence links (tests, screenshots, logs)
- [ ] Risk notes (what could break)
- [ ] Decision notes (trade-offs made)

If any item is missing, the stage is **not complete**.

---

## Quality gates

Quality is not one final check. It is a gate at every stage.

### Minimum gate per stage

- [ ] Build passes
- [ ] Tests for changed behavior pass
- [ ] Documentation updated for changed contracts
- [ ] Security/policy constraints respected
- [ ] Reviewer can reproduce validation steps

### Phase exit gate

To close a phase, require:

- [ ] All stage gates marked complete
- [ ] No unresolved P0 defects opened during phase
- [ ] Metrics reviewed and acknowledged
- [ ] Carry-over risks documented for next phase

---

## Metrics that matter

Track a small set of operational metrics weekly:

| Metric | Why it matters |
|--------|----------------|
| Lead time (intake → merge) | Detects workflow friction |
| Validation pass rate | Detects unstable implementation quality |
| Rework rate | Detects poor specs or unclear acceptance criteria |
| Escalation frequency | Detects uncertainty and policy pressure points |
| Defect escape rate | Detects weak stage gates |

Avoid vanity metrics (e.g., PR count, raw lines changed).

---

## Quality review cadence

Run a short weekly quality review:

1. Inspect failed validations and categorize causes
2. Review escalations and identify recurring ambiguity
3. Review escaped defects and map them to missing gates
4. Tighten templates, prompts, or acceptance criteria
5. Record one process improvement for next week

This is the loop that turns a scaffold into a living system.

---

## Signals your process is healthy

- Most tasks clear on first or second pass
- Escalations are specific and actionable
- Stage evidence is complete without ad-hoc chasing
- Defects are found before merge, not after
- Process docs improve over time from real usage

If these signals degrade, treat process drift as a production issue.
