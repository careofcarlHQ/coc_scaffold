# Root Cause Analysis — PR merge blocked by branch divergence (`dirty`)

## Date: 2026-02-18
## Investigator: solo+copilot
## Bug severity: medium

---

## Root Cause Statement
The PR head branch diverged from `main` with an add/add conflict in `scripts/solo-merge-pr.ps1`. GitHub therefore marked the PR as `dirty` and non-mergeable until conflicts were resolved and CI reran on the updated head.

## Causal Chain
```
Base branch advanced while feature branch changed same file
  → add/add conflict on merge
    → PR mergeability state becomes `dirty`
      → merge API returns "Pull Request is not mergeable"
```

## Trigger Conditions
For the bug to occur, ALL of these must be true:
1. Base branch receives overlapping changes after PR branch creation
2. PR branch is not rebased/merged with base before merge
3. Merge automation is attempted on dirty PR head

## Scope Assessment
- Records/users affected: maintainers merging stale/conflicting PRs
- Environments affected: GitHub PR merge workflow
- Duration: until conflict resolution commit is pushed
- Discovered via: automation test run on PR #3

## Code Location
- **Primary location**: `scripts/solo-merge-pr.ps1` (conflicted file)
- **Contributing code**: branch synchronization process before merge
- **Data involved**: git branch refs (`main` and PR head)

## Sibling Bugs
| Location | Same pattern? | Risk | Action |
|----------|--------------|------|--------|
| Any high-churn script/docs files in active PRs | yes | medium | add pre-merge dirty-state check to runbook |

## Why This Happened
The branch had valid changes but was not conflict-free relative to updated `main`. This is a normal PR lifecycle hazard, not a logic bug in merge automation.

## Prevention Recommendations
| Recommendation | Type | Effort | Prevents |
|----------------|------|--------|----------|
| Add explicit dirty-state remediation steps to effectiveness runbook | process | small | repeat incidents of same class |
| Add optional preflight in merge script to fail fast when PR `mergeable_state=dirty` | automation | medium | unnecessary mode toggles before known conflict |

## References
- Symptom capture: `meta/self-application/gold-standard/executions/bug-investigation/run-002/symptom-capture.md`
- Hypothesis log: `meta/self-application/gold-standard/executions/bug-investigation/run-002/hypothesis-log.md`
- Fix spec: `meta/self-application/gold-standard/executions/bug-investigation/run-002/fix-spec.md`
