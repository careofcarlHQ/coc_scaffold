# 07 — Agent Automation Prompts

## Purpose

This guide provides **concrete, executable prompts** that an AI agent can use to analyze code, plan refactoring, and execute transformations. Instead of a human manually reading every file and deciding what to change, an agent runs these analysis and execution patterns systematically.

## How to use these prompts

For each refactoring phase, there's a set of prompts that:

1. **Analyze** — extract metrics and structural information from the codebase
2. **Plan** — generate migration maps and checklists
3. **Execute** — apply named refactoring patterns
4. **Verify** — confirm behavior is preserved

Give the agent the relevant prompt along with the migration map or checklist. The agent reads the code, applies the pattern, and verifies the result.

---

## Assessment Prompts

### Prompt: Complexity analysis

```
Analyze the complexity of this codebase and produce a health report.

STEP 1 — FILE-LEVEL METRICS
For every source file under {source_root}:
- Count lines of code (excluding blank lines and comments)
- Flag files over 300 lines
- Flag files over 500 lines

STEP 2 — FUNCTION-LEVEL METRICS
For every function/method:
- Count lines
- Run `radon cc {source_root}/ -a -nc` and parse the output for cyclomatic complexity
  (if radon is unavailable, count branches: if/elif/else/for/while/try/except/and/or)
- Flag functions over 50 lines
- Flag functions with complexity > 10

IMPORTANT: Use tool output, not estimation. Run the commands and parse results.
If a tool is unavailable, install it first (`pip install radon`).

STEP 3 — DUPLICATION
Search for:
- Functions with identical or near-identical signatures in different files
- Code blocks of 6+ lines that appear in multiple places
- Constants or config values repeated in 3+ locations

STEP 4 — SUMMARY
Produce a table: | File | Lines | Max Function Length | Max Complexity | Issues |

Output: A completed codebase-assessment.md using the template.
```

### Prompt: Dependency graph extraction

```
Map the internal dependency graph of this codebase.

STEP 1 — IMPORT MAPPING
For every source file under {source_root}:
- List all internal imports (imports from within the project)
- List all external imports (third-party packages)
- Record the specific symbols imported

STEP 2 — DEPENDENCY MATRIX
Create a module-level adjacency matrix:
- Rows = importing module
- Columns = imported module
- Cells = number of symbols imported

STEP 3 — ANALYSIS
Identify:
- Circular dependencies (A imports B imports A)
- Hub modules (imported by > 10 other modules)
- Fan-out modules (imports > 5 other internal modules)
- Layering violations (lower layer importing from higher layer)

STEP 4 — VISUALIZATION
Create a text-based dependency diagram showing:
- Modules as nodes
- Import relationships as arrows
- Circular dependencies highlighted

Output: Dependency graph report with matrix, analysis, and diagram.
```

### Prompt: Change hotspot analysis

```
Analyze the git history to find change hotspots.

STEP 1 — CHURN ANALYSIS
Run git log analysis for the last 6 months:
- Count how many times each file was changed
- List the top 20 most-changed files

STEP 2 — CO-CHANGE ANALYSIS
From the same history:
- Identify files that are frequently changed together in the same commit
- List the top 10 co-change pairs

STEP 3 — CHURN × COMPLEXITY
Cross-reference the churn list with complexity metrics:
- For each of the top 20 churned files, note its complexity and line count
- Rank by churn × complexity score

STEP 4 — RECOMMENDATIONS
For the top 5 hotspots:
- What refactoring pattern would reduce churn?
- What would the target structure look like?
- What tests exist? What's missing?

Output: Hotspot report with ranked targets and recommendations.
```

---

## Planning Prompts

### Prompt: Migration map generation

```
Generate a migration map for refactoring {target_module}.

CURRENT STATE:
Read {target_file} and document:
- Every class, function, and constant defined (by name, not line number)
- What each definition does (one-line summary)
- Who calls each definition (search for imports and usages)

TARGET STATE:
Based on the refactoring plan, determine:
- What new modules need to be created
- Where each definition should move
- What the named refactoring pattern is for each move

IMPORTANT: Anchor all entries to function/class names, never line numbers.
Line numbers go stale after any edit. `file::function()` is self-healing.

OUTPUT FORMAT:
| Current location | New location | Pattern | What moves | Callers to update |
|-----------------|--------------|---------|------------|-------------------|
| file::function_or_class | new_file | pattern_name | description | list of callers |

Also generate:
- Dependency order (what must move first)
- Risk assessment per move (low/medium/high based on caller count and test coverage)
```

### Prompt: Characterization test generation

```
Generate characterization tests for {target_module} before refactoring.

STEP 1 — INVENTORY
Read {target_file} and list every public function/method with:
- Name and signature
- Input types and valid ranges
- Output types
- Side effects (DB writes, API calls, file I/O, logging)
- Error conditions (what raises exceptions)

STEP 2 — GENERATE TESTS
For each public function:
- Write a test with representative valid input → expected output
- Write a test for each documented error condition
- Write a test for edge cases (empty input, None, boundary values)
- If the function has side effects, verify the side effects

STEP 3 — VERIFY COVERAGE
Run the new tests and confirm they pass.
Report coverage on the target file before and after adding characterization tests.

RULES:
- Tests must assert on ACTUAL behavior, even if it looks like a bug
- If behavior seems like a bug, add a comment: # NOTE: possible bug, preserving current behavior
- Use descriptive test names: test_{function}_when_{condition}_then_{result}
- Group tests by function
```

---

## Execution Prompts

### Prompt: Extract module

```
Apply "Extract Module" refactoring to {source_file}.

MIGRATION MAP ENTRY:
{paste the specific migration map rows for this extraction}

EXECUTION STEPS:
1. Create the new file at {new_location}
2. Copy the specified functions/classes to the new file
3. Add necessary imports to the new file
4. In the old file, replace the moved code with imports from the new location
   (strangler fig — old file re-exports from new location)
5. **Python __init__.py check**: If the old module is re-exported from any
   `__init__.py` file, add a re-export of the new location there too:
   ```python
   # __init__.py — add temporary re-export to avoid breaking package-level imports
   from {new_module} import {symbol}  # re-export during migration
   ```
   Run `grep -rn "from {package} import {symbol}" {source_root}/` to find
   callers using the package-level import.
6. Run tests — they must all pass
7. Update one caller at a time to import from the new location directly
8. Run tests after each caller update
9. When zero callers use the old re-exports, remove them from the old file
   AND from any `__init__.py` files
10. Run tests one final time

SAFETY CHECKS after each step:
- pytest -x
- ruff check {source_root}/
- mypy {source_root}/

OUTPUT:
- Commit message: "refactor: extract {description} from {source_file} to {new_location}"
- Log entry for refactoring log
```

### Prompt: Consolidate duplicates

```
Apply "Consolidate Duplicates" refactoring.

DUPLICATE LOCATIONS:
{list the files and line ranges containing the duplicated code}

EXECUTION STEPS:
1. Identify the best version of the duplicated code (most complete, best tested)
2. Create or identify the canonical location for this code
3. Move/copy the best version to the canonical location
4. Add tests for the canonical version if not already covered
5. Run tests
6. Replace each duplicate with an import from the canonical location, one at a time
7. Run tests after each replacement
8. Verify all duplicates are eliminated

HANDLE VARIATIONS:
If the duplicates aren't identical, note the differences:
- If differences are parameterizable, add parameters to the canonical version
- If differences represent genuinely different logic, they may not be true duplicates — log and skip

OUTPUT:
- Commit message: "refactor: consolidate {description} into {canonical_location}"
- Log entry noting which duplicates were consolidated and any variations found
```

### Prompt: Fix layering violation

```
Apply "Fix Layering Violation" refactoring.

VIOLATION:
{module_a} in layer {higher_layer} is imported by {module_b} in layer {lower_layer}.

EXPECTED LAYER ORDER (top to bottom):
1. API / Routes (top — handles HTTP)
2. Services (business logic orchestration)
3. Core / Domain (pure business rules)
4. Repositories / DB (data access)
5. Models / Schemas (data definitions)

EXECUTION STEPS:
1. Identify what {module_b} actually needs from {module_a}
2. Determine where that functionality should live:
   - Is it a shared type/interface? → Move to core/models layer
   - Is it a utility function? → Move to core/utils
   - Is it a service call? → Inject as a dependency instead of importing
3. Create the correct home for the shared code
4. Move the code (following the Extract Module pattern)
5. Update both {module_a} and {module_b} to use the new location
6. Run tests after each change
7. Verify the layering violation no longer exists

OUTPUT:
- Commit message: "refactor: fix layering violation — move {description} to {correct_layer}"
```

### Prompt: Split god module

```
Apply "Split God Module" refactoring to {target_file}.

CURRENT STATE:
{target_file} is {line_count} lines with {responsibility_count} responsibilities:
{list each responsibility}

MIGRATION MAP:
{paste migration map for this split}

EXECUTION STEPS:
1. For each responsibility identified in the migration map:
   a. Create new module file
   b. Move related functions/classes (following Extract Module pattern)
   c. Add re-exports in the old file
   d. Run tests
2. After all extractions:
   a. Update callers one by one to import from new locations
   b. Run tests after each update
3. When the old file only contains re-exports:
   a. Check if any caller still imports from the old file
   b. If zero callers remain, delete or convert to __init__.py
   c. Run tests

ORDERING:
Extract in dependency order:
- Extract modules with zero internal dependencies first
- Then extract modules that depend only on already-extracted modules
- The "core" or most-connected responsibility stays in the original file longest

OUTPUT:
- One commit per extracted module
- Commit message: "refactor: extract {responsibility} from {target_file} to {new_file}"
- Final commit: "refactor: complete split of {target_file}"
```

---

## Verification Prompts

### Prompt: Post-refactoring validation

```
Verify that the refactoring of {target} preserved behavior.

VALIDATION STEPS:
1. Run the full test suite and record results
2. Compare test results to the baseline recorded before refactoring:
   - Same number of tests passing?
   - Any new failures?
   - Any new warnings?
3. Run test coverage and compare:
   - Coverage must be ≥ baseline
   - If coverage decreased, identify what's uncovered
4. Run lint and type checks:
   - No new errors
   - No new warnings (unless explicitly accepted)
5. Run complexity analysis on refactored files:
   - Complexity should have decreased or stayed the same
   - File lengths should have decreased
6. Check dependency graph:
   - Circular dependencies should have decreased or stayed the same
   - Import fan-out should have decreased

PRODUCE REPORT:
| Metric | Before | After | Status |
|--------|--------|-------|--------|
| Tests passing | | | |
| Coverage | | | |
| Lint errors | | | |
| Type errors | | | |
| Avg complexity | | | |
| Circular deps | | | |
| Max file length | | | |

VERDICT:
- PASS: All metrics maintained or improved → proceed
- WARN: Metrics maintained but some concerns → review with human
- FAIL: Any metric degraded → revert and investigate
```
