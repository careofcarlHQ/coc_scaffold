# Code Refactoring Scaffold

A reusable framework for systematically refactoring existing codebases — the lateral companion to the [greenfield project scaffold](../greenfield/) and [repo documentation scaffold](../repo-documentation/).

Where the project scaffold goes **forward** (design → build) and the documentation scaffold goes **backward** (code → document), this framework works **laterally** (code → analyze → reshape). It gives you a repeatable process for transforming working code into better-structured, more maintainable code — driven by agent-human collaboration.

## Who is this for?

Any developer or team that:

- Has a working codebase that has grown organically and needs structural improvement
- Wants to reduce technical debt without introducing regressions
- Needs to restructure code to support new features or scaling requirements
- Wants to migrate between patterns, frameworks, or architectures
- Needs a disciplined approach to large refactors that doesn't stall or break things

## What makes this approach different?

1. **Working code is sacred** — the system works today; refactoring must preserve that
2. **Evidence-driven scope** — measure the pain before prescribing the cure
3. **Incremental transformation** — small, verifiable steps; never a big bang rewrite
4. **Behavior preservation first** — characterization tests before structural changes
5. **Agent executes, human steers** — agents do the mechanical work; humans set direction and approve

## How to use this scaffold

1. Read [00-philosophy.md](00-philosophy.md) to understand the principles
2. Read [01-process-overview.md](01-process-overview.md) for the end-to-end workflow
3. Run the [02-codebase-assessment-checklist.md](02-codebase-assessment-checklist.md) against your repo
4. Use [03-refactoring-plan-guide.md](03-refactoring-plan-guide.md) to design your transformation
5. Execute using [04-phased-refactoring-guide.md](04-phased-refactoring-guide.md)
6. Maintain with [05-validation-and-safety.md](05-validation-and-safety.md)
7. Write the agent entry point with [06-agents-md-for-refactoring.md](06-agents-md-for-refactoring.md)
8. Use [07-agent-prompts.md](07-agent-prompts.md) for automated analysis and execution
9. Track progress with [08-progress-and-quality.md](08-progress-and-quality.md)

## Document Index

| File | Purpose |
|------|---------|
| [00-philosophy.md](00-philosophy.md) | Core principles for safe, incremental refactoring |
| [01-process-overview.md](01-process-overview.md) | End-to-end refactoring workflow |
| [02-codebase-assessment-checklist.md](02-codebase-assessment-checklist.md) | Systematic audit of current code health |
| [03-refactoring-plan-guide.md](03-refactoring-plan-guide.md) | How to design a refactoring plan agents can execute |
| [04-phased-refactoring-guide.md](04-phased-refactoring-guide.md) | Phased execution with safety gates |
| [05-validation-and-safety.md](05-validation-and-safety.md) | Test strategies, rollback plans, regression prevention |
| [06-agents-md-for-refactoring.md](06-agents-md-for-refactoring.md) | Writing AGENTS.md for a refactoring project |
| [07-agent-prompts.md](07-agent-prompts.md) | Concrete analysis and refactoring prompts for agents |
| [08-progress-and-quality.md](08-progress-and-quality.md) | Metrics, tracking, and quality gates |
| [templates/](templates/) | Copy-paste starter templates |

## Templates

| Template | Purpose |
|----------|---------|
| [AGENTS.md.template](templates/AGENTS.md.template) | Agent entry point for a refactoring project |
| [codebase-assessment.md.template](templates/codebase-assessment.md.template) | Code health audit results |
| [refactoring-plan.md.template](templates/refactoring-plan.md.template) | Transformation plan with scope and phases |
| [refactoring-checklist.md.template](templates/refactoring-checklist.md.template) | Phase checklist with safety gates |
| [refactoring-log.md.template](templates/refactoring-log.md.template) | Progress tracking per stage |
| [characterization-test-plan.md.template](templates/characterization-test-plan.md.template) | Behavior preservation test strategy |
| [migration-map.md.template](templates/migration-map.md.template) | Old structure → new structure mapping |
| [risk-register.md.template](templates/risk-register.md.template) | Known risks and mitigation strategies |
| [rollback-plan.md.template](templates/rollback-plan.md.template) | How to undo each refactoring step |
| [verify-baseline.ps1.template](templates/verify-baseline.ps1.template) | Single-command baseline verification script |

## Relationship to the Other Scaffolds

```
Greenfield (forward)          Repo Documentation (backward)     Refactoring (lateral)
────────────────────          ───────────────────────────────    ─────────────────────
PRD → Specs → Code            Code → Discovery → Docs           Code → Analysis → Better Code
"What should we build?"       "What do we actually have?"        "How should we reshape this?"
Design-first                  Evidence-first                     Safety-first
Creates new repos             Documents existing repos           Transforms existing repos
```

All three frameworks share the same core values:
- Repository as system of record
- AGENTS.md as navigation entry point
- Progressive disclosure over front-loading
- Objective quality gates over subjective judgment
- Human steers, agent executes

## Origin

Built as the third companion in the agent-first scaffold family, based on the experience of evolving `coc_capi` — a production FastAPI service that grew organically and needed systematic structural improvement while maintaining production stability.
