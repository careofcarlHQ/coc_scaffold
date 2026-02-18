# Hypothesis Log — PR merge blocked by branch divergence (`dirty`)

## Investigation started: 2026-02-18
## Current status: root cause found

---

## H1: Required CI check is failing again
- **Claim**: merge failed because required check was not green
- **Because**: merge API returned 405
- **Test**: inspect check runs for PR head SHA
- **Result**: ❌ rejected
- **Evidence**: `validate-scaffolds` concluded `success`
- **Time spent**: 7
- **Next**: inspect PR mergeability state

---

## H2: PR has merge conflict / dirty state against base
- **Claim**: head branch diverged from `main` and cannot be merged automatically
- **Because**: GitHub mergeability status shows `dirty`
- **Test**: query PR mergeability and attempt update-branch API
- **Result**: ✅ confirmed
- **Evidence**: PR `mergeable=False`, `mergeable_state=dirty`; update-branch API returned merge conflict
- **Time spent**: 16
- **Next**: resolve conflict locally, push updated head, rerun checks and merge

---

## H3: Merge script leaves protection in unsafe mode on merge failure
- **Claim**: if merge fails on dirty PR, team protections may remain disabled
- **Because**: script enables solo mode before merge call
- **Test**: inspect script run output after failure
- **Result**: ❌ rejected
- **Evidence**: script restored `team` mode and verified protection in `finally` path
- **Time spent**: 6
- **Next**: retain current safety design; improve runbook guidance for dirty PR remediation

---

## Summary

### Confirmed chain
PR head diverged from base (`dirty`) → GitHub marks PR non-mergeable → merge API rejects request → manual conflict resolution + recheck required before merge

### Dead ends
| Hypothesis | Why rejected | Time spent |
|------------|-------------|------------|
| CI failure | required check was green | 7 |
| script safety regression | protection restore path worked correctly | 6 |

### Total investigation time: 29
### Root cause: PR branch conflict with latest `main` (mergeability dirty), not CI or protection misconfiguration
