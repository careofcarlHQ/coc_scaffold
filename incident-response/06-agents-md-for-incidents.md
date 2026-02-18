# 06 — AGENTS.md for Incidents

> How to orient an agent during an active incident. Incident work is unique: it's time-pressured, high-stakes, and requires restraint.

---

## Why AGENTS.md matters for incidents

Incidents are the worst possible time for an agent to be unfocused. An agent without clear constraints during an incident might:
- Try to refactor the broken code instead of just fixing it
- Make speculative changes without understanding the problem
- Edit production configuration without verification
- Attempt a "clean fix" when a simple rollback would resolve it in seconds

The incident AGENTS.md is deliberately narrow. It constrains the agent to the minimum necessary actions.

---

## Incident brief structure

### 1. Incident context

```markdown
## Incident
SEV{N} — {one-line description of what's broken}

## Current phase
{Triage / Mitigation / Diagnosis / Fix}

## Symptoms
- {Symptom 1: e.g., "POST /api/orders returns 500"}
- {Symptom 2: e.g., "Error in logs: KeyError 'discount_code'"}
- {Symptom 3: e.g., "Started at 14:30 UTC after deploy abc123"}

## What NOT to do
- Do NOT refactor code
- Do NOT change code outside the broken path
- Do NOT run database migrations
- Do NOT "improve" anything — find and fix the one problem
```

### 2. Phase-specific instructions

#### During Triage:
```markdown
## Your job
1. Check the last deployment: what changed?
2. Check the error logs: what's the actual exception?
3. Check if the error correlates with the deploy timestamp
4. Report: severity, scope, likely cause
5. Recommend: rollback, hotfix, or investigate further

Do NOT make any changes. Observe and report only.
```

#### During Mitigation:
```markdown
## Your job
1. Execute the mitigation: {rollback deploy / toggle flag / restart service}
2. Verify: does the error stop?
3. If not, try: {fallback mitigation}
4. Report the result

Do NOT try to fix the root cause. Stop the bleeding only.
```

#### During Diagnosis:
```markdown
## Your job
1. Read the incident timeline in incidents/{incident-id}.md
2. Read the deploy diff: {commit range or PR}
3. Form hypotheses about root cause
4. Test each hypothesis with evidence from logs/code
5. Document findings in the incident report

Do NOT write any fix code yet. Confirm root cause first.
```

#### During Fix:
```markdown
## Your job
1. The confirmed root cause is: {root cause}
2. Write a regression test that reproduces the bug
3. Write the minimal fix that addresses the root cause
4. Run the full test suite
5. Prepare the fix for deployment

Rules:
- Fix ONLY the root cause
- Do NOT refactor adjacent code
- Do NOT "improve" while you're here
- The regression test must fail without the fix and pass with it
```

---

## Constraints for incident work

| Constraint | Why |
|-----------|-----|
| Minimal changes only | Every change during an incident carries risk |
| No refactoring | You're here to stop the fire, not redesign the kitchen |
| Write tests for the fix | The same bug should never happen again |
| Verify after every action | Confirm each step worked before proceeding |
| Log everything | The post-mortem depends on accurate records |
| Ask before destructive actions | Don't drop tables, delete data, or modify prod directly |

---

## Template

See `templates/AGENTS.md.template` for a ready-to-fill incident orientation document.
