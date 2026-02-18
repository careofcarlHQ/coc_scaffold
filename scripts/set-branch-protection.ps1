param(
    [string]$Owner = "careofcarlHQ",
    [string]$Repo = "coc_scaffold",
    [string]$Branch = "main",
    [ValidateSet("team", "solo")]
    [string]$Mode = "team",
    [Nullable[int]]$RequiredApprovals = $null,
    [switch]$VerifyOnly
)

$token = $env:GITHUB_TOKEN
if (-not $token) {
    Write-Error "GITHUB_TOKEN is not set. Export a token with repository administration permissions and retry."
    exit 1
}

$headers = @{
    Authorization = "Bearer $token"
    Accept = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
}

$uri = "https://api.github.com/repos/$Owner/$Repo/branches/$Branch/protection"

$effectiveApprovals = if ($null -ne $RequiredApprovals) {
    [int]$RequiredApprovals
}
elseif ($Mode -eq "solo") {
    0
}
else {
    1
}

if (-not $VerifyOnly) {
    $body = @{
        required_status_checks = @{
            strict   = $true
            contexts = @("Scaffold Validation")
        }
        enforce_admins = $true
        required_pull_request_reviews = @{
            dismissal_restrictions = @{}
            dismiss_stale_reviews  = $true
            require_code_owner_reviews = $false
            required_approving_review_count = $effectiveApprovals
            require_last_push_approval = $false
        }
        restrictions = $null
        required_linear_history = $false
        allow_force_pushes = $false
        allow_deletions = $false
        block_creations = $false
        required_conversation_resolution = $true
        lock_branch = $false
        allow_fork_syncing = $false
    } | ConvertTo-Json -Depth 8

    Invoke-RestMethod -Method Put -Uri $uri -Headers $headers -Body $body | Out-Null
    Write-Output "Branch protection applied to ${Owner}/${Repo}:${Branch}"
}

$result = Invoke-RestMethod -Method Get -Uri $uri -Headers $headers

$contexts = @()
if ($result.required_status_checks -and $result.required_status_checks.contexts) {
    $contexts = @($result.required_status_checks.contexts)
}

$hasScaffoldValidation = $contexts -contains "Scaffold Validation"
$enforceAdmins = [bool]$result.enforce_admins.enabled
$requiredReviews = [int]$result.required_pull_request_reviews.required_approving_review_count
$conversationResolution = [bool]$result.required_conversation_resolution.enabled

Write-Output "VERIFY_HAS_SCAFFOLD_VALIDATION=$hasScaffoldValidation"
Write-Output "VERIFY_ENFORCE_ADMINS=$enforceAdmins"
Write-Output "VERIFY_MODE=$Mode"
Write-Output "VERIFY_EFFECTIVE_REQUIRED_REVIEWS=$effectiveApprovals"
Write-Output "VERIFY_REQUIRED_REVIEWS=$requiredReviews"
Write-Output "VERIFY_CONVERSATION_RESOLUTION=$conversationResolution"

if (-not $hasScaffoldValidation) {
    Write-Error "Verification failed: required status check 'Scaffold Validation' is not configured."
    exit 2
}

if ($requiredReviews -ne $effectiveApprovals) {
    Write-Error "Verification failed: expected required approvals $effectiveApprovals but found $requiredReviews."
    exit 3
}

Write-Output "Branch protection verification passed."
