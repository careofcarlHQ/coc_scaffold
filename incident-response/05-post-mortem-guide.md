# 05 — Post-Mortem Guide

> The post-mortem is where incidents become investments. A good post-mortem ensures you never have the same incident twice. A bad one (or none) guarantees you will.

---

## When to Write a Post-Mortem

**Always** for SEV1 and SEV2 incidents.
**Recommended** for SEV3 incidents that reveal systemic issues.
**Optional** for SEV4 incidents, unless there's a pattern.

**When**: Within 48 hours of resolution. Memories fade faster than you think.

---

## Post-Mortem Structure

### 1. Summary

One paragraph: what happened, when, how bad, how it was resolved.

> On {date} at {time}, {service} experienced {symptom} for approximately {duration}, affecting {scope}. The root cause was {root cause}. The incident was mitigated by {mitigation} and permanently fixed by {fix}.

### 2. Timeline

Precise, timestamped sequence of events:

```
HH:MM — {Event: deploy completed / first error logged / alert fired}
HH:MM — {Event: triage started / severity classified as SEVN}
HH:MM — {Event: mitigation attempted — {what}}
HH:MM — {Event: mitigation confirmed working}
HH:MM — {Event: root cause identified}
HH:MM — {Event: fix deployed}
HH:MM — {Event: verification complete, incident closed}
```

Include:
- When the problem actually started (may differ from when it was detected)
- Detection lag: how long between start and detection
- Time to mitigate: how long from detection to user impact resolved
- Time to fix: how long from detection to permanent fix deployed

### 3. Root Cause

**What**: The specific technical cause.
**Why**: The chain of events that led to it.
**How**: The mechanism by which it caused user impact.

Use the "5 Whys" technique:
1. Why did the service return 500 errors? → Because the database query failed
2. Why did the database query fail? → Because a column was renamed in the migration
3. Why didn't we catch this before deploy? → Because we don't have integration tests for that endpoint
4. Why don't we have integration tests? → Because testing was never retrofitted for this module
5. Why wasn't it retrofitted? → Because we didn't prioritize it (it's our most critical endpoint)

### 4. Impact

| Dimension | Impact |
|-----------|--------|
| Duration | {total time of user impact} |
| Users affected | {count or percentage} |
| Requests failed | {count if known} |
| Data impact | {none / corrupted records / lost data} |
| Revenue impact | {estimate if applicable} |
| Trust impact | {description} |

### 5. What went well

Be specific. This reinforces good practices.

- {e.g., "Monitoring detected the error spike within 3 minutes"}
- {e.g., "Rollback was executed in under 5 minutes"}
- {e.g., "Incident report was kept up-to-date in real time"}

### 6. What went poorly

Be specific and blameless. Focus on systems and processes, not people.

- {e.g., "No test existed for the affected endpoint"}
- {e.g., "Took 20 minutes to find the correct rollback procedure"}
- {e.g., "No monitoring alert for this specific error type"}

### 7. Action Items

Every action item must be:
- **Specific**: not "improve testing" but "add integration test for /api/orders endpoint"
- **Assignable**: who will do it (even if it's just "me")
- **Measurable**: how will you know it's done?
- **Time-bound**: by when?

| # | Action | Type | Priority | Due | Status |
|---|--------|------|----------|-----|--------|
| 1 | {action} | {test / monitor / process / code} | {P1/P2/P3} | {date} | {todo/done} |
| 2 | {action} | {type} | {priority} | {date} | {status} |

---

## Post-Mortem Anti-Patterns

| Anti-pattern | Why it's bad | Instead |
|-------------|-------------|---------|
| "Human error" as root cause | Blames people, prevents systemic improvement | "The system allowed X without safeguard Y" |
| Vague action items | Never get done | "Add test for X" not "improve testing" |
| No timeline | Can't learn timing lessons | Reconstruct from logs even if painful |
| Skip "what went well" | Miss reinforcing good practices | Always include at least 2 positives |
| Action items with no owner | Nobody does them | Assign everything, even to yourself |
| Never following up | The same incident recurs | Track action items to completion |
| Writing it a week later | Details forgotten, lessons diluted | Within 48 hours, no exceptions |

---

## Blameless Post-Mortem Culture

Even as a solo developer, practice blameless thinking:

- **Instead of**: "I was stupid and forgot to test" → **Write**: "The deployment pipeline has no test gate for this endpoint"
- **Instead of**: "I should have noticed" → **Write**: "There's no monitoring alert for this failure mode"
- **Instead of**: "I knew this was risky" → **Write**: "Known risk was not mitigated with a safeguard"

The shift from person-blame to system-blame is what turns incidents into improvements. Every "I should have..." translates to a system improvement that *makes it impossible to have the same failure*.
