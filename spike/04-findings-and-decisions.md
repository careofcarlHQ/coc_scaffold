# 04 — Findings and Decisions

> The findings document is the actual deliverable of a spike. Prototype code is ephemeral — the findings are permanent.

---

## Writing the Findings Document

### Structure

The findings document should answer these questions in order:

1. **What was the question?** (from the charter)
2. **What's the answer?** (short version — go / no-go / it depends)
3. **What did you learn?** (detailed findings)
4. **What are the trade-offs?** (pros and cons)
5. **What's the effort estimate?** (if "go")
6. **What remains unknown?** (honestly)

### Be concrete, not abstract

| Abstract (bad) | Concrete (good) |
|----------------|-----------------|
| "Performance was acceptable" | "Average response time: 45ms for 1000-item queries" |
| "Integration was easy" | "Integrated with our auth in 2 hours, no custom code" |
| "The library had issues" | "Crashes on empty input (issue #423, open since 2023)" |
| "It would take a while" | "Estimated 3 days for basic integration, 1 week for full rollout" |

---

## Making the Decision

### Decision types

| Decision | When | Next step |
|----------|------|-----------|
| **Go** | Spike question answered positively, effort is acceptable | Use appropriate scaffold to implement |
| **No-go** | Approach won't work, or cost/effort too high | Archive and move on |
| **Pivot** | Learned something that changes the question | Write a new spike charter |
| **Expand** | Need more information to decide | Write a follow-up spike charter with refined scope |

### Decision criteria

The decision should be based on the charter's success/failure criteria, not on how you feel about the technology. Check each criterion explicitly:

| Criterion | Met? | Evidence |
|-----------|------|---------|
| {Success criterion 1} | Yes / No / Partial | {reference from exploration log} |
| {Success criterion 2} | Yes / No / Partial | {reference} |
| {Success criterion 3} | Yes / No / Partial | {reference} |

### The decision record

Every spike ends with a decision record that future-you can reference:

- **Decision**: {Go / No-go / Pivot}
- **Rationale**: {Why, in 2-3 sentences}
- **Conditions**: {What would change this decision — e.g., "If the library fixes issue #423"}
- **Next actions**: {What happens next — which scaffold, what scope}

---

## Effort Estimation

If the decision is "go," provide an effort estimate for the real implementation:

### Estimation approach

Based on what you learned during the spike, break the real implementation into stages:

| Stage | Description | Estimated effort | Confidence |
|-------|------------|-----------------|------------|
| 1 | {Foundation / setup} | {hours/days} | {high/med/low} |
| 2 | {Core implementation} | {hours/days} | {confidence} |
| 3 | {Integration} | {hours/days} | {confidence} |
| 4 | {Testing} | {hours/days} | {confidence} |
| 5 | {Deployment} | {hours/days} | {confidence} |

### Confidence levels

- **High**: Did something very similar during the spike. Solid understanding.
- **Medium**: Partially explored during spike. Known unknowns remain.
- **Low**: Extrapolating from spike findings. Unknown unknowns likely.

### Uncertainty multiplier

| Confidence | Estimated | Budget |
|-----------|-----------|--------|
| High | X hours | 1.2x |
| Medium | X hours | 1.5x |
| Low | X hours | 2x |

---

## Comparison Findings

When comparing multiple approaches, structure the findings as a comparison matrix:

### Comparison table

| Criterion | Approach A | Approach B | Approach C |
|-----------|-----------|-----------|-----------|
| Performance | {finding} | {finding} | {finding} |
| Complexity | {finding} | {finding} | {finding} |
| Maintainability | {finding} | {finding} | {finding} |
| Integration effort | {finding} | {finding} | {finding} |
| Risk | {finding} | {finding} | {finding} |
| **Score** | **{N}** | **{N}** | **{N}** |

### Winner and rationale

**Recommended**: Approach {X}

**Why**: {2-3 sentences explaining the recommendation}

**Caveat**: {Any conditions or concerns about the recommendation}

---

## Handling "inconclusive" results

Sometimes a spike doesn't give a clear answer. That's fine — document it honestly:

1. **What you know**: {facts established by the spike}
2. **What you don't know**: {questions that remain}
3. **Why it's inconclusive**: {what prevented a clear answer — time? complexity? external factor?}
4. **Recommendation**: {follow-up spike with refined question? go with available info? abandon?}

An honest "inconclusive" is far more useful than a false "go" or "no-go."
