# Symptom Capture — PR merge blocked by branch divergence (`dirty`)

## Date: 2026-02-18
## Severity: medium
## Reporter: solo operator

---

## What is happening?
One-click merge for PR #3 failed with GitHub error indicating PR is not mergeable due to divergence/conflict.

```
{"message":"Pull Request is not mergeable","status":"405"}
```

## What should be happening?
When a PR branch is behind/conflicting with `main`, the process should surface the conflict, resolve it safely, and complete merge without bypassing protections.

## When did it start?
- First observed: 2026-02-18 during merge attempt for PR #3
- Pattern: deterministic for conflicting PR head
- Recent changes: `main` moved while feature branch had pending docs/process updates

## Who/what is affected?
- Affected users: maintainers using one-click merge with stale/conflicting PR heads
- Affected endpoints: merge API and update-branch flow
- Affected environments: GitHub PR workflow

## Reproduction (if known)
1. Open PR with branch that conflicts with latest `main`
2. Run `./scripts/solo-merge-pr.ps1 -PullNumber 3`
3. Observe `Pull Request is not mergeable`

## Environment
- Python version: 3.13
- Framework version: coc_scaffold (main branch, Feb 2026)
- Database: N/A
- OS: Windows
- Config notes: protected `main`, required check `validate-scaffolds`

## Related context
- Recent deploys: N/A
- Recent migrations: N/A
- Related issues: conflict surfaced in PR #3 merge test
- Similar past bugs: run-001 was a status-check mismatch (different class)
