# 02 — Triage and Severity

> Fast, structured assessment. Get the severity right (enough) and figure out the scope. You can reclassify later.

---

## Severity Levels

### SEV1 — Critical
- **Definition**: Service down or core functionality broken for ALL users
- **Examples**: Site returns 500 for all requests, database unreachable, data corruption in progress
- **Response time**: Immediately — drop everything
- **Target resolution**: < 1 hour to mitigate
- **Communication**: Status page / user notification within 15 minutes

### SEV2 — Major
- **Definition**: Core functionality degraded for a significant portion of users
- **Examples**: Checkout failing for 30% of users, API responses extremely slow, one critical endpoint broken
- **Response time**: Within 15 minutes of detection
- **Target resolution**: < 4 hours to mitigate
- **Communication**: Status page update within 30 minutes

### SEV3 — Minor
- **Definition**: Non-core functionality broken, or core functionality broken for a small subset of users
- **Examples**: Admin dashboard broken, email notifications not sending, edge case causing errors for specific inputs
- **Response time**: Within 1 hour
- **Target resolution**: < 24 hours to fix
- **Communication**: Not typically needed externally

### SEV4 — Low
- **Definition**: Cosmetic issue, minor inconvenience, or degradation with an easy workaround
- **Examples**: Styling broken on one page, non-critical background job failing, minor data inconsistency
- **Response time**: During normal working hours
- **Target resolution**: Within a few days
- **Communication**: None needed

---

## Quick Triage Checklist

Run through this in under 10 minutes:

### 1. What's broken?
- [ ] Which endpoint(s) / page(s) / feature(s)?
- [ ] What error are users seeing?
- [ ] What does the log show?

### 2. How many users affected?
- [ ] All users → likely SEV1
- [ ] Significant portion → likely SEV2
- [ ] Small subset → likely SEV3
- [ ] Edge case → likely SEV4

### 3. What changed recently?
- [ ] Code deployed in last 24h? → check deploy diff
- [ ] Database migration ran? → check migration log
- [ ] Config changed? → check env vars, feature flags
- [ ] Dependency updated? → check lock file changes
- [ ] Infrastructure change? → check platform status
- [ ] Nothing changed? → external factor? data growth? traffic spike?

### 4. Is it getting worse?
- [ ] Error rate increasing → urgent, act now
- [ ] Error rate stable → controlled, can investigate
- [ ] Error rate decreasing → might be self-healing, monitor
- [ ] Data being corrupted → SEV1, stop writes immediately

### 5. What's your mitigation path?
- [ ] Can you rollback? (fastest)
- [ ] Can you toggle a feature flag?
- [ ] Can you restart the service?
- [ ] Can you redirect traffic?
- [ ] Do you need a hotfix?

---

## Scope Assessment

### Service scope

| Question | Status |
|----------|--------|
| Which service(s) affected? | {service list} |
| All endpoints or specific? | {scope} |
| API consumers affected? | {yes/no — which?} |
| Background jobs affected? | {yes/no — which?} |
| Database integrity at risk? | {yes/no} |

### User scope

| Question | Status |
|----------|--------|
| All users or subset? | {scope} |
| Which user segment? | {segment} |
| Any workaround available? | {yes/no — what?} |
| Revenue impact? | {estimate} |

### Temporal scope

| Question | Status |
|----------|--------|
| When did it start? | {timestamp} |
| Correlated with a deploy? | {yes/no — which deploy?} |
| Getting worse over time? | {yes/no} |
| Self-healing expected? | {yes/no — why?} |

---

## Decision: Response Strategy

Based on triage, choose your approach:

| If | Then |
|----|------|
| Recent deploy correlates with incident | **Rollback immediately** |
| Feature flag controls the broken code | **Toggle it off** |
| Service is overloaded | **Scale up / restart** |
| External dependency is down | **Enable fallback mode / circuit breaker** |
| Data is being corrupted | **Stop the process immediately, then investigate** |
| Root cause is already clear | **Write hotfix, deploy with extra verification** |
| Root cause is not clear | **Mitigate (rollback/toggle/scale), then investigate at leisure** |

---

## Reclassification

Severity can change as you learn more. Update the incident report when:

- Scope turns out to be larger than initially thought → escalate
- You discover data corruption → escalate to SEV1
- A workaround is found → may de-escalate
- Only a tiny fraction of users are affected → may de-escalate

Always log reclassification with timestamp and reason.
