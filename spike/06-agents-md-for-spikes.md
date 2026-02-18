# 06 — AGENTS.md for Spikes

> How to orient an agent for exploration work. Spike work is unique: the agent needs *permission* to be messy, but *constraints* to stay focused.

---

## Why AGENTS.md matters for spikes

Agents are trained to write production-quality code. During a spike, that instinct works against you. An agent without spike-specific guidance will:
- Write tests for prototype code (wasting time)
- Handle edge cases (not the point right now)
- Refactor the prototype (it's disposable!)
- Install packages in the main project (contamination)
- Forget to document what it's learning (losing the actual deliverable)

The spike AGENTS.md gives the agent permission to be scrappy while keeping it focused on the question.

---

## Spike brief structure

### 1. What we're exploring

```markdown
## Spike
{Name of the spike}

## Question
{The specific question from the charter}

## Time box
{How much time remains — this helps the agent prioritize}

## Success criteria
- {Criterion 1}
- {Criterion 2}
```

### 2. Exploration permissions

```markdown
## Spike rules (different from normal!)
- You MAY hardcode values
- You MAY skip error handling
- You MAY skip tests
- You MAY copy-paste from examples
- You MAY write ugly code — speed over quality

But:
- You MUST work in temp/spike-{name}/ (not in the main codebase)
- You MUST keep an exploration log (findings are the deliverable)
- You MUST stay on the charter question (no scope creep)
- You MUST NOT install packages in the main project
- You MUST NOT modify existing source code
```

### 3. What to document

```markdown
## For every experiment
Document in the exploration log:
1. What you're trying and why
2. What happened (include errors, output, measurements)
3. What you learned from it
4. What to try next

## At the end
1. Can we answer the spike question? Yes/No/Partially
2. What are the trade-offs?
3. What's the effort estimate for real implementation?
4. What remains unknown?
```

### 4. Scope boundaries

```markdown
## In scope
- {What to explore}
- {What to prototype}

## Out of scope
- {What NOT to touch}
- {What to explicitly ignore}
- Production code
- Main project dependencies
```

---

## Session management

Spikes can benefit from multiple agent sessions:

### Session 1: Research
```markdown
## Your job
Research {topic}. Read the docs. Find examples. Assess feasibility.
Do NOT write any code yet.
Document findings in temp/spike-{name}/exploration-log.md.
```

### Session 2: Prototype
```markdown
## Your job
Read the exploration log from session 1.
Build a proof of concept in temp/spike-{name}/.
Focus on answering: {specific question from charter}.
Document what works and what doesn't in the exploration log.
```

### Session 3: Findings
```markdown
## Your job
Read the exploration log and the prototype.
Write temp/spike-{name}/findings.md using the template.
Write temp/spike-{name}/decision.md with your recommendation.
```

---

## Template

See `templates/AGENTS.md.template` for a ready-to-fill spike orientation document.
