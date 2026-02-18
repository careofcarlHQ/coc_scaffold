# Symptom Capture — PR merge blocked despite green CI

## Date: 2026-02-18
## Severity: high
## Reporter: solo operator

---

## What is happening?
Pull request merge automation fails with GitHub API response indicating required status check mismatch.

```
{"message":"Required status check \"Scaffold Validation\" is expected.","status":"405"}
```

## What should be happening?
If CI for the PR head commit is green, merge automation should proceed without manual branch-protection edits.

## When did it start?
- First observed: 2026-02-18 during automated merge of PR #2
- Pattern: always when required check context is configured as `Scaffold Validation`
- Recent changes: branch-protection automation + one-click merge script introduced

## Who/what is affected?
- Affected users: repository maintainers using one-click merge
- Affected endpoints: `PUT /repos/{owner}/{repo}/pulls/{pull_number}/merge`
- Affected environments: GitHub-hosted repository automation flow

## Reproduction (if known)
1. Configure branch protection required context to `Scaffold Validation`
2. Run CI job where actual check run name is `validate-scaffolds`
3. Run `./scripts/solo-merge-pr.ps1 -PullNumber <N>`
4. Observe merge API failure with required status check message

## Environment
- Python version: 3.13
- Framework version: coc_scaffold (main branch, Feb 2026)
- Database: N/A
- OS: Windows
- Config notes: GitHub token supplied via `.env.local`

## Related context
- Recent deploys: N/A
- Recent migrations: N/A
- Related issues: observed during PR #2 merge run
- Similar past bugs: none recorded prior to this run
