# Feature Spec — One-click solo merge automation

## Summary
Provide a deterministic one-command merge operation for protected `main` that safely handles temporary solo mode, merge execution, protection restoration, and local cleanup.

## Motivation
Reduce manual merge friction for solo operator workflows while preserving CI/branch-protection safety guarantees.

## Scope

### In scope
- Add `scripts/solo-merge-pr.ps1`
- Integrate with `scripts/set-branch-protection.ps1`
- Document operator contract in `AGENTS.md`, README, and PR template

### Not in scope
- Bypassing required status checks
- Replacing GitHub branch protection with custom policy engines

## Database Changes
No database changes.

### New tables
| Table | Column | Type | Nullable | Default | Constraints | Purpose |
|-------|--------|------|----------|---------|-------------|---------|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A |

### Modified tables
| Table | Change | Migration notes |
|-------|--------|----------------|
| N/A | none | none |

## API Changes
No application API changes. Uses existing GitHub APIs as operator integration.

### New endpoints
N/A

### Modified endpoints
| Method | Path | Change | Backward compatible? |
|--------|------|--------|---------------------|
| N/A | N/A | none | yes |

## Business Logic
1. Enable temporary solo mode before merge
2. Attempt merge via GitHub API
3. Always restore team mode and verify protection
4. If merge succeeded, sync local main and remove local feature branch

### Edge cases
| Scenario | Expected behavior |
|----------|------------------|
| CI pending | merge rejected; process retries only after checks complete |
| PR dirty/conflicted | merge rejected; conflict resolution required before retry |
| API/auth failure | fail safely and restore team mode |

## Compatibility
- Existing branch-protection model retained
- Existing PR flow retained
- Existing test suite remains green

## Test Requirements

### Unit tests
- N/A (script-driven operational logic)

### Integration tests
- Merge flow success path
- Failure path with required-check mismatch
- Failure path with dirty PR

### Edge case tests
- Team mode restoration after any failure
- Verify required check context is correct

## Acceptance Criteria

- [x] One command merges compliant PRs safely
- [x] Team mode is restored and verified in all paths
- [x] No direct push to `main` required
- [x] Existing tests continue to pass
