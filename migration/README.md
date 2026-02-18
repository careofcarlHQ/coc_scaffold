# Migration Scaffold

A reusable framework for safely migrating between states — database upgrades, dependency bumps, platform moves, API version transitions, and framework upgrades. The transitional companion to the [refactoring scaffold](../refactoring/) and [feature-addition scaffold](../feature-addition/).

Where refactoring reshapes code **without changing behavior**, and features add **new behavior**, migrations change the **environment, platform, or foundation** the code runs on.

## Who is this for?

Any developer or team that:

- Needs to upgrade a database, programming language, or framework version
- Is moving between hosting platforms (e.g., Heroku → Render)
- Needs to migrate an API to a new version with consumer transition
- Is upgrading critical dependencies with breaking changes
- Wants a systematic approach to "swap the engine while the car is running"

## What makes this approach different?

1. **Current-state snapshot before target-state planning** — know exactly what you have
2. **Compatibility gap map** — identify every break point between current and target state
3. **Every stage is independently deployable and rollback-safe** — never all-or-nothing
4. **Parallel running where possible** — old and new coexist during transition
5. **Cutover as a distinct phase** — the switch from old to new is planned, not accidental

## How to use this scaffold

1. Read [00-philosophy.md](00-philosophy.md) to understand the principles
2. Read [01-process-overview.md](01-process-overview.md) for the end-to-end workflow
3. Snapshot current state using [02-current-state-assessment.md](02-current-state-assessment.md)
4. Plan the migration with [03-migration-plan-guide.md](03-migration-plan-guide.md)
5. Execute using [04-phased-migration-guide.md](04-phased-migration-guide.md)
6. Manage risk with [05-rollback-and-safety.md](05-rollback-and-safety.md)
7. Write the agent entry point with [06-agents-md-for-migrations.md](06-agents-md-for-migrations.md)
8. Use [07-agent-prompts.md](07-agent-prompts.md) for automated analysis and execution
9. Track progress with [08-progress-and-quality.md](08-progress-and-quality.md)

## Document Index

| File | Purpose |
|------|---------|
| [00-philosophy.md](00-philosophy.md) | Core principles for safe migrations |
| [01-process-overview.md](01-process-overview.md) | End-to-end migration workflow |
| [02-current-state-assessment.md](02-current-state-assessment.md) | Snapshot what you have today |
| [03-migration-plan-guide.md](03-migration-plan-guide.md) | Design the transition strategy |
| [04-phased-migration-guide.md](04-phased-migration-guide.md) | Staged execution with safety gates |
| [05-rollback-and-safety.md](05-rollback-and-safety.md) | Rollback plans and risk management |
| [06-agents-md-for-migrations.md](06-agents-md-for-migrations.md) | Writing AGENTS.md for a migration |
| [07-agent-prompts.md](07-agent-prompts.md) | Concrete prompts for automated migration |
| [08-progress-and-quality.md](08-progress-and-quality.md) | Tracking and verification |
| [templates/](templates/) | Copy-paste starter templates |

## Templates

| Template | Purpose |
|----------|---------|
| [AGENTS.md.template](templates/AGENTS.md.template) | Agent entry point for a migration |
| [current-state-snapshot.md.template](templates/current-state-snapshot.md.template) | What we have today |
| [target-state-definition.md.template](templates/target-state-definition.md.template) | Where we're going |
| [compatibility-gap-map.md.template](templates/compatibility-gap-map.md.template) | What breaks between current and target |
| [migration-checklist.md.template](templates/migration-checklist.md.template) | Staged execution with gates |
| [rollback-plan.md.template](templates/rollback-plan.md.template) | How to undo each stage |
| [cutover-checklist.md.template](templates/cutover-checklist.md.template) | The switch from old to new |

## Relationship to the Other Scaffolds

```
migration/ (transitional)     refactoring/ (lateral)        feature-addition/ (forward)
─────────────────────────     ────────────────────────      ──────────────────────────
Current → Gap → Target        Code → Analyze → Reshape      Impact → Spec → Build
"How do we get from A to B?"  "How should we reshape?"       "What should we add?"
Foundation changes             Structure changes              Behavior changes
Platform/version/infra         Code organization              New capabilities
```

## Origin

Built as part of the agent-first scaffold family, based on the experience of migrating `coc_capi` across platform moves, dependency upgrades, and database schema evolutions while maintaining production stability.
