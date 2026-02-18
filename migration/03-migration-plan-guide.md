# 03 — Migration Plan Guide

## Purpose

A migration plan translates the gap map into an executable sequence of stages. Each stage is independently deployable, independently reversible, and independently verifiable.

## Planning principles

### 1. Lowest risk first

Start with changes that have the smallest blast radius. Build confidence before tackling the hard parts.

```
Stage 1: Update development tooling (no production impact)
Stage 2: Add compatibility shims (no behavior change)
Stage 3: Migrate configuration (low-risk, easy rollback)
Stage 4: Migrate data layer (high-risk, careful verification)
Stage 5: Migrate application code (medium-risk)
Stage 6: Cutover infrastructure (high-risk, monitored)
```

### 2. One layer per stage

Don't migrate the database and the framework in the same stage. Isolate changes so failures are attributable to a single cause.

### 3. Compatibility windows

During migration, the system must support both old and new states simultaneously:
- Code should work with both old and new database schemas
- APIs should handle both old and new request formats
- Configuration should have fallbacks to old values

### 4. Parallel running strategy

Where possible, run old and new simultaneously:

```
┌──────────────┐     ┌──────────────┐
│  Old System  │────→│   Traffic    │
│  (primary)   │     │   Router     │────→ Users
│              │     │              │
│  New System  │────→│  (can switch │
│  (shadow)    │     │   instantly) │
└──────────────┘     └──────────────┘
```

## Migration plan structure

### 1. Migration overview

```markdown
## Migration: {name}

### From
{current state summary — one line per layer}

### To
{target state summary — one line per layer}

### Motivation
{Why now? What triggers the migration?}

### Timeline
- Planning: {dates}
- Execution: {dates}
- Cutover: {date}
- Cleanup: {date}
- Total: {duration}

### Abort criteria
Stop the migration and reconsider if:
- {condition 1: e.g., more than 3 stages fail on first attempt}
- {condition 2: e.g., total timeline exceeds estimate by 2x}
- {condition 3: e.g., data integrity issue discovered}
```

### 2. Stage definitions

For each stage:

```markdown
### Stage N — {Name}

**What changes**: {Brief description}
**Layers affected**: {infrastructure / data / dependencies / code / config / consumers}
**Risk**: low / medium / high
**Estimated effort**: {hours}
**Dependencies**: Stage N-1 (or "none")

**Changes**:
- {Specific change 1}
- {Specific change 2}

**Verification**:
- {How to confirm the stage succeeded}

**Rollback**:
- {Exact steps to undo this stage}

**Rollback tested**: yes / no / N/A
```

### 3. Stage ordering

Typical ordering for different migration types:

#### Dependency upgrade
```
Stage 1: Add compatibility layer / shims
Stage 2: Update development dependency (local testing)
Stage 3: Fix deprecation warnings
Stage 4: Update production dependency
Stage 5: Remove compatibility shims
Stage 6: Cleanup
```

#### Platform migration
```
Stage 1: Set up target platform (empty)
Stage 2: Deploy application to target (non-production)
Stage 3: Migrate configuration and secrets
Stage 4: Migrate database (copy or sync)
Stage 5: Verify application on target
Stage 6: Switch DNS / traffic routing
Stage 7: Decommission old platform
```

#### Database major version upgrade
```
Stage 1: Test application against new DB version (local/CI)
Stage 2: Fix any incompatibilities
Stage 3: Set up new DB instance
Stage 4: Configure replication (old → new)
Stage 5: Verify data sync
Stage 6: Switch application to new DB
Stage 7: Monitor for issues
Stage 8: Decommission old DB
```

## Gap-to-stage mapping

For each gap in your gap map, assign it to a stage:

```markdown
## Gap → Stage Mapping

| Gap | Risk | Effort | Stage | Notes |
|-----|------|--------|-------|-------|
| {gap 1} | low | 1h | Stage 1 | {notes} |
| {gap 2} | medium | 4h | Stage 3 | Depends on gap 1 |
| {gap 3} | high | 2h | Stage 4 | Needs careful testing |
```

All gaps must be assigned. If a gap isn't addressed, document why (accepted risk, deferred, not applicable).

## Verification strategy

Each stage must have a verification that confirms:
1. The change was applied correctly
2. The system still works (tests pass)
3. Rollback is possible

```markdown
## Verification per stage

| Stage | Automated test | Manual check | Rollback test |
|-------|---------------|--------------|---------------|
| 1 | `pytest` passes | App starts | Revert commit |
| 2 | CI pipeline green | Deploy succeeds | Redeploy old version |
| 3 | DB queries work | Data intact | Restore from backup |
```
