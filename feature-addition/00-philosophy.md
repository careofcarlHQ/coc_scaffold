# 00 — Philosophy: Adding Features to Working Systems

## The core insight

Most development work isn't greenfield and isn't refactoring — it's **adding new capabilities to existing systems**. This is uniquely challenging because you're solving two problems simultaneously: building something new while preserving everything that already works.

When agents do the implementation, the human's job is to define **what** the feature does, **where** it fits in the existing system, and **what must not break**.

## Principles

### 1. Impact analysis before implementation

Before writing any code, understand the blast radius. Every feature touches existing code, and the places it touches are where bugs hide.

In practice this means:
- Map which modules, tables, endpoints, and tests the feature affects
- Identify existing consumers that might be impacted
- Quantify the scope: is this a 2-file change or a 20-file change?
- If the blast radius surprises you, reconsider the approach

### 2. Feature specs, not PRDs

A greenfield project needs a PRD. A feature addition needs a **feature spec** — a focused contract covering only the delta:
- What's being added (not what already exists)
- How it interacts with existing behavior
- What constraints it inherits from the current system
- What new constraints it introduces

### 3. Compatibility is the default constraint

Existing API consumers, data shapes, UI flows, and CLI behaviors must continue to work unless you explicitly decide to break them. Breaking changes require:
- A documented rationale
- A migration path for existing consumers
- Version negotiation or deprecation timeline

### 4. Build in dependency order

Always build bottom-up through the stack:

```
1. Database (schema changes, migrations)
2. Service layer (business logic)
3. API layer (endpoints, validation)
4. UI layer (pages, components)
5. Background jobs (if applicable)
```

Why this order?
- Each layer depends on the one below
- You can test each layer independently
- Failures are caught at the foundation, not the surface
- Agents can implement each layer with clear inputs and outputs

### 5. One feature, one branch, one purpose

Never combine feature work with:
- Refactoring (use the refactoring scaffold instead)
- Bug fixes (use the bug-investigation scaffold instead)
- "While I'm in here" improvements

Mixed-purpose branches are harder to review, harder to revert, and harder for agents to reason about.

### 6. Tests follow the feature, not later

Every feature implementation includes its tests. Not "we'll add tests later" — that later never comes and you lose the context.

For each feature layer:
- Database: migration test (up/down), constraint tests
- Service: unit tests for new business logic
- API: endpoint tests for new routes, edge cases, error responses
- UI: component tests or smoke tests
- Integration: end-to-end path through the new feature

### 7. Incremental verification, not final validation

Don't wait until the feature is "done" to test it. Verify at every layer:
- Migration runs? Verify.
- Service function works? Verify.
- Endpoint returns correct response? Verify.
- UI renders? Verify.

This catches problems close to their source and prevents cascading failures during integration.

### 8. Rollout is part of the feature, not an afterthought

The feature isn't done when the code works locally. It's done when:
- Migrations are safe to run in production
- Backward compatibility is confirmed
- Rollback strategy is documented
- Monitoring/logging covers the new behavior
- Feature flag (if applicable) is in place

### 9. Scope creep is the #1 feature killer

Features grow. "Just one more thing" turns a 4-hour feature into a 4-day project. Fight this by:
- Writing the spec before coding (locks scope)
- Saying "that's a separate feature" liberally
- Keeping a "follow-up" list for ideas that emerge during implementation
- Reviewing scope at each stage gate

### 10. Document the decision, not just the code

When you add a feature, record:
- Why this approach was chosen (not just what was built)
- What alternatives were considered and rejected
- What trade-offs were accepted
- What follow-up work was deferred

This context is invisible in code and invaluable for future decisions.

---

## Lessons from extending coc_capi

### What worked well

1. **Impact analysis before coding** — mapping affected modules before starting prevented mid-implementation surprises. The 5 minutes spent on analysis saved hours of rework.

2. **Database-first implementation** — always starting with migrations and schema changes meant the foundation was solid before building on top.

3. **Feature specs as agent briefs** — a one-page spec with endpoints, payloads, and error semantics was enough for agents to implement confidently.

4. **Compatibility checks against existing tests** — running the full existing test suite after each layer confirmed nothing was broken.

### What we'd do differently

1. **Write rollout plans earlier** — we sometimes discovered migration complexity late. Thinking about production deployment at spec time would have caught issues.

2. **Track follow-up items more rigorously** — good ideas that emerged during feature work sometimes got lost. A formal follow-up list would have preserved them.

3. **Feature flags from the start** — for larger features, having a kill switch from day one would have reduced deployment anxiety.
