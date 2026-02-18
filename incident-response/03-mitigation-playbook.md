# 03 — Mitigation Playbook

> Stop the bleeding first. This playbook covers the most common mitigation patterns. Pick the one that applies, execute it, verify it worked.

---

## Mitigation Decision Tree

```
Is there a recent deploy?
├── Yes → Rollback the deploy
│         Did rollback fix it?
│         ├── Yes → Done (mitigated). Now diagnose.
│         └── No → Continue down the tree
└── No
    Is a feature flag involved?
    ├── Yes → Toggle the flag off
    │         Did toggling fix it?
    │         ├── Yes → Done (mitigated). Now diagnose.
    │         └── No → Continue down the tree
    └── No
        Is the service overloaded?
        ├── Yes → Scale up or restart
        └── No
            Is an external dependency down?
            ├── Yes → Enable fallback / circuit breaker
            └── No
                Is data being corrupted?
                ├── Yes → STOP the offending process. Then investigate.
                └── No
                    → Apply general mitigation strategies below
```

---

## Mitigation Pattern 1: Rollback

**When**: A recent deploy introduced the problem.

**Steps**:
1. Identify the last known-good deployment
2. Trigger rollback via your deployment platform
3. Wait for rollback to complete
4. Verify: hit the affected endpoint, check error rates
5. Confirm: users are back to working

**Platform-specific**:
```bash
# Render: Redeploy previous successful deploy from dashboard
# Or use the API to trigger a rollback

# Git-based (if CI/CD auto-deploys):
git revert HEAD
git push origin main
```

**Verification**:
- [ ] Affected endpoint returns expected response
- [ ] Error rate returned to baseline
- [ ] No new errors in logs

**Caveats**:
- If a database migration ran, rollback may not be enough — see data rollback below
- If API consumers cached the new behavior, they may need notification

---

## Mitigation Pattern 2: Feature Flag Toggle

**When**: The broken functionality is behind a feature flag.

**Steps**:
1. Identify which feature flag controls the broken code
2. Toggle it off
3. Verify the feature is disabled and the error stops
4. Confirm: other functionality still works (the toggle didn't break something else)

**Verification**:
- [ ] Feature no longer accessible
- [ ] Error rate dropped
- [ ] Other features unaffected

---

## Mitigation Pattern 3: Service Restart

**When**: The service is in a bad state (memory leak, connection pool exhaustion, deadlock).

**Steps**:
1. Restart the service (or scale down to 0, then back up)
2. Monitor startup: does it come up healthy?
3. Check: do the errors resume after restart?
4. If errors resume immediately → restart isn't the fix, try other patterns
5. If errors resume after a delay → likely a slow leak, restart buys time

**Verification**:
- [ ] Service health check passes
- [ ] Error rate dropped
- [ ] Response times normal

**Caveats**: Restart is a temporary measure for state corruption. If the problem recurs, you need a real fix.

---

## Mitigation Pattern 4: Scale Up

**When**: The service is overwhelmed by traffic or resource usage.

**Steps**:
1. Check current resource usage (CPU, memory, connections)
2. Scale horizontally (more instances) or vertically (bigger instance)
3. Verify: response times improving, errors decreasing
4. If scaling doesn't help → the bottleneck is elsewhere (database, external service)

**Verification**:
- [ ] Response times returned to baseline
- [ ] Error rate dropped
- [ ] Resource usage within acceptable range

---

## Mitigation Pattern 5: Traffic Redirect / Maintenance Mode

**When**: You can't fix the current service quickly and need to buy time.

**Steps**:
1. Put up a maintenance page or redirect to a static fallback
2. If you have a standby environment, redirect traffic there
3. Communicate: tell users what's happening and when you expect resolution

**Verification**:
- [ ] Users see maintenance page (not error page)
- [ ] No traffic hitting the broken service
- [ ] Communication sent

---

## Mitigation Pattern 6: Data Protection

**When**: Data is being corrupted or incorrectly modified.

**Steps**:
1. **STOP THE OFFENDING PROCESS IMMEDIATELY** — kill the job, disable the endpoint, stop the worker
2. Take a backup of the current state (even if it's partially corrupted)
3. Assess the damage: what data was affected, how much, since when?
4. If possible, identify the last known-good state
5. Do NOT attempt data restoration under pressure — mitigate first, restore carefully later

**Verification**:
- [ ] Offending process stopped
- [ ] No further data modification occurring
- [ ] Backup taken of current state

**Caveats**: Data incidents are the most dangerous. Never rush a data restoration. A bad restore can make things much worse.

---

## Mitigation Log Format

For every mitigation action, log:

```
## {timestamp}
**Action**: {what you did}
**Reasoning**: {why you chose this action}
**Result**: {what happened — success/failure/partial}
**Next**: {what you'll try next if this didn't work}
```

---

## When mitigation isn't working

If you've tried two mitigation strategies and neither worked:

1. **Stop and reassess** — are you sure about the triage?
2. **Re-examine scope** — is the problem where you think it is?
3. **Check for multiple causes** — could two things be broken simultaneously?
4. **Consider the nuclear option**: maintenance mode + methodical diagnosis
5. **Don't compound the problem** — each failed mitigation attempt carries risk

---

## After mitigation

Once users are unblocked:

1. Take a breath. The emergency is over (for now).
2. Record the mitigation that worked and exactly what state the system is in.
3. Don't celebrate yet — you've applied a bandage, not a cure.
4. Move to the **Diagnose** phase within the hour.
5. Keep the mitigation in place until the proper fix is deployed.
