# Framework Gold Standard Definition

## Rating levels

- `Bronze`: structure exists, but quality controls are weak or missing
- `Silver`: structure + automated integrity checks pass consistently
- `Gold`: silver + proven effectiveness in realistic execution

## Gold criteria (all required)

1. **Structural integrity**
   - Scaffold passes all repository contract tests
   - Required guides/templates/links are complete
2. **Operator clarity**
   - README + AGENTS template provide unambiguous run order
   - Safety constraints and done criteria are explicit
3. **Execution effectiveness**
   - At least one realistic run demonstrates successful outcome
   - Run includes evidence artifacts and gate outputs
4. **Safety resilience**
   - Failure paths handled with explicit rollback/abort behavior
   - No unsafe shortcuts required for normal use
5. **Reproducibility**
   - Different sessions/operators can repeat the flow with equivalent result
   - Evidence is stored and referenceable in-repo

## Scoring model

Each criterion is scored:

- `0` = not satisfied
- `1` = partially satisfied
- `2` = satisfied with evidence

Maximum score: `10`.

## Gold threshold

A scaffold is `Gold` when:

- score is `>= 9/10`, and
- criterion 3 (Execution effectiveness) is `2`, and
- criterion 4 (Safety resilience) is `2`.
