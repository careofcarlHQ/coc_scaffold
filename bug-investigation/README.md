# Bug Investigation Scaffold

A reusable framework for systematically diagnosing and fixing bugs — the diagnostic companion to the [feature-addition scaffold](../feature-addition/) and [refactoring scaffold](../refactoring/).

Where feature addition goes forward and refactoring goes laterally, bug investigation works **inward** — drilling from symptoms to root causes with structured methodology instead of ad-hoc flailing.

## Who is this for?

Any developer or team that:

- Wastes time debugging without a systematic approach
- Wants agents to investigate bugs effectively instead of guessing randomly
- Needs to prevent the same class of bug from recurring
- Wants a traceable record of what was tried and why
- Has bugs that resist quick fixes and require deep investigation

## What makes this approach different?

1. **Hypothesis-driven investigation** — structured "I think X because Y, test by Z" instead of random exploration
2. **Reproduction before diagnosis** — if you can't reproduce it, you can't fix it
3. **Root cause, not symptoms** — fix the underlying problem, not just the visible error
4. **Regression guard mandatory** — every fix produces a test that would have caught it
5. **Investigation artifacts preserved** — dead ends are documented so nobody repeats them

## How to use this scaffold

1. Read [00-philosophy.md](00-philosophy.md) to understand the principles
2. Read [01-process-overview.md](01-process-overview.md) for the end-to-end workflow
3. Capture the symptom using [02-symptom-capture-guide.md](02-symptom-capture-guide.md)
4. Reproduce and isolate with [03-reproduction-and-isolation.md](03-reproduction-and-isolation.md)
5. Diagnose using [04-diagnosis-workflow.md](04-diagnosis-workflow.md)
6. Fix and verify with [05-fix-and-verify.md](05-fix-and-verify.md)
7. Write the agent entry point with [06-agents-md-for-debugging.md](06-agents-md-for-debugging.md)
8. Use [07-agent-prompts.md](07-agent-prompts.md) for automated investigation
9. Track quality with [08-post-fix-quality.md](08-post-fix-quality.md)

## Document Index

| File | Purpose |
|------|---------|
| [00-philosophy.md](00-philosophy.md) | Core principles for systematic debugging |
| [01-process-overview.md](01-process-overview.md) | End-to-end investigation workflow |
| [02-symptom-capture-guide.md](02-symptom-capture-guide.md) | How to capture bug symptoms accurately |
| [03-reproduction-and-isolation.md](03-reproduction-and-isolation.md) | Reproducing and narrowing down the problem |
| [04-diagnosis-workflow.md](04-diagnosis-workflow.md) | Hypothesis-driven root cause analysis |
| [05-fix-and-verify.md](05-fix-and-verify.md) | Implementing and verifying the fix |
| [06-agents-md-for-debugging.md](06-agents-md-for-debugging.md) | Writing AGENTS.md for bug investigation |
| [07-agent-prompts.md](07-agent-prompts.md) | Concrete prompts for automated investigation |
| [08-post-fix-quality.md](08-post-fix-quality.md) | Regression guards, post-fix review, prevention |
| [templates/](templates/) | Copy-paste starter templates |

## Templates

| Template | Purpose |
|----------|---------|
| [AGENTS.md.template](templates/AGENTS.md.template) | Agent entry point for bug investigation |
| [symptom-capture.md.template](templates/symptom-capture.md.template) | Structured bug report |
| [hypothesis-log.md.template](templates/hypothesis-log.md.template) | Track theories and test results |
| [root-cause-analysis.md.template](templates/root-cause-analysis.md.template) | Document the actual root cause |
| [fix-spec.md.template](templates/fix-spec.md.template) | Plan the fix before implementing |
| [regression-test-plan.md.template](templates/regression-test-plan.md.template) | Tests that prevent recurrence |

## Relationship to the Other Scaffolds

```
bug-investigation/ (inward)      feature-addition/ (forward)        refactoring/ (lateral)
──────────────────────────       ──────────────────────────         ────────────────────────
Symptom → Root Cause → Fix       Impact → Spec → Build              Code → Analyze → Reshape
"Why is this broken?"            "What should we add?"               "How should we restructure?"
Hypothesis-driven                Compatibility-first                 Safety-first
Fixes existing behavior          Adds new behavior                   Preserves behavior
```

## Origin

Built as part of the agent-first scaffold family, based on the experience of diagnosing and fixing production bugs in `coc_capi` — where structured investigation saved hours compared to ad-hoc debugging sessions.
