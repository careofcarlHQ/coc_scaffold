# 04 — Diagnosis Workflow

## Purpose

Diagnosis bridges isolation (where the bug is) to the fix (what to change). The key tool is the **hypothesis log** — a structured record of theories tested and results observed.

## The hypothesis loop

```
Observe → Hypothesize → Test → Record → Repeat (or conclude)
```

### 1. Observe

Look at the isolated code and data. What do you see?

```markdown
## Observation
export.storage_key is None at services/export.py:45
This causes a TypeError when trying to call .replace() on None
```

### 2. Hypothesize

Form a testable theory about WHY the observation exists.

A good hypothesis has:
- A specific claim: "X is true"
- A reason: "because Y"
- A test: "if I check Z, the claim is confirmed/refuted"

```markdown
## Hypothesis 1
**Claim**: storage_key is None because the export was created before the column was added
**Reason**: The migration adding storage_key didn't backfill existing rows
**Test**: Check created_at for export 123 vs. migration timestamp
```

### 3. Test

Execute the test. Don't skip this — opinions are not evidence.

```markdown
## Test result
Export 123 created_at: 2026-02-10
Migration 20260215_add_storage_key: applied 2026-02-15
→ Confirmed: export pre-dates the storage_key column
```

### 4. Record

Document the result whether the hypothesis was confirmed or rejected.

### 5. Repeat or conclude

If confirmed: trace deeper. "Why didn't the migration backfill?"
If rejected: form a new hypothesis based on what you learned.

---

## The hypothesis log

Keep a running log during investigation. This is the most valuable debugging artifact.

```markdown
# Hypothesis Log — [Bug Title]

## H1: storage_key NULL because export pre-dates migration
- Test: Compare export.created_at vs migration date
- Result: ✅ Confirmed — export created 5 days before migration
- Duration: 5 minutes
- Next: Why didn't migration backfill?

## H2: Migration didn't backfill because it was ALTER TABLE ADD COLUMN only
- Test: Read migration file 20260215_add_storage_key.py
- Result: ✅ Confirmed — migration adds nullable column with no UPDATE
- Duration: 2 minutes
- Next: Why does the service assume storage_key is always set?

## H3: Service assumes storage_key is set because it was written after migration
- Test: Check git blame for services/export.py:45
- Result: ✅ Confirmed — function was written in same PR as migration
- Duration: 1 minute
- → ROOT CAUSE IDENTIFIED

## Root cause chain:
Migration adds nullable column → Existing rows get NULL →
Service written assuming column always populated → TypeError on old exports
```

---

## Diagnosis patterns

### Pattern 1: Missing guard

**Symptom**: AttributeError, TypeError, or KeyError on None/missing data
**Root cause usually**: Code assumes data is always present, but some code path doesn't provide it
**Diagnosis**: Trace back from the error to find which code path produces the None/missing value

### Pattern 2: Race condition

**Symptom**: Intermittent failures, works "most of the time"
**Root cause usually**: Two concurrent operations interfere with each other
**Diagnosis**: Look for shared mutable state, database transactions without proper isolation, or time-of-check-to-time-of-use gaps

### Pattern 3: State machine violation

**Symptom**: Object in an "impossible" state, constraint violation errors
**Root cause usually**: Code path that bypasses the state machine (direct DB update, missing validation)
**Diagnosis**: Trace all code that modifies the object's state, find the path that skips validation

### Pattern 4: Environment mismatch

**Symptom**: Works locally, fails in production (or vice versa)
**Root cause usually**: Different configuration, different data, different timing
**Diagnosis**: Diff the environments systematically (config, versions, data, external services)

### Pattern 5: Data migration gap

**Symptom**: Errors only on "old" data, new data works fine
**Root cause usually**: Schema change without data backfill
**Diagnosis**: Compare affected records to unaffected records, check migration history

### Pattern 6: External service failure

**Symptom**: Errors correlate with external service status
**Root cause usually**: External API changed, credentials expired, rate limit hit
**Diagnosis**: Check external service status, review API response, check credentials

---

## When to stop diagnosing

Stop when you can answer ALL of these:

1. **What is the root cause?** (not the symptom — the underlying reason)
2. **What is the causal chain?** (root cause → intermediate effects → visible symptom)
3. **What data/conditions trigger it?** (reproduction conditions)
4. **What is the scope?** (how many users/records are affected)
5. **Are there sibling bugs?** (same pattern elsewhere in the codebase)

If you can't answer all five, keep investigating.

---

## When to escalate

Escalate (ask for help, take a break, start fresh) when:

- You've exceeded your time box
- You have more than 5 rejected hypotheses and no new leads
- The root cause involves code you don't understand
- The bug requires production access or data you can't reach
- Multiple hypotheses are equally plausible and you can't distinguish them
