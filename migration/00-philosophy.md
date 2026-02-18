# 00 — Philosophy: Safe Migrations

## The core insight

Migrations are terrifying because they change the foundation under a running system. The database you depend on, the platform you deploy to, the language version your code runs on — these are the things you trust to be stable. Changing them means temporarily trusting nothing.

The antidote is **incremental transition with verified rollback at every step**. Never change everything at once. Never burn the bridge behind you until you're sure the new bridge holds.

## Principles

### 1. Snapshot before you move

You can't navigate from A to B if you don't know exactly what A is. Before any migration work, capture the complete current state: versions, configurations, data shapes, dependencies, and deployment topology.

"We're running Postgres 14" is not a snapshot. A snapshot is: "Postgres 14.9, 47 tables, 23 indexes, 12 foreign keys, hosted on Render standard plan, 2.3GB data, daily backups retained 7 days."

### 2. Map the gap before crossing it

The compatibility gap map is the most important migration artifact. It's the list of every difference between current state and target state, classified by risk and effort.

```
Current: Python 3.11 + SQLAlchemy 1.4
Target: Python 3.13 + SQLAlchemy 2.0

Gap map:
- 47 deprecated query patterns (Session.query → select())
- 3 removed stdlib modules (imghdr, cgi, lib2to3)
- Type annotation changes (Optional[X] → X | None)
- AsyncIO syntax changes
...
```

### 3. Every stage is reversible

The golden rule of migration: you can always go back. Every stage must have a documented rollback that:
- Has been tested (not just theorized)
- Can be executed quickly (minutes, not hours)
- Preserves data created during the migration period
- Doesn't require heroics (one command, not 20 manual steps)

### 4. Parallel running over hard cutover

When possible, run old and new systems simultaneously:
- Old database alongside new database (with sync)
- Old API alongside new API (with routing)
- Old deployment alongside new deployment (with traffic management)

Parallel running makes rollback trivial: just route back to the old system.

### 5. Data is more precious than code

Code can be rewritten. Data cannot. Every migration stage that touches data must:
- Have a verified backup strategy
- Preserve data integrity (no lost rows, no corrupted values)
- Handle the "data created during migration" window
- Be testable on a copy before running on production

### 6. Migrate in layers, not all at once

The migration stack:

```
1. Infrastructure (platform, hosting, networking)
2. Data (databases, object storage, caches)
3. Dependencies (libraries, language version)
4. Code (syntax updates, API changes)
5. Configuration (env vars, secrets, feature flags)
6. Consumers (API clients, integrations)
```

Migrate one layer at a time. Each layer should work with both old and new versions of adjacent layers during transition.

### 7. Test the migration, not just the result

It's not enough to test that the target state works. You must test that the **transition** works:
- Migration scripts run cleanly
- Data transforms correctly
- Rollback works
- Performance during migration is acceptable
- No downtime (or planned, acceptable downtime)

### 8. Communicate, even if the audience is just you

Document the migration plan, timeline, and status. Even as a solo developer, having a written plan prevents:
- Forgetting where you were
- Skipping steps under pressure
- Making decisions twice
- Not knowing what "done" means

### 9. Time-box the migration

Migrations that drag on become "permanent temporary states" — half-migrated systems that are harder to maintain than either old or new. Set a deadline and work backward:
- Week 1: Snapshot + gap map + plan
- Week 2–3: Staged migration
- Week 4: Cutover + cleanup

If the migration can't fit in a month, it's too big. Decompose into smaller migrations.

### 10. Clean up after yourself

After migration is complete:
- Remove old code/config (don't keep dead paths)
- Delete compatibility shims
- Update documentation
- Archive migration artifacts
- Verify nothing references the old state

The migration isn't done until the old state is fully removed.

---

## Migration types

| Type | Risk level | Example | Key concern |
|------|-----------|---------|-------------|
| **Database upgrade** | High | Postgres 14 → 16 | Data integrity, downtime |
| **Framework upgrade** | Medium | FastAPI 0.100 → 0.115 | Breaking API changes |
| **Language upgrade** | Medium | Python 3.11 → 3.13 | Syntax, stdlib changes |
| **Platform migration** | High | Heroku → Render | Config, networking, secrets |
| **Dependency upgrade** | Low–High | Pydantic v1 → v2 | API surface changes |
| **API versioning** | Medium | v1 → v2 | Consumer coordination |
| **Schema migration** | Medium | Normalize tables | Data transformation |
