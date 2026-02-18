# 07 — Agent Prompts for Feature Addition

## Purpose

Concrete, copy-paste prompts for each stage of the feature addition workflow. Use these to brief agents for specific tasks.

---

## Impact Analysis Prompt

```
I need to add a feature to this codebase. Before implementing anything, analyze the impact.

Feature description: [paste feature description]

Analyze the following layers and report what will be affected:

1. **Database**: New tables? Modified tables? Affected queries?
2. **Service layer**: New functions? Modified functions? Affected callers?
3. **API layer**: New endpoints? Modified endpoints? Unchanged endpoints at risk?
4. **UI layer**: New pages? Modified components? Navigation changes?
5. **Background jobs**: New jobs? Modified jobs?
6. **Tests**: Which existing tests cover affected code? What new tests are needed?
7. **Configuration**: New env vars? Changed defaults?

For each affected area, assess:
- Risk level (low/medium/high)
- Backward compatibility impact
- Estimated effort

Output a structured impact analysis document.
```

---

## Feature Spec Review Prompt

```
Review this feature spec for completeness and implementability.

[paste or reference feature spec]

Check for:
1. Is every endpoint fully specified (method, path, request, response, errors)?
2. Is every database change specified (table, column, type, nullable, default)?
3. Are edge cases listed?
4. Are error conditions specific (exact status codes and conditions)?
5. Are acceptance criteria objective and testable?
6. Is the "not in scope" list clear?
7. Could an agent implement this without asking questions?

Report any gaps or ambiguities found.
```

---

## Database Stage Prompt

```
Implement the database changes for this feature.

Feature spec: [reference feature-spec.md]
Current migration head: [reference or let agent discover]

Tasks:
1. Create a new Alembic migration with the schema changes defined in the spec
2. Follow existing migration naming conventions in this project
3. Ensure the migration runs forward (upgrade) without errors
4. Ensure the migration runs backward (downgrade) without errors
5. Do NOT modify any existing migration files
6. Do NOT change any existing table structures unless the spec explicitly requires it

Verify by running:
- alembic upgrade head
- alembic downgrade -1
- alembic upgrade head (confirm idempotent)

Report: migration file created, verification results, any concerns.
```

---

## Service Layer Prompt

```
Implement the service layer (business logic) for this feature.

Feature spec: [reference feature-spec.md]
Impact analysis: [reference impact-analysis.md]

Tasks:
1. Implement the business logic functions defined in the spec
2. Follow existing patterns in the service layer (look at similar service modules)
3. Write unit tests for every new function
4. Cover happy path, error paths, and edge cases from the spec
5. Do NOT modify existing service functions unless the spec explicitly requires it
6. Do NOT refactor existing code while implementing

After implementation, run:
- New unit tests (all must pass)
- Full existing test suite (zero new failures)

Report: functions implemented, tests written, test results, any deviations from spec.
```

---

## API Layer Prompt

```
Implement the API endpoints for this feature.

Feature spec: [reference feature-spec.md]
Service layer: [reference the service functions just implemented]

Tasks:
1. Add new routes as defined in the spec
2. Wire endpoints to the service layer
3. Add request validation (input types, required fields)
4. Add response serialization (match spec exactly)
5. Handle all error cases with exact status codes from the spec
6. Write endpoint tests for every response code
7. Follow existing route patterns (router structure, dependency injection)
8. Do NOT modify existing endpoints unless the spec requires it

After implementation, run:
- New endpoint tests (all must pass)
- Full existing test suite (zero new failures)

Report: endpoints implemented, tests written, test results, any deviations from spec.
```

---

## UI Layer Prompt

```
Implement the UI changes for this feature.

Feature spec: [reference feature-spec.md]
API endpoints: [reference the endpoints just implemented]

Tasks:
1. Add new pages or components as defined in the spec
2. Wire to the API endpoints
3. Handle loading state, error state, and empty state
4. Follow existing component patterns and styling
5. Add navigation links if the spec requires it
6. Do NOT modify existing pages unless the spec requires it

Verify:
- Page renders without console errors
- Data loads from API correctly
- User can complete the intended flow
- Error states display correctly

Report: components created, verification results, any deviations from spec.
```

---

## Integration Verification Prompt

```
Verify the complete feature implementation.

Feature spec: [reference feature-spec.md]

Run these checks:
1. Full existing test suite — report total passed, failed, skipped
2. All new tests — report total passed, failed
3. Complete feature flow end-to-end:
   - [describe the user flow from spec]
4. Backward compatibility:
   - [list existing endpoints that should be unchanged]
   - [list existing UI flows that should work]
5. Migration safety:
   - Migration up succeeds
   - Migration down succeeds

For each acceptance criterion in the spec, report: met / not met / partially met.

Output a verification evidence document.
```

---

## Rollout Review Prompt

```
Review this feature for production readiness.

Feature spec: [reference feature-spec.md]
Implementation: [reference the changes made]

Check:
1. Are all migrations reversible?
2. Are there any breaking API changes? If so, is there a migration path?
3. Are there new environment variables? Do they have defaults?
4. Is there a feature flag? Should there be one?
5. What monitoring should be in place for the new behavior?
6. What is the rollback plan if something goes wrong?
7. Are there any data-destructive operations?

Output a rollout readiness assessment.
```
