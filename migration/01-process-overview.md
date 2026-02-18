# 01 — Process Overview: End-to-End Migration Workflow

## The migration lifecycle

```
┌─────────────────────────────────────────────────────────┐
│                    MIGRATION LIFECYCLE                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. SNAPSHOT           Document current state            │
│       │                                                 │
│       ▼                                                 │
│  2. TARGET DEFINITION  Define where we're going         │
│       │                                                 │
│       ▼                                                 │
│  3. GAP MAP            Identify every break point       │
│       │                                                 │
│       ▼                                                 │
│  4. PLAN               Staged migration strategy        │
│       │                                                 │
│       ▼                                                 │
│  5. EXECUTE            Incremental migration + verify   │
│       │                                                 │
│       ▼                                                 │
│  6. CUTOVER            Switch from old to new           │
│       │                                                 │
│       ▼                                                 │
│  7. CLEANUP            Remove old artifacts             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Phase breakdown

### 1. Snapshot (1–2 hours)

**Input**: A running system that needs migration
**Output**: Current state snapshot document

Activities:
- Document all versions (language, framework, database, dependencies)
- Document infrastructure (hosting, networking, DNS, secrets)
- Document data (table counts, row counts, data sizes)
- Document configuration (environment variables, feature flags)
- Document integrations (external APIs, webhooks, consumers)
- Run the test suite and capture baseline results
- Capture performance baselines (response times, throughput)

Key document:
- `migration/current-state-snapshot.md`

Gate: Every field in the snapshot template is filled. No "unknown" entries.

### 2. Target Definition (1 hour)

**Input**: Migration motivation (why change)
**Output**: Target state definition document

Activities:
- Define the target versions / platform / configuration
- State the motivation (why migrate now?)
- Define success criteria (what "done" looks like)
- Define non-negotiable requirements (zero downtime? data preservation?)
- Set a time box for the entire migration

Key document:
- `migration/target-state-definition.md`

Gate: Target state is specific (version numbers, not "latest"). Success criteria are objective.

### 3. Gap Map (2–4 hours)

**Input**: Current state + target state
**Output**: Compatibility gap map

Activities:
- For each layer (infra, data, dependencies, code, config, consumers), identify:
  - What changes between current and target
  - What breaks
  - What needs adaptation
  - What's unchanged
- Classify each gap by risk (low / medium / high) and effort (hours / days)
- Identify dependencies between gaps (must fix A before B)
- Identify gaps that can be parallelized

Key document:
- `migration/compatibility-gap-map.md`

Gate: Every gap has a risk level, effort estimate, and dependency list. No unclassified items.

### 4. Plan (1–2 hours)

**Input**: Gap map
**Output**: Migration plan with stages

Activities:
- Group gaps into stages (each independently deployable)
- Order stages by dependency and risk (lowest risk first)
- Define rollback strategy for each stage
- Identify parallel-running opportunities
- Set timeline with checkpoints
- Define abort criteria (when to stop and reconsider)

Key documents:
- `migration/migration-checklist.md`
- `migration/rollback-plan.md`

Gate: Every stage has a rollback plan. Timeline is realistic. Abort criteria defined.

### 5. Execute (days to weeks)

**Input**: Migration plan
**Output**: Migrated system (still running alongside old)

Activities per stage:
1. Announce stage (update migration checklist)
2. Take backup (if data-touching)
3. Apply changes
4. Run verification (tests, smoke tests, integration checks)
5. Verify rollback works
6. Mark stage complete (with evidence)

Key document:
- `migration/migration-checklist.md` (updated per stage)

Gate per stage: Changes applied. Verification passes. Rollback verified. Evidence captured.

### 6. Cutover (1–2 hours)

**Input**: Fully migrated system (parallel with old)
**Output**: New system as primary

Activities:
- Final verification on new system
- Route traffic / connections to new system
- Monitor for errors (first hour)
- Confirm old system can be decommissioned
- Keep old system available for rollback (24–72 hours)

Key document:
- `migration/cutover-checklist.md`

Gate: New system serving all traffic. Error rates normal. Old system standby confirmed.

### 7. Cleanup (1–2 hours)

**Input**: Stable new system (post-cutover monitoring period)
**Output**: Clean state with no migration residue

Activities:
- Remove compatibility shims
- Delete old configuration
- Decommission old system / old database
- Update all documentation
- Archive migration artifacts
- Update AGENTS.md

Gate: No references to old state remain. Documentation updated. Migration artifacts archived.

---

## Timeline examples

### Small migration (dependency upgrade)
```
Day 1: Snapshot + target + gap map
Day 2: Plan + execute (1–3 stages)
Day 3: Cutover + cleanup
```

### Medium migration (framework major version)
```
Week 1: Snapshot + target + gap map + plan
Week 2: Execute stages 1–3
Week 3: Execute stages 4–6 + cutover
Week 4: Monitoring + cleanup
```

### Large migration (platform move)
```
Week 1: Snapshot + target + gap map
Week 2: Plan + initial infrastructure
Week 3–4: Staged migration (data, services, config)
Week 5: Parallel running + testing
Week 6: Cutover + monitoring + cleanup
```
