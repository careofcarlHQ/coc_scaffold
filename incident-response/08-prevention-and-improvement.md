# 08 — Prevention and Improvement

> An incident is only valuable if it makes the system stronger. This guide ensures every incident results in concrete improvements.

---

## The Prevention Loop

```
Incident → Post-Mortem → Action Items → Implementation → Verification
                                              ↓
                                    Reduced future incidents
```

Every incident should result in at least one of:
- A new test that would have caught it
- A new monitor/alert that would have detected it faster
- A code change that makes it impossible to recur
- A process change that adds a safety check

---

## Action Item Categories

### Tests (most common, most valuable)

| What | Example |
|------|---------|
| Regression test | Test that reproduces the exact bug |
| Characterization test | Lock behavior of related code |
| Integration test | Cover the full path that broke |
| Edge case test | Cover the specific input that triggered the bug |

**Goal**: Make the CI pipeline catch this before it reaches production.

### Monitoring & Alerts

| What | Example |
|------|---------|
| Error rate alert | Alert when error rate exceeds 2x baseline |
| Endpoint monitoring | Health check for the specific endpoint that broke |
| Log alert | Alert on specific error message patterns |
| Performance alert | Alert when response time exceeds threshold |

**Goal**: Detect the *next* similar incident in seconds, not minutes or hours.

### Code Improvements

| What | Example |
|------|---------|
| Input validation | Validate data before processing |
| Error handling | Handle the specific error case gracefully |
| Circuit breaker | Fail fast when dependency is down |
| Defensive coding | Check assumptions explicitly |
| Feature flags | Wrap risky code in toggles for easy rollback |

**Goal**: Make the code resilient to the failure mode.

### Process Improvements

| What | Example |
|------|---------|
| Pre-deploy checklist | Check for migration compatibility |
| Deploy verification | Automated post-deploy health check |
| Runbook update | Add procedure for this incident type |
| Review gate | Add review requirement for high-risk changes |

**Goal**: Add friction at the points where mistakes were made.

---

## Tracking Action Items

### The prevention backlog

Maintain a single document (`incidents/prevention-backlog.md`) that tracks ALL action items from ALL incidents:

| # | Incident | Action | Category | Priority | Status | Due | Done |
|---|----------|--------|----------|----------|--------|-----|------|
| 1 | INC-001 | Add test for /api/orders | Test | P1 | Done | Jan 20 | Jan 18 |
| 2 | INC-001 | Add error rate alert | Monitor | P2 | Todo | Jan 25 | — |
| 3 | INC-002 | Add input validation | Code | P1 | In progress | Feb 1 | — |

### Follow-up cadence

| Check | Frequency | Action |
|-------|-----------|--------|
| New action items assigned | After every post-mortem | Add to prevention backlog |
| Action item progress | Weekly | Review the backlog, update status |
| Stale action items | Bi-weekly | Escalate any item older than 2 weeks |
| Pattern review | Monthly | Look for patterns across incidents |

---

## Pattern Recognition

After multiple incidents, look for systemic patterns:

### Same module keeps breaking
→ The module needs a comprehensive test retrofit. Use the **testing-retrofit** scaffold.

### Same type of error recurs (different modules)
→ There's a systemic gap — maybe validation, error handling, or test coverage across the codebase.

### Incidents correlate with deploys
→ The deployment pipeline needs better gates — tests, canary deploys, health checks.

### Incidents correlate with data changes
→ Need data validation, schema constraints, or migration testing.

### Detection is always slow
→ Monitoring and alerting gaps. Invest in observability.

---

## Incident Metrics

Track these over time to measure whether you're getting better:

### Leading indicators (predictive)

| Metric | Description | Good trend |
|--------|------------|-----------|
| Action items completed | % of post-mortem actions done | → 100% |
| Time to complete actions | Days from post-mortem to done | → Shorter |
| Test coverage of incident-prone code | Coverage of modules that had incidents | → Higher |
| Monitoring coverage | % of critical paths with alerts | → Higher |

### Lagging indicators (measuring results)

| Metric | Description | Good trend |
|--------|------------|-----------|
| Incident count | Total incidents per month | → Fewer |
| Repeat incidents | Same root cause recurring | → Zero |
| Time to detect | Minutes from incident start to alert | → Shorter |
| Time to mitigate | Minutes from detection to user impact resolved | → Shorter |
| Time to fix | Hours from detection to root cause fix deployed | → Shorter |

---

## The Virtuous Cycle

The goal is to create a virtuous cycle:

```
Incident happens
    → Post-mortem written (within 48h)
        → Action items created (specific, time-bound)
            → Actions implemented (within 2 weeks)
                → Monitoring improved (catch it faster next time)
                → Tests added (catch it before deploy next time)
                → Code hardened (prevent it from being possible)
                    → Fewer incidents
                    → Faster detection
                    → Faster mitigation
```

Each incident makes the system a little bit more resilient. Over time, the serious incidents become rare, the minor ones get caught before users notice, and the system earns the trust it deserves.
