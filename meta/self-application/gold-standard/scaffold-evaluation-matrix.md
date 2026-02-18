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
| feature-addition | 2 | 1 | 0 | 1 | 0 | 4 | Silver validated | tests + docs only |
| bug-investigation | 2 | 1 | 0 | 1 | 0 | 4 | In progress | [bug-investigation review](reviews/bug-investigation-effectiveness-review.md) |
| testing-retrofit | 2 | 2 | 1 | 2 | 1 | 8 | In progress | self-application run artifacts |
| migration | 2 | 1 | 0 | 1 | 0 | 4 | Silver validated | tests + docs only |
| incident-response | 2 | 1 | 0 | 1 | 0 | 4 | Silver validated | tests + docs only |
| spike | 2 | 1 | 0 | 1 | 0 | 4 | Silver validated | tests + docs only |

## Next recommended order

1. bug-investigation
2. feature-addition
3. incident-response
4. migration
5. refactoring
6. greenfield
7. repo-documentation
8. spike
9. testing-retrofit (finalize from 8 to 9+)
