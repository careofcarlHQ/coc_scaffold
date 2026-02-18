# 00 — Philosophy: Systematic Bug Investigation

## The core insight

Debugging is the most common activity that agents do poorly at — not because they lack ability, but because they lack structure. Without a systematic approach, agents (and humans) cycle through random guesses, re-investigate dead ends, and fix symptoms instead of root causes.

The solution is the same as for every other engineering activity: **give the agent a process**.

## Principles

### 1. Symptoms are not causes

The visible error is rarely the actual problem. A 500 error might be caused by a None value, which was caused by a missing database row, which was caused by a race condition in the job processor. Fixing the None check masks the real bug.

Always ask: "Why does this condition exist in the first place?"

### 2. Reproduce before you diagnose

If you can't reproduce the bug, you can't verify the fix. Reproduction is not optional — it's the foundation of everything that follows.

Rules:
- Find the minimal steps that trigger the bug
- Document the exact environment (Python version, database state, config)
- Make reproduction deterministic (same input → same bug, every time)
- If you can't reproduce, you're missing context — investigate further before diagnosing

### 3. Hypothesis-driven investigation

Never "just look around" — formulate explicit hypotheses and test them:

```
Hypothesis: "The 500 error occurs because user_id is None when the session expires"
Test: "Add logging before the failing line. Trigger the bug. Check if user_id is None."
Result: "Confirmed — user_id is None. But why?"

Hypothesis: "user_id is None because the auth middleware doesn't set it for expired sessions"
Test: "Read the auth middleware. Check the expired session path."
Result: "Confirmed — expired sessions return early without setting user_id."
```

This prevents circular investigation and documents the path to the answer.

### 4. Log your dead ends

Dead ends are valuable — they narrow the search space. A future investigator (human or agent) should not re-explore paths already ruled out.

```markdown
### Dead end: database connection pool exhaustion
- Hypothesis: 500 errors caused by connection pool running out
- Test: Checked pool stats during error window
- Result: Pool was at 3/20 connections. Not the cause.
- Time spent: 15 minutes
```

### 5. Fix the root cause, not the symptom

```python
# ❌ Symptom fix — masks the real bug
if user_id is None:
    return default_user  # Why is user_id None?

# ✅ Root cause fix
# Fix the auth middleware to properly handle expired sessions
if session.is_expired:
    raise AuthenticationError("Session expired")
```

Sometimes a symptom fix is appropriate as an immediate mitigation, but it must be accompanied by a root cause fix.

### 6. Every fix requires a regression guard

A fix without a test is a fix that will break again. The regression test should:
- Reproduce the exact conditions that caused the bug
- Fail before the fix is applied
- Pass after the fix is applied
- Be specific enough that unrelated changes don't affect it

### 7. Scope the fix narrowly

The fix should change as little as possible. Resist the urge to "clean up while I'm here" — that's refactoring, not bug fixing. Mixed-purpose changes are harder to revert and harder to verify.

### 8. Time-box investigation

Set a time limit before starting. If you haven't found the root cause within the time box:
- Document what you've learned
- Document what you've ruled out
- Escalate or take a break
- Return with fresh eyes (or a fresh agent session)

Suggested time boxes:
- Simple bugs: 30 minutes
- Medium bugs: 2 hours
- Complex bugs: 4 hours, then reassess

### 9. Bugs cluster

Fix one bug and look for siblings. If a race condition exists in one job handler, it probably exists in others. If a None check is missing in one endpoint, check similar endpoints.

### 10. Prevention over repetition

After fixing a bug, ask: "What systemic change would have prevented this class of bug?"

Possible answers:
- A linter rule
- A type annotation
- A test pattern applied more broadly
- A code review checklist item
- An architectural change (move logic to a safer location)

Feed prevention items into your testing-retrofit or refactoring scaffolds.

---

## Lessons from debugging coc_capi

### What worked

1. **Hypothesis logs** — writing "I think X because Y" before investigating X prevented going in circles and created a traceable record.

2. **Minimal reproduction** — stripping away everything except the trigger conditions made root cause obvious in most cases.

3. **Dead-end documentation** — returning to a bug after a break was fast because previous investigation was captured.

4. **Agent-driven code search** — agents excel at tracing call chains, finding all callers, and checking for similar patterns across the codebase.

### What burned time

1. **Investigating without reproduction** — trying to fix bugs that couldn't be reliably triggered led to speculative fixes that didn't actually work.

2. **Symptom fixes without root cause analysis** — quick patches that masked the real problem, only for it to surface differently later.

3. **Not time-boxing** — spending 6 hours on a bug that a fresh pair of eyes (or a fresh agent session) solved in 20 minutes.
