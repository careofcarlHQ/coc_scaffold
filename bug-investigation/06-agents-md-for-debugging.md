# 06 — Writing AGENTS.md for Bug Investigation

## Purpose

When assigning a bug to an agent, provide a focused brief that orients the agent on the investigation. The agent needs: what's broken, what's been tried, and what the rules are.

## Bug investigation brief

Create `bugfix/AGENTS-BRIEF.md` for each investigation:

```markdown
# Bug Investigation Brief — [Bug Title]

## Symptom
[One-paragraph description of what's happening]

## Expected behavior
[What should happen instead]

## Read these files (in order)
1. `AGENTS.md` (project-level rules)
2. `bugfix/symptom-capture.md` (detailed symptom)
3. `bugfix/hypothesis-log.md` (what's been tried — DON'T repeat dead ends)

## Key constraints
- Do NOT fix anything without writing a regression test first
- Do NOT refactor while fixing — one purpose per change
- Do NOT modify existing tests to make them pass
- Run the full test suite after applying any fix
- Document every hypothesis in the hypothesis log

## Investigation status
- [ ] Symptom captured
- [ ] Bug reproduced
- [ ] Problem isolated
- [ ] Root cause identified
- [ ] Fix specified
- [ ] Fix implemented
- [ ] Fix verified

## Current phase
[Which phase of the investigation you're in]

## Dead ends (do not re-investigate)
- [hypothesis that was already tested and rejected]
```

## When to create vs. skip the brief

| Situation | Action |
|-----------|--------|
| Bug takes > 30 minutes | Create a brief |
| Bug spans multiple agent sessions | Create a brief |
| Bug has been investigated before | Create a brief (capture dead ends!) |
| Trivial 5-minute fix | Skip — just fix and test |

## Lifecycle

```
Bug reported   → Create bugfix/AGENTS-BRIEF.md + symptom-capture.md
Investigation  → Update hypothesis-log.md as hypotheses are tested
Fix ready      → Create fix-spec.md
Fix merged     → Delete bugfix/ artifacts (or archive in docs/bugfixes/)
```

## Tips for effective agent debugging

1. **Pre-populate dead ends**: If you've already investigated and ruled things out, tell the agent. This prevents the agent from going in circles.

2. **Provide reproduction steps**: Agents can run tests and commands, but they need exact steps.

3. **Point to relevant code**: If you suspect a specific area, say so. "Start looking at `app/services/export.py`" saves the agent from searching the whole codebase.

4. **Set a time box**: "Spend 30 minutes on diagnosis. If you haven't found the root cause, report what you've learned and stop."
