# 01 — Process Overview: End-to-End Feature Addition Workflow

## The feature addition lifecycle

Adding a feature to a working system follows a predictable lifecycle. Each phase builds on the previous one, and every transition has an explicit gate.

```
┌─────────────────────────────────────────────────────────┐
│                FEATURE ADDITION LIFECYCLE                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. SCOPING            Define what you're adding        │
│       │                                                 │
│       ▼                                                 │
│  2. IMPACT ANALYSIS    Map what it touches              │
│       │                                                 │
│       ▼                                                 │
│  3. FEATURE SPEC       Write the contract               │
│       │                                                 │
│       ▼                                                 │
│  4. IMPLEMENTATION     Build bottom-up with gates       │
│       │                                                 │
│       ▼                                                 │
│  5. VERIFICATION       Prove it works, nothing broke    │
│       │                                                 │
│       ▼                                                 │
│  6. ROLLOUT            Deploy safely to production      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Phase breakdown

### 1. Scoping (30 minutes)

**Input**: A feature request, user need, or technical requirement
**Output**: One-paragraph feature definition with clear boundaries

Activities:
- Write a single paragraph describing what the feature does
- List what's in scope (the feature) and what's NOT in scope (future work)
- Identify the user/consumer of this feature
- Estimate complexity: small (hours), medium (1–2 days), large (3+ days)

Gate: Feature description fits in one paragraph. Scope boundaries are explicit.

### 2. Impact Analysis (30–60 minutes)

**Input**: Feature definition
**Output**: Impact analysis document

Activities:
- List all database tables affected (new, modified, unchanged-but-queried)
- List all modules/services touched
- List all API endpoints affected (new, modified, unchanged)
- List all UI pages affected
- List all background jobs affected
- List all existing tests that exercise affected code
- Identify external system interactions (APIs, webhooks, etc.)

Gate: No "unknown" entries in the impact analysis. Every affected area is identified.

Key document:
- `feature/impact-analysis.md`

### 3. Feature Spec (1–2 hours)

**Input**: Impact analysis + feature definition
**Output**: Feature specification document

Activities:
- Define new database schema changes (tables, columns, constraints, migrations)
- Define new or modified API endpoints (method, path, request, response, errors)
- Define new business logic rules
- Define compatibility requirements (what must not change)
- Define test requirements per layer
- Define acceptance criteria (how do you know it works?)

The spec should be detailed enough that an agent can implement from it without asking questions.

Gate: Spec covers all layers identified in impact analysis. Acceptance criteria are objective.

Key document:
- `feature/feature-spec.md`

### 4. Implementation (hours to days)

**Input**: Feature spec + impact analysis
**Output**: Working code with tests at each layer

Build in strict order:

```
Stage 1 — Database Layer
           Create migration. Add new tables/columns/constraints.
           Gate: Migration runs up and down cleanly. Existing data preserved.

Stage 2 — Service Layer
           Implement business logic functions.
           Gate: Unit tests pass for all new logic. Edge cases covered.

Stage 3 — API Layer
           Add or modify endpoints. Wire to service layer.
           Gate: Endpoint tests pass. Error responses correct. Existing endpoints unchanged.

Stage 4 — UI Layer (if applicable)
           Add pages, components, or modify existing views.
           Gate: UI renders correctly. User flow works end-to-end.

Stage 5 — Background Jobs (if applicable)
           Add or modify job processing.
           Gate: Job executes correctly. Failure/retry behavior works.

Stage 6 — Integration Verification
           Run full test suite. Test the complete feature path.
           Gate: All existing tests pass. New feature works end-to-end.
```

### 5. Verification (30–60 minutes)

**Input**: Completed implementation
**Output**: Verification evidence

Activities:
- Run full existing test suite — zero regressions
- Run new feature tests — all pass
- Verify backward compatibility (existing API consumers, data shapes)
- Test error paths and edge cases
- Check for missing documentation updates
- Review migration safety (reversible? data-preserving?)

Gate: Zero regressions. Feature works as specified. Compatibility confirmed.

Key document:
- `feature/compatibility-check.md`

### 6. Rollout (30 minutes to hours)

**Input**: Verified feature
**Output**: Feature live in production

Activities:
- Review migration running order and safety
- Confirm rollback plan exists
- Deploy to staging/preview environment (if available)
- Run smoke tests against deployed version
- Deploy to production
- Verify feature works in production
- Monitor for errors in first 24 hours

Gate: Feature operational in production. No error spikes. Rollback plan tested or documented.

Key document:
- `feature/rollout-plan.md`

---

## Task-level workflow for agents

Within implementation, agents follow this pattern for each stage:

```
Read Spec → Implement → Test → Self-Verify → Report
```

### Read Spec
- Read the feature spec for the current layer
- Read the impact analysis for affected modules
- Read existing code in affected areas

### Implement
- Write code that satisfies the spec
- Follow existing patterns in the codebase
- Make minimal changes — don't refactor while adding features

### Test
- Write tests for new behavior
- Run existing tests to confirm no regressions

### Self-Verify
- Check: does the implementation match the spec?
- Check: are all acceptance criteria met for this stage?
- Check: are there any TODO/FIXME items left?

### Report
- Summarize what was implemented
- List any deviations from spec (and why)
- List any follow-up items discovered
- Provide gate evidence

---

## Sizing guide

| Size | Time | Stages | Example |
|------|------|--------|---------|
| Small | 2–4 hours | 2–3 stages | Add a new API endpoint with one DB query |
| Medium | 1–2 days | 4–5 stages | New resource type with CRUD + UI page |
| Large | 3–5 days | 6 stages | New subsystem with jobs, API, and UI |
| Too Large | 5+ days | — | Break into multiple features |

If a feature is "too large," decompose it into independent deliverable features that each provide value.
