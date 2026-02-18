# AGENTS.md

## Mission

Operate this repository with a deterministic, low-friction solo workflow that still preserves branch protection and CI gates.

## Merge command contract

When the user asks to merge a PR (for example: "Merga PR#2"), execute the repository merge script:

- `./scripts/solo-merge-pr.ps1 -PullNumber <PR_NUMBER>`

Default behavior of this script:

1. Enables temporary solo mode on `main`
2. Merges the PR through GitHub API
3. Restores team mode (`1` required approval)
4. Verifies branch protection
5. Syncs local `main` and deletes the local feature branch used by the PR

## Preconditions

Before running merge automation:

- Ensure PR CI check `validate-scaffolds` is green
- Ensure a GitHub token exists in `GITHUB_TOKEN` or `.env.local`

If checks are still running, wait and retry; do not bypass required status checks.

## Safety rules

- Never push directly to `main`
- Use feature branch + PR flow for all changes
- If cleanup must be skipped, run:
  - `./scripts/solo-merge-pr.ps1 -PullNumber <PR_NUMBER> -SkipLocalCleanup`
