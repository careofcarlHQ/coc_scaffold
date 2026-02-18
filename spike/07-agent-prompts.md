# 07 — Agent Prompts

> Copy-paste prompts for each phase of a spike. Spike prompts are deliberately looser than other scaffolds — exploration needs room to breathe.

---

## Prompt 1: Research Phase

```
Read the AGENTS.md and the spike charter at temp/spike-{name}/charter.md.

Research phase — DO NOT write code yet.

1. Read the official documentation for {technology/approach}
2. Find and review:
   - Getting started guide
   - API reference (skim for scope and capabilities)
   - Known limitations or breaking changes
   - GitHub issues (common problems)
3. Assess compatibility with our stack:
   - Python version: {version}
   - Framework: {framework}
   - Deployment: {platform}
4. Find 2-3 example implementations relevant to our use case

Document everything in temp/spike-{name}/exploration-log.md.

Report:
- Key capabilities relevant to our question
- Potential blockers or concerns
- Your recommendation: proceed to prototype? Or no-go already?
```

---

## Prompt 2: Prototype — Single Approach

```
Read the AGENTS.md and the exploration log at temp/spike-{name}/exploration-log.md.

Build a proof of concept in temp/spike-{name}/.

The question: {spike question from charter}

Build the SIMPLEST thing that answers this question:
1. Set up a minimal working example
2. Test the core capability (the one that matters for our question)
3. If it works, push slightly further — test one edge case
4. If it doesn't work, try ONE alternative approach
5. Measure {what to measure: performance, complexity, compatibility}

Rules:
- Work ONLY in temp/spike-{name}/
- Hardcode values, skip tests, skip error handling
- Speed over quality — this is throwaway code
- Document everything in the exploration log

Report:
- Does it work for our use case? Yes/No/Partially
- What surprised you?
- What's the effort estimate for a real implementation?
```

---

## Prompt 3: Prototype — Compare Approaches

```
Read the AGENTS.md and the spike charter at temp/spike-{name}/charter.md.

Compare these approaches by prototyping each:

Approach A: {description}
Approach B: {description}
{Approach C: {description} — if applicable}

For each approach:
1. Build a minimal prototype in temp/spike-{name}/{approach}/
2. Test against this scenario: {common test scenario}
3. Measure: {criteria from charter}
4. Note: difficulty, surprises, gotchas

Give each approach roughly equal time ({time per approach}).

Document in the exploration log: what you tried, what happened, measurements.

At the end, score each approach:
| Criterion | Weight | Approach A | Approach B |
|-----------|--------|-----------|-----------|
| {criterion} | {weight} | {score/5} | {score/5} |

Recommend the winner with reasoning.
```

---

## Prompt 4: Write Findings Document

```
Read the exploration log at temp/spike-{name}/exploration-log.md
and review the prototype code at temp/spike-{name}/.

Write the findings document at temp/spike-{name}/findings.md.

Structure:
1. Question: {restate from charter}
2. Answer: {Go / No-go / Inconclusive — one sentence}
3. Summary of findings (2-3 paragraphs)
4. What worked
5. What didn't work
6. Trade-offs discovered
7. Effort estimate for real implementation (if "go"):
   | Stage | Description | Effort | Confidence |
   |-------|------------|--------|------------|
8. Remaining unknowns
9. References (docs, examples, issues that were useful)

Be concrete: include numbers, measurements, and specific observations.
Avoid vague statements like "performance was good" — say "45ms average response."
```

---

## Prompt 5: Write Decision Record

```
Read the spike charter and findings document.

Write the decision record at temp/spike-{name}/decision.md.

Include:
1. Decision: Go / No-go / Pivot / Expand
2. Summary: one paragraph explaining the decision
3. Criteria evaluation:
   | Criterion | Met? | Evidence |
   |-----------|------|---------|
   {evaluate each success criterion from the charter}
4. Rationale: why this decision (2-3 sentences)
5. Conditions: what would change this decision
6. Next actions:
   - If go: which scaffold to use, scope of first phase
   - If no-go: what to do instead
   - If pivot: what the new spike question should be
```

---

## Prompt 6: Cleanup and Archive

```
The spike {name} is complete. Decision: {go/no-go/pivot}.

Clean up and archive:

1. Ensure all documents exist in temp/spike-{name}/:
   - charter.md
   - exploration-log.md
   - findings.md
   - decision.md
2. If prototype code is worth keeping:
   - Add a README.md explaining how to run it
   - Remove any hardcoded secrets
3. Clean up:
   - Remove temporary credentials or .env files
   - Remove downloaded large files
   - Remove dependency directories (node_modules, .venv)
4. Move the spike directory to spikes/{name}/
   (or leave in temp/ if you prefer — but make sure it's findable)
5. Update the spikes index if one exists

Report what was archived and what was cleaned up.
```
