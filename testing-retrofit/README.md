# Testing Retrofit Scaffold

> *"How do I add meaningful test coverage to a codebase that has little or none?"*

The **testing-retrofit** scaffold is a structured methodology for systematically adding tests to existing, under-tested codebases. It is the **safety net** companion to the greenfield, feature-addition, and refactoring scaffolds.

---

## When to use this scaffold

- You inherited a codebase with low or no test coverage
- You want to refactor safely but need tests first
- CI has no quality gate — code ships without verification
- You keep regressing on things that should have been caught
- You're adding features to untested code and want confidence

## How to use this scaffold

1. Read [00-philosophy.md](00-philosophy.md) to align on testing principles
2. Use [01-process-overview.md](01-process-overview.md) to understand the lifecycle
3. Run [02-coverage-baseline-checklist.md](02-coverage-baseline-checklist.md) to capture reality
4. Prioritize using [03-test-strategy-guide.md](03-test-strategy-guide.md)
5. Implement by phase using [04-phased-testing-guide.md](04-phased-testing-guide.md)
6. Configure CI gates with [05-ci-integration-and-gates.md](05-ci-integration-and-gates.md)
7. Prepare agent context via [06-agents-md-for-testing.md](06-agents-md-for-testing.md)
8. Use [07-agent-prompts.md](07-agent-prompts.md) to execute the work
9. Track progress with [08-progress-and-quality.md](08-progress-and-quality.md)

## Core lifecycle

| Phase | Question answered | Key output |
|-------|------------------|-----------|
| **Coverage Baseline** | What is the current testing reality? | Coverage report, test inventory |
| **Risk Map** | Where are tests most needed? | Prioritized risk map |
| **Characterization Tests** | What does the code actually do today? | Tests that lock existing behavior |
| **Unit Tests** | Are individual components correct? | Isolated unit tests for high-risk code |
| **Integration Tests** | Do components work together? | Tests for critical paths |
| **CI Gates** | How do we prevent regression? | CI pipeline with coverage thresholds |

---

## Document index

| File | Purpose |
|------|---------|
| [00-philosophy.md](00-philosophy.md) | Core principles for testing retrofit |
| [01-process-overview.md](01-process-overview.md) | Full lifecycle walkthrough |
| [02-coverage-baseline-checklist.md](02-coverage-baseline-checklist.md) | How to assess current test state |
| [03-test-strategy-guide.md](03-test-strategy-guide.md) | Choosing what to test and how |
| [04-phased-testing-guide.md](04-phased-testing-guide.md) | Bottom-up test implementation order |
| [05-ci-integration-and-gates.md](05-ci-integration-and-gates.md) | Setting up CI, coverage gates, quality thresholds |
| [06-agents-md-for-testing.md](06-agents-md-for-testing.md) | How to write AGENTS.md for test work |
| [07-agent-prompts.md](07-agent-prompts.md) | Copy-paste prompts for each phase |
| [08-progress-and-quality.md](08-progress-and-quality.md) | Tracking coverage growth and test quality |

## Templates

| Template | Purpose |
|----------|---------|
| [AGENTS.md.template](templates/AGENTS.md.template) | Agent orientation for testing work |
| [coverage-baseline.md.template](templates/coverage-baseline.md.template) | Current state of testing |
| [risk-priority-map.md.template](templates/risk-priority-map.md.template) | Where tests are most needed |
| [test-pattern-catalog.md.template](templates/test-pattern-catalog.md.template) | Reusable test patterns for the codebase |
| [testing-checklist.md.template](templates/testing-checklist.md.template) | Phase-by-phase progress tracking |
| [coverage-report.md.template](templates/coverage-report.md.template) | Tracking coverage growth over time |
