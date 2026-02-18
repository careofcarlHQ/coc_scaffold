# Hypothesis Log — PR merge blocked despite green CI

## Investigation started: 2026-02-18
## Current status: root cause found

---

## H1: CI job itself is failing
- **Claim**: merge fails because the required CI job result is failing
- **Because**: GitHub merge endpoint refused merge with status-check message
- **Test**: inspect check runs for PR head SHA
- **Result**: ❌ rejected
- **Evidence**: `validate-scaffolds` check runs completed with `success`
- **Time spent**: 10
- **Next**: inspect required context configured in branch protection

---

## H2: Branch protection expects wrong status context name
- **Claim**: required status check context configured in branch protection does not match real check run name
- **Because**: workflow display name differs from check run context name on GitHub
- **Test**: query branch protection + compare with check-runs API output
- **Result**: ✅ confirmed
- **Evidence**: protection expected `Scaffold Validation`; actual check run context was `validate-scaffolds`
- **Time spent**: 18
- **Next**: update protection automation script to require `validate-scaffolds`

---

## H3: One-click merge script is unsafe because it cannot recover from this mismatch
- **Claim**: if merge fails, protection may remain in solo mode
- **Because**: solo mode toggles before merge attempt
- **Test**: run merge script through failure path and inspect post-state
- **Result**: ❌ rejected
- **Evidence**: script `finally` block restored team mode and verified branch protection after failure
- **Time spent**: 9
- **Next**: keep safety logic; only fix required-check context mismatch

---

## Summary

### Confirmed chain
Wrong required status context in branch protection (`Scaffold Validation`) → required check unresolved on merge gate → GitHub merge API rejects request (`405`) despite green CI run

### Dead ends
| Hypothesis | Why rejected | Time spent |
|------------|-------------|------------|
| CI failing | CI was green (`validate-scaffolds` success) | 10 |
| merge script safety failure | protection restore + verify succeeded | 9 |

### Total investigation time: 37
### Root cause: Branch protection required-check context mismatch with actual check-run context name
