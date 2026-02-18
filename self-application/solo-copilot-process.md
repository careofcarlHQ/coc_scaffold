# Solo + Copilot Process (MVP)

A minimal process for one human developer working together with Copilot in this repository.

## Goal

Keep safety gates from the framework, but remove day-to-day friction when no second reviewer is available.

## Default policy

- Always work in a feature branch
- Always open a PR to `main`
- Always require green CI (`Scaffold Validation`)
- Always leave a self-review comment on the PR with checklist evidence

## Two merge modes

## One-click solo merge

When you need a fully automated solo merge flow, run one command:

- `./scripts/solo-merge-pr.ps1 -PullNumber <PR_NUMBER>`

This command will:

1. Enable temporary solo mode (`0` approvals)
2. Merge the PR (default method: `squash`)
3. Restore team mode (`1` approval)
4. Verify team mode protection

### 1) Team mode (preferred)

Use when an external reviewer is available.

- Branch protection requires 1 approval
- Merge only after at least one external `Approve`

Command:

- `./scripts/set-branch-protection.ps1 -Mode team`

### 2) Solo mode (controlled override)

Use only when you are the sole operator and need to merge without external reviewers.

- Branch protection requires 0 approvals
- CI and conversation resolution remain enforced
- Must be temporary for the current merge only

Commands:

1. Enable temporary solo mode:
   - `./scripts/set-branch-protection.ps1 -Mode solo`
2. Merge the PR once checks are green
3. Restore team mode immediately:
   - `./scripts/set-branch-protection.ps1 -Mode team`
4. Verify protection:
   - `./scripts/set-branch-protection.ps1 -Mode team -VerifyOnly`

## PR self-review template (paste into PR comment)

```markdown
## Self-review (solo mode)

- Scope: [what changed]
- Risks checked: links / templates / process contract / CI
- Test evidence: `python -m unittest discover -s tests -p "test_*.py" -v`
- CI status: [link or note]
- Decision: merge in solo mode, then restore team mode
```

## Guardrails

- Never push directly to `main`
- Never keep solo mode enabled after merge
- If uncertain, use team mode and request external approval
