# Rollout Plan — One-click solo merge automation

## Feature spec: `meta/self-application/gold-standard/executions/feature-addition/run-001/feature-spec.md`
## Date: 2026-02-18

---

## Pre-Deployment Checklist

- [x] All acceptance criteria met
- [x] Zero test regressions
- [x] Compatibility check passed
- [x] Migration tested (up and down)
- [x] Rollback steps documented (below)
- [x] Feature flag in place (if applicable)

## Deployment Steps

### 1. Database Migration
```bash
# no migration required
```

**Verify**: no schema changes expected
**Rollback**: none

### 2. Backend Deployment
```bash
# script and docs merged via protected PR flow
./scripts/solo-merge-pr.ps1 -PullNumber <PR_NUMBER>
```

**Verify**:
- Branch protection in team mode after merge
- Required context `validate-scaffolds` configured

**Rollback**: revert merge commit via PR, re-run verification

### 3. Frontend Deployment (if applicable)
```bash
# not applicable
```

**Verify**:
- N/A

**Rollback**: N/A

### 4. Feature Verification
- [x] One-click merge works on compliant PR
- [x] Failure path restores team mode
- [x] Local cleanup can be skipped when needed

### 5. Monitor (24 hours)
- [x] No branch-protection drift
- [x] No merge safety regressions observed
- [x] No unexpected operational errors

## Feature Flag (if applicable)

```
Flag name: N/A
Default: N/A
```

## Rollback Plan

### Trigger conditions
Roll back if any of these occur within 24 hours:
- team mode not restored automatically
- merge script bypasses required checks
- local cleanup causes unsafe branch deletions

### Rollback steps
1. Disable automation use and revert to manual PR merge path
2. Revert problematic script commit via PR
3. Re-apply/verify protection with:
   - `./scripts/set-branch-protection.ps1 -Mode team`
   - `./scripts/set-branch-protection.ps1 -Mode team -VerifyOnly`
4. Re-run tests and operational check

### Data considerations
- New rows created: none
- Modified rows: none
- External side effects: GitHub branch protection settings (reversible)

## Post-Deployment

- [x] Feature working in production
- [x] Monitoring confirms no issues
- [x] Feature flag set to production state
- [x] Clean up feature branch
- [x] Clean up feature brief / temporary AGENTS.md section
- [x] Update documentation if needed
