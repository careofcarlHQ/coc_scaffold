# 01 — Process Overview

> From alert to prevention, in controlled steps — even when everything feels urgent.

---

## The Incident Response Lifecycle

```
Alert → Triage → Mitigate → Diagnose → Fix → Post-Mortem → Prevention
  │        │        │          │         │        │            │
Detect   Classify  Stop the   Find     Deploy   Document     Make it
the      severity  bleeding   root     proper   and learn    impossible
problem  & scope              cause    fix                   to recur
```

The first three phases happen under time pressure. The last four happen after the immediate crisis is resolved. Don't skip either group.

---

## Phase 1: Alert & Capture

**Goal**: Recognize the incident and start the record.

**Activities**:
- Notice the problem (monitoring alert, user report, error log, your own observation)
- Open the incident report document immediately
- Record: what's happening, when it started, how you found out
- Record the current state: error messages, status codes, affected endpoints

**Output**: Initial incident report with symptoms documented.

**Time**: 5 minutes. Don't research yet — just capture what you see.

---

## Phase 2: Triage

**Goal**: Determine severity and scope — how bad is it, who's affected?

**Activities**:
- Classify severity (SEV1/SEV2/SEV3/SEV4)
- Determine scope: all users? some users? one endpoint? all endpoints?
- Check recent deployments: did anything change recently?
- Check recent changes: database migrations, config changes, dependency updates
- Decide response strategy: rollback? hotfix? toggle? wait?

**Output**: Severity classification, scope assessment, initial response direction.

**Time**: 10 minutes. Fast and decisive — you can reclassify later if new info emerges.

---

## Phase 3: Mitigate

**Goal**: Stop the user-facing impact as fast as possible.

**Activities**:
- Execute the mitigation strategy chosen in triage
- Common mitigations: rollback deploy, disable feature flag, restart service, scale up, redirect traffic
- Verify mitigation: are users back to working?
- If first mitigation didn't work, try the next option
- Log every action and result in the mitigation log

**Output**: User impact stopped or significantly reduced. Mitigation log filled.

**Time**: As fast as possible. Minutes, not hours.

**Critical rule**: Mitigation is *not* a fix. You're applying a tourniquet, not performing surgery. A mitigation that rolls back to yesterday's code is perfectly fine.

---

## Phase 4: Diagnose

**Goal**: Find the root cause. Now that users aren't suffering, take the time to understand.

**Activities**:
- Review the timeline: what changed when?
- Check logs, error traces, monitoring dashboards
- Form hypotheses about the root cause
- Test hypotheses methodically
- Identify the chain of events: trigger → mechanism → impact

**Output**: Root cause identified and documented.

**Time**: Hours if needed. Thoroughness matters here.

---

## Phase 5: Fix

**Goal**: Deploy a proper fix for the root cause.

**Activities**:
- Write the fix (not a workaround — the actual fix)
- Write a regression test that would have caught this
- Test the fix locally and in staging
- Deploy the fix
- Verify the fix: remove the mitigation (if applicable), confirm everything works
- Monitor for 24 hours

**Output**: Proper fix deployed, regression test in place.

---

## Phase 6: Post-Mortem

**Goal**: Document what happened, why, and what you're going to do about it.

**Activities**:
- Write the timeline (using your incident report and mitigation log)
- Document root cause and contributing factors
- Identify what went well (fast detection? good mitigation?)
- Identify what went poorly (slow response? missing monitoring?)
- Write action items: specific, assignable, measurable

**Output**: Post-mortem document with timeline, root cause, and action items.

**Time**: Within 48 hours of resolution. Memories fade fast.

---

## Phase 7: Prevention

**Goal**: Turn the incident into lasting improvement.

**Activities**:
- Implement action items from the post-mortem
- Add monitoring that would have detected this faster
- Add tests that would have prevented this
- Update runbooks if applicable
- Review similar systems for the same vulnerability
- Close the loop: mark action items done, verify they work

**Output**: Monitoring, tests, and process improvements implemented.

**Time**: Within 2 weeks. Action items that aren't done within 2 weeks tend to never get done.

---

## Special case: Solo developer incidents

As a solo agent-first developer, some traditional incident response rituals don't apply (no war room, no paging). But the core structure still helps:

1. **Don't panic** — the structure gives you steps to follow
2. **Write it down** — your incident report is your thinking partner
3. **Mitigate first** — resist the urge to debug for an hour while users wait
4. **Take a break before the post-mortem** — you need fresh eyes
5. **Be honest in the post-mortem** — there's no one to impress or blame
