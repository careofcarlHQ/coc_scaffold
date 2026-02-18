# 07 — Agent Prompts

> Copy-paste prompts for each phase of incident response. These are designed for urgency — they're shorter and more directive than other scaffold prompts.

---

## Prompt 1: Triage (start here when something breaks)

```
INCIDENT TRIAGE — READ AGENTS.md FIRST.

Something is broken in production. I need your help triaging:

Symptoms:
- {symptom 1}
- {symptom 2}
- {symptom 3}

Do this NOW (observation only, no changes):
1. Check the last deployment: when was it, what changed? (git log --oneline -10)
2. Check the error logs for the exact error message and stack trace
3. Determine: does the error start time correlate with the last deploy?
4. Check: all users affected, or a subset?
5. Check: one endpoint or many?

Report back:
- Severity: SEV1/SEV2/SEV3/SEV4 with justification
- Scope: who/what is affected
- Likely cause: your best hypothesis
- Recommended action: rollback / hotfix / toggle / investigate
```

---

## Prompt 2: Mitigation — Rollback

```
INCIDENT MITIGATION — READ AGENTS.md FIRST.

We need to rollback the last deployment to mitigate a production incident.

1. Identify the current deployed version
2. Identify the previous known-good version
3. Execute the rollback (tell me the exact commands/steps)
4. After rollback, verify:
   - Health check endpoints return 200
   - The specific error from triage is no longer occurring
   - Error rate in logs has dropped

Report: Did the rollback resolve the user-facing issue? Yes/No.
If No, what's the next mitigation option?
```

---

## Prompt 3: Mitigation — Hotfix

```
INCIDENT MITIGATION — READ AGENTS.md FIRST.

A rollback isn't possible (or didn't help). We need a targeted hotfix.

The error is: {exact error message/trace}
Located in: {file and line if known}

Write the MINIMUM change needed to stop the error:
1. Read the code at the error location
2. Understand why it's failing
3. Write the smallest possible fix (defensive coding is fine here)
4. Run tests to make sure the fix doesn't break other things
5. Present the diff for review

Rules:
- ONE problem, ONE fix
- No refactoring
- No improvements
- If you're not confident in the fix, say so
```

---

## Prompt 4: Diagnosis

```
INCIDENT DIAGNOSIS — READ AGENTS.md FIRST.

The incident is mitigated. Users are unblocked. Now find the root cause.

Read: incidents/{incident-id}.md (the incident timeline)

1. Build a complete timeline of events:
   - Last deployment time and what changed
   - First error occurrence
   - Any config/data changes in the window
2. Review the deploy diff commit by commit
3. Form 2-3 hypotheses about root cause
4. For each hypothesis, find supporting or contradicting evidence
5. Confirm one root cause that explains ALL symptoms

Document your findings in the incident report.
Do NOT write any fix code yet.
```

---

## Prompt 5: Fix with Regression Test

```
INCIDENT FIX — READ AGENTS.md FIRST.

Root cause confirmed: {root cause description}

1. Write a regression test that reproduces the bug:
   - The test should FAIL on the current (broken) code
   - Name it: test_{incident_description}_regression
   - Put it in the appropriate test directory
2. Write the fix:
   - Minimal change addressing only the root cause
   - No refactoring, no improvements
3. Verify:
   - The regression test now PASSES
   - The full test suite PASSES
   - No other tests broke
4. Present the complete diff (test + fix) for review

The fix must be deployable as-is.
```

---

## Prompt 6: Post-Mortem Draft

```
Read the incident report at incidents/{incident-id}.md and the mitigation log.

Draft a post-mortem using the template at incident-response/templates/post-mortem.md.template.

Include:
1. Summary (one paragraph)
2. Timeline (from incident report, add any missing events)
3. Root cause (with 5 Whys analysis)
4. Impact (duration, users, data, revenue if applicable)
5. What went well (at least 2 items)
6. What went poorly (be specific and blameless)
7. Action items (specific, assignable, time-bound)

For action items, categorize as:
- Test: missing test that would have caught this
- Monitor: missing alert that would have detected it faster
- Process: missing safeguard that would have prevented it
- Code: defensive improvement to prevent recurrence

Save to incidents/{incident-id}-postmortem.md.
```

---

## Prompt 7: Prevention Implementation

```
Read the post-mortem at incidents/{incident-id}-postmortem.md.

Implement the following action items:
{list the specific action items from the post-mortem}

For each action item:
1. Implement the change (test, monitor, code, process)
2. Verify it works
3. Mark it as done in the post-mortem
4. Explain how this would have prevented or detected the incident

Do NOT bundle unrelated improvements. Only implement what's listed.
```
