# Fix Spec — PR merge blocked by branch divergence (`dirty`)

## Date: 2026-02-18
## Root cause reference: `meta/self-application/gold-standard/executions/bug-investigation/run-002/root-cause-analysis.md`

---

## Root Cause (brief)
PR branch conflicted with updated `main`, making the PR non-mergeable.

## The Fix

### Code changes
| File | Change | Lines affected |
|------|--------|---------------|
| `scripts/solo-merge-pr.ps1` | resolve add/add conflict by preserving enhanced cleanup + safety behavior | small |
| PR branch | merge/rebase with latest `main`, then rerun checks | small |

### Data changes (if any)
| Table | Change | Records affected |
|-------|--------|-----------------|
| N/A | N/A | 0 |

### Configuration changes (if any)
| Setting | Change |
|---------|--------|
| N/A | none |

## What does NOT change
- No reduction of branch protection constraints
- No bypass of required checks
- No direct pushes to `main`

## Risk Assessment
- **Fix complexity**: low
- **Regression risk**: low
- **Data risk**: none
- **Rollback complexity**: simple

## Regression Test

### Test name
`test_dirty_pr_requires_conflict_resolution_before_merge`

### Setup
- PR branch with known conflict against `main`

### Steps
1. Attempt merge automation
2. Observe non-mergeable response
3. Resolve conflict and push branch
4. Wait for green checks
5. Re-run merge automation

### Expected before fix
Merge fails with `Pull Request is not mergeable`

### Expected after fix
Merge succeeds after conflict resolution and green checks

## Deployment Notes
No deployment artifact changes; process-level remediation only.
