# 07 — Agent Prompts for Migration

## Purpose

Concrete, copy-paste prompts for each phase of a migration. These are more cautious than feature or refactoring prompts because migrations touch foundations.

---

## Current State Snapshot Prompt

```
Analyze this codebase and produce a complete current-state snapshot for migration planning.

Document the following:
1. Language and runtime: exact version of Python (or other language) and runtime
2. Framework: exact version of FastAPI (or other framework) and key dependencies
3. Database: engine, version, table count, approximate data size, migration tool and current head
4. Dependencies: export full dependency list with versions
5. Infrastructure: hosting platform, service type, region (from config files if available)
6. Configuration: list all environment variables referenced in the code
7. External integrations: list all external APIs, webhooks, and SDK calls
8. Tests: run the test suite, report pass/fail/skip counts
9. Known deprecation warnings: run with warnings enabled, capture any deprecation notices

Use the current-state-snapshot template format. Mark anything you cannot determine as "UNKNOWN — requires manual check".
```

---

## Gap Map Prompt

```
I'm migrating from {current state} to {target state}.

Analyze the codebase and produce a compatibility gap map.

For each gap found:
1. What exactly needs to change
2. Which files are affected
3. Risk level (low / medium / high)
4. Estimated effort (hours)
5. Dependencies (does this gap depend on fixing another gap first?)

Categories to check:
- Breaking API changes in dependencies
- Deprecated function/module usage
- Configuration changes needed
- Database compatibility
- Test compatibility
- Import path changes
- Type annotation changes

Output a structured gap map sorted by dependency order, then by risk (lowest first).
```

---

## Stage Execution Prompt

```
Execute migration stage {N}: {stage name}.

Migration plan: [reference migration-checklist.md]
Current state: [reference current-state-snapshot.md]

BEFORE STARTING:
1. Confirm current test suite passes (run pytest, report results)
2. Take backup if this stage touches data

EXECUTE:
{Stage-specific instructions from migration plan}

AFTER EXECUTION:
1. Run the full test suite — report pass/fail/skip
2. Compare test results to baseline (any new failures?)
3. Verify the stage-specific acceptance criteria
4. Confirm rollback is possible (describe how)

OUTPUT:
- Changes made (list files/config/data changed)
- Test results comparison (before vs after)
- Verification results
- Rollback confirmation
- Any issues or deviations from plan
```

---

## Rollback Verification Prompt

```
Test the rollback for migration stage {N}: {stage name}.

The changes applied in this stage were: {list changes}

Tasks:
1. Execute the documented rollback steps
2. Verify: test suite passes after rollback
3. Verify: application functions correctly after rollback
4. Re-apply the stage changes (restore the migrated state)
5. Verify: test suite passes after re-apply

Report:
- Rollback steps executed
- Rollback verification result
- Re-apply verification result
- Time taken for rollback
- Any issues discovered
```

---

## Cutover Readiness Prompt

```
Assess cutover readiness for this migration.

Migration checklist: [reference migration-checklist.md]

Check:
1. Are ALL migration stages complete?
2. Are ALL stage verifications passing?
3. Are ALL rollback plans tested?
4. Is the test suite passing on the migrated state?
5. Are there any outstanding issues or deviations?
6. Is monitoring in place for post-cutover?
7. Is the old system available for rollback?
8. Is there a communication plan for users (if applicable)?

Output: READY / NOT READY with specific blockers if not ready.
```

---

## Post-Migration Cleanup Prompt

```
The migration is complete and stable. Perform cleanup.

Tasks:
1. Identify all compatibility shims, fallback code, or temporary workarounds added during migration
2. Identify all old configuration that is no longer needed
3. Identify all references to the old state (old versions, old paths, old URLs)
4. For each item found:
   - Can it be safely removed?
   - Are there tests that depend on it?
   - Does any documentation reference it?
5. Remove safely removable items
6. Update documentation to reflect the new state
7. Run the test suite after cleanup — zero regressions

Output: List of items cleaned up, list of items that need manual attention, test results.
```
