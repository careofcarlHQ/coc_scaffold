# 06 — Writing AGENTS.md for Feature Work

## Purpose

When an agent is assigned to implement a feature in an existing codebase, it needs a focused entry point. The feature-specific AGENTS.md section (or a temporary feature brief) tells the agent: what are you building, where does it fit, and what are the rules.

## Two approaches

### 1. Feature brief (recommended for most features)

Create a temporary `feature/AGENTS-BRIEF.md` that the agent reads alongside the main `AGENTS.md`. Delete it after the feature merges.

```markdown
# Feature Brief — [Feature Name]

## What you're building
One paragraph describing the feature.

## Read these files (in order)
1. `AGENTS.md` (project-level rules)
2. `feature/feature-spec.md` (what to build)
3. `feature/impact-analysis.md` (what it touches)
4. `feature/feature-checklist.md` (build stages)

## Key constraints
- Do NOT modify existing test files unless the spec requires it
- Do NOT refactor while implementing — one purpose per change
- Follow existing code patterns in the modules you're touching
- Run the full test suite after each stage

## Current stage
Stage N — [stage name]

## Acceptance criteria
[Copy from feature spec]
```

### 2. AGENTS.md section (for long-running features)

For features that span multiple sessions, add a temporary section to the main `AGENTS.md`:

```markdown
## Current Feature Work

**Feature**: [name]
**Spec**: `feature/feature-spec.md`
**Impact**: `feature/impact-analysis.md`
**Checklist**: `feature/feature-checklist.md`
**Current stage**: Stage N — [name]

Remove this section when the feature is merged.
```

## What to include in the feature brief

| Section | Purpose | Example |
|---------|---------|---------|
| What you're building | Orient the agent | "Add download endpoint for exports" |
| Reading order | Progressive disclosure | Numbered file list |
| Key constraints | Rails for the agent | "Don't refactor while adding features" |
| Current stage | Focus the agent | "Stage 2 — Service Layer" |
| Acceptance criteria | Define done | Copied from feature spec |

## What NOT to include

- Full implementation details (those live in the feature spec)
- Codebase architecture overview (that's in the main AGENTS.md)
- History of why this feature was chosen (that's in the motivation section)

## Lifecycle

```
Feature starts  → Create feature/AGENTS-BRIEF.md
Each session    → Update "Current stage" to where work should resume
Feature merges  → Delete feature/AGENTS-BRIEF.md
                → Remove any temporary AGENTS.md sections
                → Update main AGENTS.md if feature changed project structure
```

## Validation checklist

- [ ] Brief is under 50 lines
- [ ] Reading order has the feature spec
- [ ] Constraints include "don't refactor" and "run full tests"
- [ ] Current stage is accurate
- [ ] All referenced files exist
