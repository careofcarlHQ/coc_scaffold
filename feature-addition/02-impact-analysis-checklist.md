# 02 — Impact Analysis Checklist

## Purpose

Before writing any feature code, map the blast radius. This checklist systematically identifies everything the feature touches in the existing system.

## When to use

Run this checklist for every feature that:
- Modifies database schema
- Adds or changes API endpoints
- Touches more than one module
- Affects existing user-facing behavior

Skip only for trivial additions (e.g., adding a static config value).

## The checklist

### Database Layer

- [ ] **New tables**: List any new tables being created
  - Table name, columns, types, constraints
  - Relationships to existing tables (foreign keys)
- [ ] **Modified tables**: List existing tables being altered
  - New columns (nullable? default value? backfill needed?)
  - Changed constraints
  - New indexes
- [ ] **Queried tables**: List tables queried but not modified
  - Will new query patterns affect performance?
  - Are existing indexes sufficient?
- [ ] **Migration safety**:
  - Can migration run without downtime?
  - Is migration reversible?
  - Does migration handle existing data correctly?

### Service Layer

- [ ] **New services/functions**: List new business logic being added
- [ ] **Modified services/functions**: List existing logic being changed
  - What callers depend on the current behavior?
  - Do changes affect return types, exceptions, or side effects?
- [ ] **Shared utilities**: Does the feature use existing shared code?
  - Any risk of modifying shared code to support the feature?
- [ ] **External dependencies**: Does the feature call external APIs?
  - Error handling for external failures
  - Rate limiting considerations
  - Cost implications

### API Layer

- [ ] **New endpoints**: List new routes being added
  - Method, path, request body, response body, error responses
  - Authentication/authorization requirements
- [ ] **Modified endpoints**: List existing endpoints being changed
  - Are changes backward-compatible?
  - Do existing clients break?
  - Are response shape changes additive (new fields only)?
- [ ] **Unchanged endpoints**: Any endpoints that query affected tables/services?
  - Could data shape changes affect their responses?

### UI Layer

- [ ] **New pages/components**: List new UI elements
- [ ] **Modified pages/components**: List existing UI being changed
- [ ] **Navigation changes**: Does the feature add menu items, routes, or links?
- [ ] **State management**: Does the feature affect shared state?

### Background Jobs

- [ ] **New jobs**: List new background processing
- [ ] **Modified jobs**: List changes to existing job logic
- [ ] **Queue changes**: Any changes to job dispatch or scheduling?

### Tests

- [ ] **Existing test coverage**: List tests that exercise affected code
  - Will they still pass after changes?
  - Do they need updating?
- [ ] **New tests needed**: List test gaps for the new feature
- [ ] **Integration tests**: Any cross-module paths that need testing?

### Documentation

- [ ] **AGENTS.md**: Does it need updating?
- [ ] **API docs**: New endpoints need documentation
- [ ] **Architecture docs**: Does the feature change module responsibilities?
- [ ] **Operational docs**: New configuration, new failure modes?

### Configuration

- [ ] **New environment variables**: List any new config
- [ ] **Changed defaults**: Any existing config behavior changing?
- [ ] **Feature flags**: Is a feature flag appropriate?

---

## Blast radius summary

After completing the checklist, summarize:

```markdown
## Impact Summary

- **Database**: N new tables, M modified tables
- **Services**: N new functions, M modified functions
- **Endpoints**: N new endpoints, M modified endpoints
- **UI**: N new pages/components, M modified
- **Jobs**: N new jobs, M modified
- **Tests**: N existing tests affected, M new tests needed
- **Config**: N new env vars

### Risk assessment
- Blast radius: small / medium / large
- Backward compatibility: preserved / breaking (with migration plan)
- Estimated implementation time: X hours/days
- Rollback complexity: simple / moderate / complex
```

## Red flags

If any of these are true, pause and reconsider the approach:

- [ ] Feature modifies more than 5 existing modules
- [ ] Feature requires breaking API changes with no migration path
- [ ] Feature modifies shared utility code used by 5+ callers
- [ ] Migration requires backfilling large amounts of existing data
- [ ] Feature affects authentication or authorization logic
- [ ] Existing test coverage on affected code is < 50%

Any red flag means: step back, consider decomposing the feature, adding tests first, or using the [refactoring scaffold](../refactoring/) to restructure before adding the feature.

## Agent prompt for impact analysis

```
Analyze the impact of adding [feature description] to this codebase.

For each layer (database, service, API, UI, jobs), identify:
1. What new code needs to be written
2. What existing code needs to be modified
3. What existing code is queried/used but unchanged
4. What tests cover the affected areas
5. What risks exist for backward compatibility

Output a structured impact analysis following the template in feature/impact-analysis.md.
```
