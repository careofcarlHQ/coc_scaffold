# 00 — Philosophy: Agent-First Development

## The core insight

When AI agents are your primary code producers, the bottleneck shifts from writing code to **designing environments where agents can do reliable work**.

Human engineering effort moves upstream: defining intent, writing constraints, building feedback loops, and creating the scaffolding that makes agent output predictable and high-quality.

## Principles

### 1. Spec-first, code-second

Write the contracts before touching code. Every implementation decision should trace back to a spec document. This gives agents (and humans) a clear target and prevents scope drift.

In practice this means:
- Architecture decisions are documented before the first line of code
- API contracts define endpoints, payloads, and error semantics before routes exist
- Data models define schemas and state machines before migrations run
- Implementation checklists define stage order before coding begins

### 2. Repository as system of record

Everything the agent needs to work effectively must live in the repository. Knowledge that exists only in Slack threads, Google Docs, or people's heads is invisible to agents.

This includes:
- **AGENTS.md** — the "table of contents" for agent orientation
- **spec/** — contracts, policies, and checklists
- **Architecture docs** — stack decisions, service boundaries, data models
- **Operational docs** — bootstrap guides, runbooks, SOPs

### 3. AGENTS.md as map, not manual

Keep AGENTS.md short (under 150 lines). It should be a table of contents pointing to deeper sources of truth, not a monolithic instruction set.

A giant AGENTS.md fails because:
- It crowds out task context
- When everything is "important," nothing is
- It rots faster than focused, scoped documents
- It's hard to verify mechanically

### 4. Progressive disclosure over front-loading

Agents work best when they can navigate from a small stable entry point to deeper context on demand. Structure your docs so agents start with orientation and drill into detail as needed.

### 5. Phased delivery with acceptance gates

Break work into phases, phases into stages, stages into concrete checkboxes. Every stage has an acceptance gate — an objective condition that must be met before advancing.

This prevents:
- Half-implemented features
- Skipped validation
- "It works on my machine" advancement
- Scope creep within stages

### 6. Human steers, agent executes

Humans provide:
- Problem statements and constraints
- Risk assessments and escalation triggers
- Final approval before merge
- Taste and architectural direction

Agents provide:
- Implementation (code, tests, docs)
- Review (policy compliance, correctness)
- Validation (build, lint, test evidence)
- Evidence packaging

### 7. Fail closed, not open

When validation is missing or ambiguous, block progression. When risk exceeds agent certainty, escalate. Default to safety — it's cheaper to resolve a blocked task than to revert a broken merge.

### 8. Evidence over trust

Every stage produces artifacts. Reviewer decisions, validator outputs, command evidence, risk assessments — all captured and traceable. This makes human approval fast because the reviewer sees structured evidence, not raw diffs.

### 9. Minimize infrastructure, maximize leverage

Start with boring, well-understood technology. Postgres over Redis. FastAPI over custom frameworks. Standard tools over novel ones. Agents work best with composable, stable, well-documented technology.

### 10. Continuous refinement beats big rewrites

Encode lessons into:
- Updated specs and checklists
- Tighter acceptance gates
- New escalation triggers
- Better agent prompts

Small weekly improvements compound into a reliable system.

---

## Lessons from building coc_agent_process

### What worked well

1. **Gap analysis before coding** — we audited all existing docs to identify what was missing before writing a single line of code. This produced a clear P0/P1 priority list.

2. **11-stage checklists** — stages 0–10 with objective acceptance gates kept progress measurable and prevented premature advancement.

3. **Spec documents as agent context** — agents could read `api-contract.md` and produce correct route implementations because the contract was precise and machine-readable.

4. **Evidence templates** — standardized PR evidence made human review fast and consistent across all tasks.

5. **Cost and guardrail policies from day one** — having budget limits and escalation triggers active immediately prevented runaway spending and unsafe autonomy.

### What we'd do differently

1. **Start the UI earlier** — Phase 1 was API-only; adding the operator UI in Phase 2 revealed API gaps that would have been caught sooner with a thin UI from stage 5.

2. **Write contract tests for state machine transitions first** — these became the most valuable tests and should have been the first thing implemented.

3. **Keep the gap analysis as a living document** — it was a one-time artifact but should have been maintained as gaps were closed.

### The OpenAI Codex team's parallel learnings

Our approach independently mirrors several patterns described by the OpenAI Codex team in their [agent-first engineering post](spec/open-ai%20process%20description.md):

- Repository knowledge as system of record
- AGENTS.md as map, not manual
- Progressive context disclosure
- Enforcing architecture mechanically
- Continuous "garbage collection" of technical debt
- Increasing agent autonomy as tooling matures
