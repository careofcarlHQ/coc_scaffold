# 02 — Project Kickoff Checklist

Use this checklist to bootstrap a new project from zero using the agent-first scaffold.

## Prerequisites

- [ ] Git repository created
- [ ] Development environment set up (language runtime, package manager)
- [ ] AI coding assistant configured (Copilot, Codex, Claude, etc.)

---

## Stage 0 — Repository Foundation (30 minutes)

### 0.1 Create directory structure
```
project-root/
├── AGENTS.md
├── start-dev.ps1
├── spec/
│   └── PROCESS_INDEX.md
├── .env.example
├── .gitignore
└── README.md
```

- [ ] Create AGENTS.md (use [templates/AGENTS.md.template](templates/AGENTS.md.template))
- [ ] Create start-dev.ps1 (use [templates/start-dev.ps1.template](templates/start-dev.ps1.template))
  - [ ] Confirm script stops stale API process trees (not only port-based kill)
- [ ] Create spec/ directory
- [ ] Create spec/PROCESS_INDEX.md (use [templates/PROCESS_INDEX.md.template](templates/PROCESS_INDEX.md.template))
- [ ] Create .env.example with required environment variables
- [ ] Create .gitignore appropriate for your stack
- [ ] Create README.md with project overview

### 0.2 Initial commit

- [ ] Commit the foundation with message: "Stage 0: repository foundation"

---

## Stage 1 — PRD and Scope (1–2 hours)

- [ ] Write the PRD (use [templates/PRD.md.template](templates/PRD.md.template))
  - [ ] Summary
  - [ ] Problem statement
  - [ ] Goals (with timeframe)
  - [ ] Non-goals (explicit)
  - [ ] Target operating model
  - [ ] Autonomy and merge policy
- [ ] Add PRD to spec/
- [ ] Update PROCESS_INDEX.md to reference PRD

---

## Stage 2 — Gap Analysis (1 hour)

- [ ] Audit existing documentation against build requirements
- [ ] Create `spec/build-readiness-gap-analysis.md` (use [templates/gap-analysis.md.template](templates/gap-analysis.md.template))
  - [ ] List what's already covered
  - [ ] List P0 gaps (blocks building)
  - [ ] List P1 gaps (blocks reliable operations)
  - [ ] For each gap: specify the exact artifact needed

---

## Stage 3 — Write P0 Specs (2–4 hours)

Write in dependency order:

- [ ] `spec/implementation-architecture.md` — stack, structure, service boundaries
- [ ] `spec/data-model.md` — schemas, state machine, transitions
- [ ] `spec/api-contract.md` — endpoints, payloads, error codes
- [ ] `spec/bootstrap-local.md` — environment setup and run commands
- [ ] `spec/engineering-best-practices.md` — coding rules and delivery defaults

### Optional P0 specs (if applicable):
- [ ] `spec/job-contract.md` — queue semantics, retries, dead-letter
- [ ] `spec/cost-control.md` — budget layers, caps, escalation triggers
- [ ] `spec/guardrails-policy.md` — safety boundaries, merge gates
- [ ] `spec/escalation-policy.md` — when to stop and ask a human

---

## Stage 4 — Phase 1 Checklist (1–2 hours)

- [ ] Create `spec/phase-1-implementation-checklist.md` (use [templates/implementation-checklist.md.template](templates/implementation-checklist.md.template))
  - [ ] Define exit criteria for Phase 1
  - [ ] Define stages 0–10 with acceptance gates
  - [ ] Ensure each stage is achievable in 1–4 hours of agent work
- [ ] Create `spec/implementation-log-template.md` for progress tracking

---

## Stage 5 — Begin Phase 1 Build

- [ ] Follow the phase 1 checklist stage by stage
- [ ] Do not advance past an acceptance gate until it's met
- [ ] Log progress using the implementation log template
- [ ] Commit after each stage completion

---

## Verification gate

Project kickoff is complete when:

- [ ] AGENTS.md exists and points to all key docs
- [ ] start-dev.ps1 performs reliable restart (stale backend process-tree cleanup + port cleanup)
- [ ] PRD defines clear scope and non-goals
- [ ] Gap analysis is complete with no unaddressed P0 gaps
- [ ] All P0 spec documents exist
- [ ] Phase 1 checklist exists with acceptance gates
- [ ] First implementation stage (skeleton/health check) passes
