# 04 — Phased Implementation Guide

## The build order

Feature implementation always follows bottom-up dependency order. Each stage has an acceptance gate that must pass before advancing.

```
Stage 1   Database Layer (schema + migration)
Stage 2   Service Layer (business logic)
Stage 3   API Layer (endpoints + validation)
Stage 4   UI Layer (pages + components)  — if applicable
Stage 5   Background Jobs                — if applicable
Stage 6   Integration Verification
```

Not every feature needs all stages. A backend-only feature skips Stage 4. A feature with no new data skips Stage 1. But the **order** never changes.

## Stage design rules

### 1. Each stage should be completable in 1–4 hours

If a stage takes longer, break it into sub-stages (e.g., 2a: schema, 2b: migration, 2c: seed data).

### 2. Each stage has an acceptance gate

Gates are **objective, reproducible** conditions:

```markdown
# ✅ Good acceptance gates
- Migration runs up and down cleanly on fresh DB
- Service function returns correct result for 3 test cases
- Endpoint returns 200 with expected payload
- UI page renders and shows data from API
- Existing test suite passes with zero failures

# ❌ Bad acceptance gates
- "Code looks good"
- "Feature works"
- "Tests pass" (which tests? all? new ones only?)
```

### 3. Never skip stages

Even if you "know" the database layer is trivial, verify it before building the service layer on top. Skipping verification cascades errors upward.

### 4. Run existing tests at every stage

After every stage, run the full existing test suite. This catches regression immediately, when the cause is obvious (the change you just made).

## Stage details

### Stage 1 — Database Layer

**Activities**:
- Create migration file(s)
- Add new tables, columns, constraints, indexes
- Verify migration runs forward (up)
- Verify migration runs backward (down)
- Verify existing data is preserved (if applicable)

**Gate**: 
- `alembic upgrade head` succeeds from current state
- `alembic downgrade -1` succeeds
- Fresh database bootstrap works
- Existing query patterns still work

**Agent guidance**:
```
Implement the database changes defined in the feature spec.
Create an Alembic migration. Verify it runs up and down.
Do NOT modify any existing migration files.
Follow existing migration naming conventions.
```

### Stage 2 — Service Layer

**Activities**:
- Implement new business logic functions
- Write unit tests for each function
- Handle error cases defined in the spec
- Follow existing service patterns in the codebase

**Gate**:
- All new unit tests pass
- All existing unit tests pass
- Edge cases from spec are covered
- Error paths return expected exceptions/results

**Agent guidance**:
```
Implement the business logic defined in the feature spec.
Follow the patterns used in existing service modules.
Write unit tests for every function. Cover error paths.
Do NOT modify existing service functions unless the spec requires it.
```

### Stage 3 — API Layer

**Activities**:
- Add new routes or modify existing routes
- Wire endpoints to service layer
- Add request validation
- Add response serialization
- Write endpoint tests

**Gate**:
- New endpoint tests pass (happy path + error paths)
- All existing endpoint tests pass
- Request validation rejects invalid input
- Error responses match spec exactly

**Agent guidance**:
```
Implement the API endpoints defined in the feature spec.
Follow existing route patterns (router registration, dependency injection, etc.).
Write endpoint tests covering all response codes in the spec.
Verify existing endpoints are unchanged by running the full test suite.
```

### Stage 4 — UI Layer (if applicable)

**Activities**:
- Add new pages or components
- Wire to API endpoints
- Handle loading, error, and empty states
- Follow existing UI patterns

**Gate**:
- Page renders without errors
- Data loads from API correctly
- User can complete the intended flow
- Error states display correctly

**Agent guidance**:
```
Implement the UI changes defined in the feature spec.
Follow existing component patterns and styling conventions.
Handle loading, error, and empty states.
Test the full user flow manually or with component tests.
```

### Stage 5 — Background Jobs (if applicable)

**Activities**:
- Add or modify job handlers
- Wire job dispatch
- Handle failure and retry scenarios
- Write job-specific tests

**Gate**:
- Job executes successfully with test data
- Failure triggers retry behavior
- Dead-letter / error handling works
- Existing jobs unaffected

### Stage 6 — Integration Verification

**Activities**:
- Run the complete feature flow end-to-end
- Run the full existing test suite
- Verify no regressions anywhere
- Document any deviations from spec

**Gate**:
- Complete feature path works end-to-end
- All existing tests pass (zero regressions)
- All new tests pass
- Feature matches acceptance criteria in spec

---

## Tracking progress

Use the feature checklist template to track each stage:

```markdown
### Stage N — [Layer Name]

- Status: not-started / in-progress / done / blocked
- Work completed:
  - 
- Tests added:
  - 
- Deviations from spec:
  - 
- Acceptance gate: pass / fail
- Evidence:
  - 
```

## Common pitfalls

| Pitfall | Consequence | Prevention |
|---------|-------------|------------|
| Starting at the UI | Build on unstable foundation | Always start at database |
| Modifying existing code "while I'm here" | Mixed-purpose changes | One feature, one branch |
| Skipping the migration rollback test | Can't undo deployment | Always test down migration |
| No tests until the end | Can't isolate test failures | Tests at each stage |
| Ignoring existing test failures | Regressions slip through | Zero-regression policy at every stage |
