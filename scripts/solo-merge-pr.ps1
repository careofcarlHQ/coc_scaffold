param(
    [string]$Owner = "careofcarlHQ",
    [string]$Repo = "coc_scaffold",
    [int]$PullNumber,
    [string]$Branch = "main",
    [ValidateSet("merge", "squash", "rebase")]
    [string]$MergeMethod = "squash",
    [switch]$SkipLocalCleanup
)

if (-not $PullNumber) {
    Write-Error "PullNumber is required. Example: ./scripts/solo-merge-pr.ps1 -PullNumber 2"
    exit 1
}

function Resolve-GitHubToken {
    if ($env:GITHUB_TOKEN -and $env:GITHUB_TOKEN.Trim() -ne "") {
        return $env:GITHUB_TOKEN.Trim()
    }

    $repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
    $envLocal = Join-Path $repoRoot ".env.local"

    if (Test-Path $envLocal) {
        $line = Get-Content $envLocal | Where-Object { $_ -match '^\s*GITHUB_TOKEN\s*=' } | Select-Object -First 1
        if ($line) {
            return ($line -replace '^\s*GITHUB_TOKEN\s*=\s*', '').Trim().Trim('"').Trim("'")
        }
    }

    return $null
}

$token = Resolve-GitHubToken
if (-not $token) {
    Write-Error "GITHUB_TOKEN not found. Set env var or add GITHUB_TOKEN in .env.local"
    exit 2
}

$env:GITHUB_TOKEN = $token

$headers = @{
    Authorization = "Bearer $token"
    Accept = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
}

$protectionScript = Join-Path $PSScriptRoot "set-branch-protection.ps1"
if (-not (Test-Path $protectionScript)) {
    Write-Error "Missing script: $protectionScript"
    exit 3
}

$soloEnabled = $false
$merged = $false
$featureBranch = $null

try {
    $prUri = "https://api.github.com/repos/$Owner/$Repo/pulls/$PullNumber"
    $pr = Invoke-RestMethod -Method Get -Uri $prUri -Headers $headers
    $featureBranch = $pr.head.ref

    Write-Output "STEP=enable_solo_mode"
    & $protectionScript -Owner $Owner -Repo $Repo -Branch $Branch -Mode solo
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to enable solo mode"
    }
    $soloEnabled = $true

    Write-Output "STEP=merge_pr"
    $mergeUri = "https://api.github.com/repos/$Owner/$Repo/pulls/$PullNumber/merge"
    $mergeBody = @{
        merge_method = $MergeMethod
        commit_title = "Merge PR #$PullNumber via solo automation"
    } | ConvertTo-Json

    $mergeResult = Invoke-RestMethod -Method Put -Uri $mergeUri -Headers $headers -Body $mergeBody

    Write-Output "MERGED=$($mergeResult.merged)"
    Write-Output "MESSAGE=$($mergeResult.message)"
    if (-not $mergeResult.merged) {
        throw "Merge was not completed: $($mergeResult.message)"
    }

    $merged = $true
}
catch {
    Write-Error $_
    exit 4
}
finally {
    if ($soloEnabled) {
        Write-Output "STEP=restore_team_mode"
        & $protectionScript -Owner $Owner -Repo $Repo -Branch $Branch -Mode team
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to restore team mode. Run: ./scripts/set-branch-protection.ps1 -Mode team"
            exit 5
        }

        Write-Output "STEP=verify_team_mode"
        & $protectionScript -Owner $Owner -Repo $Repo -Branch $Branch -Mode team -VerifyOnly
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Team mode verification failed. Run: ./scripts/set-branch-protection.ps1 -Mode team -VerifyOnly"
            exit 6
        }
    }
}

if ($merged -and -not $SkipLocalCleanup) {
    Write-Output "STEP=sync_main_and_cleanup"

    $gitCommand = Get-Command git -ErrorAction SilentlyContinue
    if (-not $gitCommand) {
        Write-Warning "git is not available in PATH; skipping local cleanup"
    }
    else {
        $workingTree = git status --porcelain
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "Unable to inspect git working tree; skipping local cleanup"
        }
        elseif ($workingTree) {
            Write-Warning "Working tree is not clean; skipping local cleanup"
        }
        else {
            git fetch origin | Out-Null

            git switch $Branch | Out-Null
            if ($LASTEXITCODE -ne 0) {
                Write-Warning "Failed to switch to '$Branch'; skipping cleanup"
            }
            else {
                git pull --ff-only origin $Branch | Out-Null
                if ($LASTEXITCODE -ne 0) {
                    Write-Warning "Failed to fast-forward '$Branch'; local branch cleanup skipped"
                }
                elseif ($featureBranch -and $featureBranch -ne $Branch) {
                    $localFeatureBranch = (git branch --list $featureBranch).Trim()
                    if ($localFeatureBranch) {
                        git branch -D $featureBranch | Out-Null
                        if ($LASTEXITCODE -eq 0) {
                            Write-Output "CLEANUP_DELETED_LOCAL_BRANCH=$featureBranch"
                        }
                    }
                }
            }
        }
    }
}

Write-Output "DONE=solo_merge_flow_completed"