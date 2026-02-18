# 01 — Process Overview

> From question to decision, in a controlled explosion of exploration.

---

## The Spike Lifecycle

```
Charter → Exploration → Prototype → Findings → Decision → Cleanup
   │          │            │           │          │          │
 Define     Research     Build       Document   Go/no-go   Archive
 the        & try       a proof     what you   / pivot    or discard
 question   things      of concept  learned
```

Each phase has a clear deliverable. The spike is complete when a decision is made — whether that's "go," "no-go," or "we need a different spike."

---

## Phase 1: Charter

**Goal**: Define exactly what you're exploring and set constraints.

**Activities**:
- Write the spike question (specific, answerable, scoped)
- Define success criteria (what does a positive answer look like?)
- List what you're NOT exploring (scope boundaries)
- Set the time box (hours or days)
- Identify what you need to start (accounts, access, docs)

**Output**: `spike-charter.md` — the contract for this exploration.

**Gate**: The question is specific, the time box is set, and success criteria are defined.

---

## Phase 2: Exploration

**Goal**: Research the topic, read documentation, gather information.

**Activities**:
- Read official documentation for the technology/approach
- Find examples, tutorials, blog posts
- Identify limitations, gotchas, known issues
- Compare with alternatives (if the spike is about choosing)
- Note architectural implications for your project
- Keep a running exploration log

**Output**: Exploration log with notes, links, and initial impressions.

**Gate**: You understand enough to build a proof of concept.

---

## Phase 3: Prototype

**Goal**: Build a minimal proof of concept that answers the spike question.

**Activities**:
- Build the simplest possible thing that tests the core question
- Use hardcoded values, skip tests, skip error handling
- If it works, push a *little* further to find the edges
- If it doesn't work, try one alternative approach before concluding
- Track all experiments in the exploration log

**Output**: Working (or failed) proof of concept. Updated exploration log.

**Gate**: You have enough evidence to answer the spike question.

### Prototype rules
- Build in an isolated directory (not in the main codebase)
- Don't install anything in the main project
- Hardcode credentials in the prototype only (never commit real secrets)
- 30% of the time box should be reserved for documentation and decision

---

## Phase 4: Findings

**Goal**: Document what you learned — the actual deliverable of the spike.

**Activities**:
- Summarize the answer to the spike question
- Document what worked and what didn't
- List technical trade-offs discovered
- Estimate effort for a real implementation (if "go")
- Document unknowns that remain
- Reference the exploration log for details

**Output**: `findings-document.md` — structured summary of everything learned.

**Gate**: Someone who wasn't part of the spike can understand the findings and trade-offs.

---

## Phase 5: Decision

**Goal**: Make a go/no-go/pivot decision based on the findings.

**Activities**:
- Review findings against the original success criteria
- Consider effort vs. value
- Consider risks and unknowns
- Decide: go (proceed to implementation), no-go (abandon this approach), or pivot (run a follow-up spike with a refined question)
- If "go": identify next steps using the appropriate scaffold (feature-addition, greenfield, migration)

**Output**: `decision-record.md` — the decision and rationale.

**Gate**: A clear decision with reasoning that can be reviewed later.

---

## Phase 6: Cleanup

**Goal**: Archive useful artifacts and clean up exploratory code.

**Activities**:
- Move artifacts to a findable archive location
- Tag or label the spike for future reference
- If "go": write a brief for the implementation team/agent (the spike findings become input for the next scaffold)
- If "no-go": document why so the question doesn't get re-asked
- Delete any temporary credentials, test data, or infrastructure

**Output**: Archived spike with clear labeling. Clean workspace.

---

## Time Box Guidance

| Complexity | Time box | When to use |
|-----------|----------|-------------|
| **Quick check** | 2–4 hours | "Does this library even work for our use case?" |
| **Focused exploration** | 1 day | "Can we replace X with Y? What are the trade-offs?" |
| **Deep investigation** | 2–3 days | "How would we architect a major new capability?" |
| **Comprehensive evaluation** | 1 week | Multiple alternatives, complex integration, architecture decision |

If your spike seems like it needs more than a week, it's not a spike — it's a project. Break it into smaller, focused spikes.

---

## Spike anti-patterns

| Anti-pattern | Why it's bad | Instead |
|-------------|-------------|---------|
| No time box | Exploration never ends | Set the time box before starting |
| Vague question | Can't tell when you're done | Make the question specific and answerable |
| Over-engineering the prototype | Wastes the time box on code quality | Write throwaway code, optimize for speed |
| No exploration log | Findings lost, effort wasted | Log as you go, even rough notes |
| Spike code goes to production | Unmaintainable, untested code in prod | Always rewrite from scratch |
| Single approach only | Confirmation bias | Consider at least one alternative |
| Skipping the decision | Exploration without conclusion | Always end with go/no-go/pivot |
