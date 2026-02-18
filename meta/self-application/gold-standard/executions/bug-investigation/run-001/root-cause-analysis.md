# Root Cause Analysis — PR merge blocked despite green CI

## Date: 2026-02-18
## Investigator: solo+copilot
## Bug severity: high

---

## Root Cause Statement
Branch protection was configured to require status check context `Scaffold Validation`, while the actual GitHub check run context produced by the workflow was `validate-scaffolds`. Because required context matching is exact, merge was blocked even when CI succeeded.

## Causal Chain
```
Required check context hardcoded to `Scaffold Validation`
  → GitHub cannot match required context to actual check `validate-scaffolds`
    → required status appears unsatisfied at merge time
      → merge API responds with 405 / required status check expected
```

## Trigger Conditions
For the bug to occur, ALL of these must be true:
1. Branch protection is enforced with exact required contexts
2. Required context is set to `Scaffold Validation`
3. Workflow job check context emitted as `validate-scaffolds`

## Scope Assessment
- Records/users affected: all maintainers using automated merge on protected main
- Environments affected: repository branch-protection merge flow
- Duration: from first introduction of one-click merge until fix deployment
- Discovered via: operational run during PR merge

## Code Location
- **Primary location**: `scripts/set-branch-protection.ps1` required status contexts
- **Contributing code**: `scripts/solo-merge-pr.ps1` (revealed mismatch during merge call)
- **Data involved**: branch protection settings on `main`

## Sibling Bugs
| Location | Same pattern? | Risk | Action |
|----------|--------------|------|--------|
| other repos using copied script | yes | high | enforce context naming checklist in gold program |

## Why This Happened
A display-name assumption was used for required checks. GitHub branch protection requires exact context keys, not human-friendly workflow labels.

## Prevention Recommendations
| Recommendation | Type | Effort | Prevents |
|----------------|------|--------|----------|
| Use actual check context (`validate-scaffolds`) in protection automation | process+automation | small | this bug |
| Add effectiveness runbook check: compare required contexts vs check-runs API | test/process | small | class of mismatch bugs |

## References
- Symptom capture: `meta/self-application/gold-standard/executions/bug-investigation/run-001/symptom-capture.md`
- Hypothesis log: `meta/self-application/gold-standard/executions/bug-investigation/run-001/hypothesis-log.md`
- Fix spec: `meta/self-application/gold-standard/executions/bug-investigation/run-001/fix-spec.md`
