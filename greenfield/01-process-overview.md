# 01 — Process Overview: End-to-End Workflow

## The development lifecycle

Building a project with this scaffold follows a predictable lifecycle. Each phase builds on the previous one, and every transition has an explicit gate.

```
┌─────────────────────────────────────────────────────────┐
│                    PROJECT LIFECYCLE                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. INCEPTION          Write PRD, define scope          │
│       │                                                 │
│       ▼                                                 │
│  2. GAP ANALYSIS       Audit what's missing             │
│       │                                                 │
│       ▼                                                 │
│  3. SPEC WRITING       Contracts, models, policies      │
│       │                                                 │
│       ▼                                                 │
│  4. PHASED BUILD       Checklists + acceptance gates    │
│       │                                                 │
│       ▼                                                 │
│  5. PILOT TRIAL        Real work through the system     │
│       │                                                 │
│       ▼                                                 │
│  6. OPERATIONS         Weekly review + tuning           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Phase breakdown

### 1. Inception (Day 1)

**Input**: An idea or problem statement  
**Output**: PRD + AGENTS.md + initial spec directory

Activities:
- Write a PRD that defines the problem, goals, non-goals, and target operating model
- Create AGENTS.md as the entry point for agents
- Create the `spec/` directory with a PROCESS_INDEX.md
- Define the initial scope boundary (what's in v1, what's not)

Key documents:
- `AGENTS.md`
- `spec/PROCESS_INDEX.md`
- `spec/{project}-PRD.md`

### 2. Gap Analysis (Day 1–2)

**Input**: PRD + any existing documentation  
**Output**: Prioritized list of missing specs and artifacts

Activities:
- Audit all existing docs against what's needed to start building
- Classify gaps as P0 (blocks building) or P1 (blocks reliable operations)
- For each gap, specify the exact document/artifact needed

Key document:
- `spec/build-readiness-gap-analysis.md`

The gap analysis from `coc_agent_process` identified these P0 gaps:
1. Technical stack decision and codebase skeleton
2. API contract specification
3. Data model and migrations spec
4. Job/queue execution contract
5. Environment bootstrap and run commands

### 3. Spec Writing (Day 2–5)

**Input**: Gap analysis priorities  
**Output**: Complete P0 spec set

Write specs in dependency order:

```
1. implementation-architecture.md    ← stack decisions + repo structure
2. data-model.md                     ← schemas + state machine
3. api-contract.md                   ← endpoints + payloads + errors
4. job-contract.md                   ← queue semantics + retries
5. cost-control.md                   ← budget layers + caps
6. guardrails-policy.md              ← safety boundaries
7. escalation-policy.md              ← when to stop and ask
8. bootstrap-local.md                ← how to run locally
9. engineering-best-practices.md     ← coding rules
```

Each spec must be:
- **Complete enough** for an agent to implement from
- **Precise** — no ambiguous "should" without concrete criteria
- **Self-contained** — agents shouldn't need to search outside the spec

See [03-spec-writing-guide.md](03-spec-writing-guide.md) for details.

### 4. Phased Build (Day 5+)

**Input**: Complete spec set  
**Output**: Working software with evidence trail

Work is organized into phases (major capability milestones) and stages (incremental build steps within a phase).

Pattern from `coc_agent_process`:

| Phase | Focus | Stages |
|-------|-------|--------|
| Phase 1 | MVP backend (API + worker + DB) | 0–10 |
| Phase 2 | Operator UI + security hardening | 0–10 |
| Phase 3 | External integrations (LLM + GitHub) | 0–10 |

Each phase has:
- A **phase checklist** with all stages
- An **exit definition** (what "done" means for the phase)
- Stages 0–10 with concrete acceptance gates

See [04-phased-implementation-guide.md](04-phased-implementation-guide.md) for the stage pattern.

### 5. Pilot Trial (Phase 1, Stage 9)

**Input**: Working system  
**Output**: Evidence that the system handles real work

Run 3+ real tasks through the system at different risk levels:
- Task A: Low risk (docs/chore)
- Task B: Medium risk (feature change)
- Task C: Higher risk (integration change with escalation test)

All tasks must complete with full lifecycle artifacts.

### 6. Operations (Ongoing)

**Input**: Running system  
**Output**: Continuous improvement

Weekly cadence:
1. Process health review (metrics)
2. Drift and hygiene pass (docs vs reality)
3. Escalation pattern analysis
4. Process tuning
5. Decision log

See [05-operational-cadence.md](05-operational-cadence.md) for details.

---

## Task-level workflow

Within the phased build, individual units of work follow a lifecycle:

```
Intake → Planning → Implementation → Review → Validation → Human Approval → Merge
```

### Intake (Human)
- Problem statement
- Constraints and acceptance criteria
- Risk tier and change class
- Escalation pre-check

### Planning (Agent)
- Scope and non-goals
- Implementation plan
- Validation plan
- Risk + rollback strategy

### Implementation (Agent)
- Code, tests, docs
- Changed-file map with rationale
- Local checks from validation plan

### Review (Agent or Human)
- Correctness against acceptance criteria
- Architecture compliance
- Security/policy compliance
- Approve or request changes

### Validation (Agent)
- Build, lint, test evidence
- Runtime/UI checks where applicable
- Reproducible command outputs

### Human Approval
- Review compact checklist + key risks
- Merge, hold, or return for changes

### Merge + Post-Merge
- CI verification
- Cleanup temporary artifacts
- Update metrics
