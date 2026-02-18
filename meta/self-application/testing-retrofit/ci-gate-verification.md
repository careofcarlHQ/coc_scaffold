# CI Gate Verification — coc_scaffold (Self-Application)

## Date: 2026-02-18

## Goal
Confirm that quality gates are not only defined but enforceable in real workflow execution.

---

## Verified in repository (automated)

| Gate | Evidence | Status |
|------|----------|--------|
| Workflow triggers on PRs | `.github/workflows/scaffold-validation.yml` contains `pull_request:` | ✅ |
| Test suite runs in CI | Workflow step runs `python -m coverage run ... unittest discover ...` | ✅ |
| Coverage gate enforced | Workflow step runs `coverage report --fail-under=80` | ✅ |
| Coverage floor policy tested | `tests/test_ci_policy.py` validates presence and minimum floor | ✅ |

---

## Branch protection verification (completed)

| Gate | Verification evidence | Status |
|------|------------------------|--------|
| Branch protection requires `Scaffold Validation` check before merge | `scripts/set-branch-protection.ps1` apply + `-VerifyOnly` both passed | ✅ Complete |

## Automation path for branch protection

Use the repository script:

```bash
./scripts/set-branch-protection.ps1
```

Verification-only mode:

```bash
./scripts/set-branch-protection.ps1 -VerifyOnly
```

Prerequisite:
- Export `GITHUB_TOKEN` with repository administration permission before running.

Optional local workflow (`.env.local`):

1. Copy `.env.local.example` → `.env.local`
2. Put your real token in `GITHUB_TOKEN`
3. Load it in PowerShell session:

```powershell
Get-Content .env.local | ForEach-Object {
	if ($_ -match '^\s*([^#=]+)=(.*)$') {
		[Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
	}
}
```

---

## Command evidence (local)

```bash
python -m coverage run --rcfile=.coveragerc -m unittest discover -s tests -p "test_*.py" -v
python -m coverage report --rcfile=.coveragerc --fail-under=80
```

Latest result: PASS, floor satisfied.

Latest measured values:
- Tests: 16/16 passing
- Coverage: 81.15%
- Floor: 80% (passing)
- Branch protection: enabled on `main` with required status check `Scaffold Validation`

---

## Artifact status

All CI gate verification items in this artifact are complete.
