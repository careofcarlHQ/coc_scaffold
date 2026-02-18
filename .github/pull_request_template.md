# Pull Request

## Summary

- Scope: 
- Why: 

## Mode (choose one)

- [ ] Team mode (external approval required)
- [ ] Solo mode (temporary override, restore team mode after merge)

## Self-review checklist

- [ ] I worked from a feature branch (no direct push to `main`)
- [ ] CI check `Scaffold Validation` is green
- [ ] I reviewed changed files and links/templates/process contracts
- [ ] I ran local validation:
  - `python -m unittest discover -s tests -p "test_*.py" -v`

## Solo mode evidence (only if Solo mode is selected)

- [ ] Optional one-click automation used:
  - `./scripts/solo-merge-pr.ps1 -PullNumber <PR_NUMBER>`

- [ ] Enabled temporary solo mode:
  - `./scripts/set-branch-protection.ps1 -Mode solo`
- [ ] Merged PR after green checks
- [ ] Restored team mode immediately:
  - `./scripts/set-branch-protection.ps1 -Mode team`
- [ ] Verified protection:
  - `./scripts/set-branch-protection.ps1 -Mode team -VerifyOnly`

## Risks and rollback

- Risks considered:
- Rollback plan:
