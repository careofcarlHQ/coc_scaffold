# Feature Addition Scaffold

A reusable framework for safely adding new capabilities to existing, working systems — the incremental forward companion to the [greenfield project scaffold](../greenfield/) and [refactoring scaffold](../refactoring/).

Where the project scaffold goes **forward** from zero (design → build), and refactoring goes **laterally** (reshape without new behavior), this framework handles the most common daily work: adding something new to something that already works.

## Who is this for?

Any developer or team that:

- Has a running production system and needs to extend it
- Wants to add features without breaking existing behavior
- Needs a repeatable process for "what does this feature touch?"
- Wants agents to implement features confidently within existing constraints
- Needs to balance speed of delivery with safety of existing functionality

## What makes this approach different?

1. **Impact analysis before implementation** — understand what you're touching before you touch it
2. **Feature specs, not full PRDs** — scoped contracts for the delta, not the whole system
3. **Compatibility-first** — existing consumers, data shapes, and APIs are protected by default
4. **Incremental build order** — database → service → API → UI, always
5. **Rollout gates** — migration safety and feature flags before full exposure

## How to use this scaffold

1. Read [00-philosophy.md](00-philosophy.md) to understand the principles
2. Read [01-process-overview.md](01-process-overview.md) for the end-to-end workflow
3. Run the [02-impact-analysis-checklist.md](02-impact-analysis-checklist.md) against your planned feature
4. Write your feature spec using [03-feature-spec-guide.md](03-feature-spec-guide.md)
5. Build using [04-phased-implementation-guide.md](04-phased-implementation-guide.md)
6. Verify and roll out with [05-verification-and-rollout.md](05-verification-and-rollout.md)
7. Write the agent entry point with [06-agents-md-for-features.md](06-agents-md-for-features.md)
8. Use [07-agent-prompts.md](07-agent-prompts.md) for automated analysis and implementation
9. Track progress with [08-progress-and-quality.md](08-progress-and-quality.md)

## Document Index

| File | Purpose |
|------|---------|
| [00-philosophy.md](00-philosophy.md) | Core principles for safe incremental feature work |
| [01-process-overview.md](01-process-overview.md) | End-to-end feature addition workflow |
| [02-impact-analysis-checklist.md](02-impact-analysis-checklist.md) | Systematic audit of what a feature touches |
| [03-feature-spec-guide.md](03-feature-spec-guide.md) | How to write a scoped feature spec |
| [04-phased-implementation-guide.md](04-phased-implementation-guide.md) | Build order with acceptance gates |
| [05-verification-and-rollout.md](05-verification-and-rollout.md) | Testing, compatibility verification, rollout strategy |
| [06-agents-md-for-features.md](06-agents-md-for-features.md) | Writing AGENTS.md for feature work |
| [07-agent-prompts.md](07-agent-prompts.md) | Concrete prompts for analysis and implementation |
| [08-progress-and-quality.md](08-progress-and-quality.md) | Tracking and quality gates |
| [templates/](templates/) | Copy-paste starter templates |

## Templates

| Template | Purpose |
|----------|---------|
| [AGENTS.md.template](templates/AGENTS.md.template) | Agent entry point for a feature addition |
| [impact-analysis.md.template](templates/impact-analysis.md.template) | What does this feature touch? |
| [feature-spec.md.template](templates/feature-spec.md.template) | Scoped contract for the new capability |
| [feature-checklist.md.template](templates/feature-checklist.md.template) | Implementation stages with gates |
| [compatibility-check.md.template](templates/compatibility-check.md.template) | API/data/behavior compatibility verification |
| [rollout-plan.md.template](templates/rollout-plan.md.template) | Migration and rollout strategy |

## Relationship to the Other Scaffolds

```
spike/ (investigate)          greenfield/ (forward)          feature-addition/ (incremental)
────────────────────          ─────────────────────          ────────────────────────────────
Question → Answer             PRD → Specs → Code             Impact → Spec → Build → Verify
"Can we do this?"             "Build from zero"               "Add to what exists"
Time-boxed research           Design-first                    Compatibility-first
No production code            Creates new repos               Extends working systems
```

## Origin

Built as part of the agent-first scaffold family, based on the experience of iteratively extending `coc_capi` — adding new endpoints, background jobs, admin UI features, and external integrations to a running production system while preserving existing behavior.
