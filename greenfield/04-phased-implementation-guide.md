# 04 — Phased Implementation Guide

## The stage pattern

Every phase follows the same 11-stage pattern (0–10). This pattern was validated across three full phases in `coc_agent_process`.

```
Stage 0   Foundation lock / pre-flight verification
Stage 1   Project skeleton / scaffolding
Stage 2   Core data layer
Stage 3   Primary API / interface
Stage 4   Secondary API / supporting features
Stage 5   Background processing / workers
Stage 6   Policy enforcement / business rules
Stage 7   Evidence / output assembly
Stage 8   Operational reliability
Stage 9   Pilot trial (real work)
Stage 10  Phase sign-off
```

## Stage design rules

### 1. Each stage should be completable in 1–4 hours

If a stage takes longer, it's too big. Break it into sub-stages (4a, 4b, etc.) or split across two stages.

### 2. Each stage has an acceptance gate

An acceptance gate is an **objective, reproducible** condition. Examples:

```markdown
# ✅ Good acceptance gates
- API process starts locally and `/healthz` returns ok
- Fresh DB bootstrap + migration succeeds from zero
- Invalid state transition returns 409
- Open escalation prevents stage progression until resolved
- Worker processes job and writes result to database

# ❌ Bad acceptance gates
- "System works correctly"
- "Code looks clean"
- "Tests pass" (which tests?)
```

### 3. Stages build on each other linearly

Stage N assumes all stages 0 through N-1 are complete and their gates passed. Never skip a stage.

### 4. Every stage produces artifacts

At minimum, each stage completion should include:
- Updated code (committed)
- Updated docs (if behavior changed)
- Acceptance gate evidence (how did you verify?)
- Risk/rollback note (what could go wrong?)
- Open questions (what wasn't resolved?)

## Phase 1 pattern (MVP backend)

This is the standard Phase 1 pattern for a backend service. Adapt to your project.

```
Stage 0  — Foundation Lock
           Confirm stack, contracts, policies. No unresolved architecture decisions.

Stage 1  — Project Skeleton
           Create repo structure. Add dependency management. Health endpoint.
           Gate: Process starts, /healthz returns ok.

Stage 2  — Database + Migrations
           Implement schema. Create baseline migration. Add constraints.
           Gate: Fresh DB bootstrap succeeds. Invalid transitions rejected.

Stage 3  — Primary Resource API
           CRUD endpoints for main resource. State transitions. Audit logging.
           Gate: Can create resource and move through allowed states only.

Stage 4  — Supporting APIs
           Secondary resources (handoffs, escalations, etc.). Cross-resource rules.
           Gate: Supporting resources enforce their constraints.

Stage 5  — Background Workers
           Queue table, job claim, retry/backoff, dead-letter.
           Gate: Worker processes jobs reliably. Duplicates prevented.

Stage 6  — Policy Enforcement
           Merge gates, cost controls, guardrail breach handling.
           Gate: Policy violations are caught and blocked at runtime.

Stage 7  — Evidence Assembly
           Aggregate outputs into structured evidence packages.
           Gate: One real task produces complete evidence.

Stage 8  — Operational Reliability
           Local isolation, restart recovery, startup verification.
           Gate: System restarts cleanly without state corruption.

Stage 9  — Pilot Trial
           Run 3+ real tasks at different risk levels through the system.
           Gate: All tasks complete with full lifecycle artifacts.

Stage 10 — Phase Sign-Off
           Metrics captured. Gaps documented for next phase.
           Gate: System runs end-to-end without ad-hoc decisions.
```

## Phase 2 pattern (UI + hardening)

```
Stage 0  — Pre-flight verification (backend running, UI scaffold builds)
Stage 1  — API client / SDK layer
Stage 2  — Status/dashboard page
Stage 3  — Primary resource page (list + create)
Stage 4  — Detail page (view + actions)
Stage 5  — Evidence/export page
Stage 6  — Auth/security hardening
Stage 7  — Error handling and UX polish
Stage 8  — End-to-end smoke tests
Stage 9  — Real user testing
Stage 10 — Phase sign-off
```

## Phase 3 pattern (external integrations)

```
Stage 0  — Pre-flight (Phase 2 complete, credentials configured)
Stage 1  — External API adapter (e.g., OpenAI, GitHub)
Stage 2  — Webhook ingestion
Stage 3  — Outbound operations (create branches, open PRs)
Stage 4  — Agent role execution (planner, implementer, etc.)
Stage 5  — Cost tracking on real API calls
Stage 6  — End-to-end integration test
Stage 7  — Error recovery and retry paths
Stage 8  — Rate limiting and safety
Stage 9  — Pilot: real external operation
Stage 10 — Phase sign-off
```

## Tracking progress

Use the implementation log template to track each stage:

```markdown
### Stage N — [Name]

- Status: not-started / in-progress / done / blocked
- Work completed:
- Decisions made:
- Blockers:
- Evidence links:
- Acceptance gate result: pass / fail
```

## When to start a new phase

A new phase starts when:
1. The current phase's exit definition is fully met
2. All Stage 10 criteria are satisfied
3. Remaining gaps are documented for the next phase
4. The next phase's checklist is written with acceptance gates

## Common pitfalls

| Pitfall | Consequence | Prevention |
|---------|-------------|------------|
| Advancing past a failing gate | Technical debt compounds | Block on gate failure, fix before advancing |
| Stages too large | Progress stalls, context lost | Split stages to 1–4 hour chunks |
| No evidence for gates | Can't verify completion later | Capture evidence immediately |
| Skipping Stage 9 (pilot) | Ship untested system | Always run real work through the system |
| Phase 2 without Phase 1 sign-off | Building on unstable foundation | Complete all Stage 10 criteria first |
