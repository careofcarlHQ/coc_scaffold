# Scaffold Evaluation Matrix

## Status legend

- `Not started`
- `In progress`
- `Silver validated`
- `Gold validated`

## Current baseline

Structural/contract tests are green repository-wide.
Effectiveness evidence is strongest for PR merge automation and still incomplete for most scaffolds.

| Scaffold | Structural integrity | Operator clarity | Effectiveness evidence | Safety resilience | Reproducibility | Score | Status | Evidence |
|---|---:|---:|---:|---:|---:|---:|---|---|
| greenfield | 2 | 1 | 0 | 1 | 0 | 4 | Silver validated | tests + docs only |
| repo-documentation | 2 | 1 | 0 | 1 | 0 | 4 | Silver validated | tests + docs only |
| refactoring | 2 | 1 | 0 | 1 | 0 | 4 | Silver validated | tests + docs only |
| feature-addition | 2 | 2 | 2 | 2 | 1 | 9 | In progress | [feature-addition review](reviews/feature-addition-effectiveness-review.md), [run-001](executions/feature-addition/run-001/run-summary.md) |
| bug-investigation | 2 | 2 | 2 | 2 | 2 | 10 | Gold validated | [bug-investigation review](reviews/bug-investigation-effectiveness-review.md), [run-001](executions/bug-investigation/run-001/run-summary.md), [run-002](executions/bug-investigation/run-002/run-summary.md) |
| testing-retrofit | 2 | 2 | 1 | 2 | 1 | 8 | In progress | self-application run artifacts |
| migration | 2 | 1 | 0 | 1 | 0 | 4 | Silver validated | tests + docs only |
| incident-response | 2 | 1 | 0 | 1 | 0 | 4 | Silver validated | tests + docs only |
| spike | 2 | 1 | 0 | 1 | 0 | 4 | Silver validated | tests + docs only |

## Next recommended order

1. incident-response
2. migration
3. refactoring
4. greenfield
5. repo-documentation
6. spike
7. testing-retrofit (finalize from 8 to 9+)
8. feature-addition (run-002 for reproducibility)
