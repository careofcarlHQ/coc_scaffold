# 04 — Diagnosis and Fix

> The incident is mitigated. Users are unblocked. Now take the time to understand what actually happened, and fix it properly.

---

## Diagnosis Workflow

### Step 1: Build the timeline

Before forming hypotheses, reconstruct exactly what happened:

```
{timestamp} — {event}
{timestamp} — {event}
{timestamp} — {event}
```

Sources for timeline data:
- Deployment history (when was code last deployed?)
- Git log (what changed in the last deploy?)
- Application logs (first error occurrence)
- Monitoring dashboards (when did metrics shift?)
- Database migration history (any recent migrations?)
- Config change log (env vars, feature flags)
- Infrastructure events (platform status, scaling events)

### Step 2: Identify the change

Most incidents are caused by a change. Find it:

| Change type | How to check |
|------------|-------------|
| Code deployment | Deployment dashboard, git log |
| Database migration | Alembic/migration history |
| Configuration change | Env var diff, feature flag log |
| Dependency update | Lock file diff |
| Infrastructure change | Platform dashboard, scaling events |
| Traffic pattern change | Request metrics, geographic distribution |
| Data growth | Table sizes, query performance |
| External service change | Third-party status pages |

### Step 3: Form hypotheses

Based on the timeline and changes, form specific hypotheses:

```
Hypothesis 1: The deploy at {time} introduced a bug in {module} that causes
{error} when {condition}. Evidence: {what supports this}.

Hypothesis 2: ...
```

### Step 4: Test hypotheses

For each hypothesis, design a quick test:

| Hypothesis | Test | Result | Verdict |
|-----------|------|--------|---------|
| Deploy bug in module X | Read the diff, look for the change | {finding} | confirmed / rejected |
| Database migration broke Y | Check migration, test table schema | {finding} | confirmed / rejected |
| Config change broke Z | Compare old and new config | {finding} | confirmed / rejected |

### Step 5: Confirm root cause

A root cause explanation must satisfy:
1. **It explains all the symptoms** — not just some of them
2. **The timeline fits** — the cause precedes the effect
3. **It's reproducible** (ideally) — you can trigger it in a test environment
4. **It has a mechanism** — you understand *how* it caused the failure, not just *that* it did

---

## Common Root Cause Patterns

| Pattern | Signs | Example |
|---------|-------|---------|
| **Deploy regression** | Incident starts right after deploy | New code path raises unhandled exception |
| **Migration break** | Incident starts after migration | Column removed that old code still references |
| **Config drift** | Works in staging, fails in prod | Missing env var or wrong value in production |
| **Data edge case** | Affects specific records | New data pattern that code doesn't handle |
| **Dependency break** | Updated library behaves differently | API change in new version of dependency |
| **Resource exhaustion** | Slow degradation over time | Memory leak, connection pool drain, disk full |
| **Race condition** | Intermittent, hard to reproduce | Concurrent requests corrupt shared state |
| **External dependency** | You didn't change anything | Third-party API changed behavior or went down |

---

## Writing the Fix

### Fix quality checklist

Before writing any code:

- [ ] Root cause confirmed (not just correlated)
- [ ] Fix addresses root cause (not just the symptom)
- [ ] Fix is minimal — changes only what's necessary
- [ ] Fix includes a regression test

### The fix process

1. **Write the regression test first** — a test that fails today and will pass after the fix
2. **Write the fix** — minimal, surgical change
3. **Run the full test suite** — no regressions
4. **Test in a staging/preview environment** if available
5. **Deploy the fix**
6. **Remove the mitigation** (if applicable — e.g., re-enable the feature flag, reroute traffic)
7. **Verify in production** — the original incident no longer occurs
8. **Monitor for 24 hours** — watch error rates, performance, user reports

### Fix review questions

| Question | Answer |
|----------|--------|
| Does the fix address the root cause? | {yes/no} |
| Is the fix minimal and scoped? | {yes/no} |
| Does the regression test reproduce the bug? | {yes/no} |
| Does the regression test pass after the fix? | {yes/no} |
| Full test suite passes? | {yes/no} |
| Tested in staging? | {yes/no/na} |
| Ready to deploy? | {yes/no} |

---

## Verification After Fix

### Immediate verification (first hour)

- [ ] Affected endpoint returns expected response
- [ ] Error rate at or below pre-incident baseline
- [ ] Response times normal
- [ ] No new error types in logs
- [ ] Mitigation removed (if applicable)

### Extended verification (24 hours)

- [ ] No recurrence of the incident
- [ ] No new, related issues discovered
- [ ] Performance metrics stable
- [ ] User reports normal

### Regression test verification

- [ ] The regression test *fails* when the fix is reverted
- [ ] The regression test *passes* with the fix applied
- [ ] The regression test is included in the CI suite

---

## When diagnosis is hard

If you can't find the root cause after methodical investigation:

1. **Check if the mitigation is actually working** — sometimes what you think fixed it isn't the real fix
2. **Broaden the search** — look at infrastructure, not just code
3. **Look for multiple causes** — two unrelated small problems can combine into one big incident
4. **Try to reproduce in staging** — can you trigger the same error?
5. **Bring in fresh eyes** — explain the problem from scratch (rubber duck debugging with an agent works)
6. **Accept partial understanding** — if you can prevent it with monitoring + tests, that's acceptable temporarily
