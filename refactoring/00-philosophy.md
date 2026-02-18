# 00 — Philosophy: Refactoring with Agents

## The core insight

Refactoring is the riskiest kind of code change: you're restructuring working software. The system works today — your job is to make it work **better** without breaking what works. When agents do the mechanical work, humans can focus on the hard parts: deciding **what** to change, **why**, and **when to stop**.

## Principles

### 1. Working code is sacred

The system works today. Every refactoring step must preserve that. If you can't prove behavior is preserved, don't merge the change.

In practice this means:
- Write characterization tests before touching structure
- Run the full test suite after every atomic change
- Never refactor and add features in the same change
- If tests don't exist, write them first — that's your first refactoring phase

### 2. Measure before you cut

Don't refactor because code "looks messy." Refactor because you have evidence of a specific problem:

- **Coupling**: changing module A breaks module B
- **Complexity**: cyclomatic complexity > threshold, functions > 50 lines
- **Duplication**: same logic in 3+ places
- **Naming**: module names don't match responsibilities
- **Performance**: measurable bottleneck traced to structural issues
- **Extensibility**: adding a feature requires touching 10+ files

Refactoring without evidence of pain is refactoring for its own sake — the most common way refactoring projects stall.

### 3. Incremental transformation, never big bang

The #1 cause of failed refactoring is attempting too much at once. A "big rewrite" is not refactoring — it's a new project wearing the old project's clothes.

Rules:
- Each change must be independently mergeable
- Each change must leave the system in a working state
- Each change should take 1–4 hours of agent work
- If a refactoring step requires more than one PR, it's too big

### 4. Behavior preservation before structural change

The sequence is always:
1. **Characterize** — capture what the code actually does (not what it should do)
2. **Protect** — add tests that lock in current behavior
3. **Transform** — restructure the code
4. **Verify** — prove the tests still pass
5. **Clean up** — remove scaffolding, update docs

Never skip steps 1–2. They're what make everything else safe.

### 5. Name the pattern you're applying

Every refactoring step should be nameable. If you can't name it, you're making ad-hoc changes — not refactoring.

Common refactoring patterns:
- Extract function / method / class
- Inline function / variable
- Move module / function to better location
- Rename for clarity
- Replace conditional with polymorphism
- Introduce parameter object
- Split module by responsibility
- Consolidate duplicate logic
- Introduce interface / protocol
- Replace inheritance with composition
- Strangler fig (gradual replacement)

### 6. Repository as system of record

The refactoring plan, assessment, migration maps, and progress logs all live in the repo. An agent picking up the project mid-stream should be able to read the plan and continue without oral history.

### 7. Human steers, agent executes

Humans decide:
- What to refactor (scope)
- Why to refactor (motivation)
- When to stop (good enough vs. perfect)
- Risk tolerance (how aggressive to be)

Agents execute:
- Code analysis and metric extraction
- Characterization test generation
- Mechanical code transformations
- Verification (build, lint, test)
- Progress logging

### 8. Strangler fig over clean slate

When replacing a subsystem, don't delete the old code first. Instead:
1. Build the new structure alongside the old
2. Route new callers to the new structure
3. Migrate existing callers one by one
4. Delete the old code only when zero callers remain

This keeps the system working at every step and provides a natural rollback: just revert to the old path.

### 9. Refactoring has diminishing returns

The first 20% of refactoring captures 80% of the value. Know when to stop:

- **Stop when** the code is clear enough to extend confidently
- **Stop when** new features can be added by touching 1–3 files instead of 10
- **Stop when** test coverage on the refactored area is > 80%
- **Don't chase** perfect architecture — chase "good enough to move fast"

### 10. Every refactoring creates documentation debt

Changing code structure invalidates existing docs. Budget time to update:
- AGENTS.md pointers
- Architecture diagrams
- API surface docs
- Module maps
- Developer onboarding guides

If your repo uses the [repo-documentation scaffold](../repo-documentation/), run a freshness check after each phase.

---

## Lessons from refactoring coc_capi

### What we found

1. **Organic growth created coupling** — services imported from each other freely, making it hard to change one without affecting others.

2. **Business logic was scattered** — rules lived in route handlers, service functions, and database queries. No single source of truth for domain rules.

3. **Test coverage was uneven** — happy paths well-tested, error paths and edge cases undertested. Refactoring without better coverage was risky.

4. **Naming didn't match current responsibilities** — modules named for their original purpose had grown to do much more (or something different).

5. **Configuration was implicit** — behavior depended on environment variables accessed deep in call chains, making it hard to understand what a module needed.

### What worked

1. **Assessment before action** — running complexity metrics and dependency analysis before planning prevented wasted effort on low-impact areas.

2. **Characterization tests first** — writing tests that captured actual behavior (including bugs) before restructuring gave confidence to make changes.

3. **One pattern per PR** — each PR applied exactly one named refactoring pattern, making review fast and rollback simple.

4. **Migration maps** — documenting "module A line 45 → module B line 12" made agent execution precise and verifiable.

5. **Agent-driven mechanical changes** — agents excelled at extract-function, move-module, and rename operations. Humans focused on the harder judgment calls.

### What we'd do differently

1. **Start with dependency graph visualization** — understanding the actual import graph would have revealed the highest-impact seams faster.

2. **Define "done" more precisely upfront** — we over-refactored some areas because we didn't define concrete stopping criteria.

3. **Track migration maps in a structured format** — prose descriptions of "old → new" were harder for agents to parse than tables.
