# Fix Spec — PR merge blocked despite green CI

## Date: 2026-02-18
## Root cause reference: `meta/self-application/gold-standard/executions/bug-investigation/run-001/root-cause-analysis.md`

---

## Root Cause (brief)
Branch protection required status context did not match actual GitHub check-run context.

## The Fix

### Code changes
| File | Change | Lines affected |
|------|--------|---------------|
| `scripts/set-branch-protection.ps1` | replace required context `Scaffold Validation` with `validate-scaffolds`; improve verification output and mismatch failure handling | small |
| `.github/pull_request_template.md` | update CI checklist wording to `validate-scaffolds` | small |
| `meta/self-application/solo-copilot-process.md` | align CI reference to actual context name | small |

### Data changes (if any)
| Table | Change | Records affected |
|-------|--------|-----------------|
| N/A | N/A | 0 |

### Configuration changes (if any)
| Setting | Change |
|---------|--------|
| Branch protection required status check context | `Scaffold Validation` → `validate-scaffolds` |

## What does NOT change
- No changes to scaffold content semantics
- No changes to merge safety sequence (`solo -> merge -> team restore -> verify`)
- No bypass of branch-protection policy

## Risk Assessment
- **Fix complexity**: low
- **Regression risk**: low
- **Data risk**: none
- **Rollback complexity**: simple

## Regression Test

### Test name
`test_branch_protection_required_context_matches_ci_check`

### Setup
- Branch protection managed via `scripts/set-branch-protection.ps1`
- CI workflow job emits check context `validate-scaffolds`

### Steps
1. Apply protection with script defaults
2. Verify required context includes `validate-scaffolds`
3. Run one-click merge after green checks

### Expected before fix
Merge fails with required status check mismatch (405)

### Expected after fix
Merge succeeds when check run `validate-scaffolds` is green

## Deployment Notes
No special deployment sequence. Apply script changes, then re-run merge workflow and verify branch protection output.
