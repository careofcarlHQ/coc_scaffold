# 02 — Codebase Assessment Checklist

Use this checklist to systematically assess the structural health of an existing codebase before planning a refactoring effort. Complete this before writing a refactoring plan — it tells you what actually needs to change and what doesn't.

## Prerequisites

- [ ] Repository cloned and buildable locally
- [ ] Test suite runs (even if coverage is low)
- [ ] Access to git history (for hotspot analysis)
- [ ] Familiarity with the system's purpose (or completed [repo-documentation](../repo-documentation/) reconnaissance)

---

## Part 1 — Complexity Metrics (30 minutes)

### 1.1 File-level complexity

- [ ] List all source files with line counts
- [ ] Identify files over 300 lines (candidates for splitting)
- [ ] Identify files over 500 lines (high-priority candidates)

<details><summary>🤖 Extraction commands</summary>

```bash
# Python — file sizes sorted by length
find app/ -name "*.py" -exec wc -l {} \; | sort -rn | head -30

# TypeScript/JavaScript
find src/ -name "*.ts" -o -name "*.tsx" | xargs wc -l | sort -rn | head -30

# Go
find . -name "*.go" -not -path "./vendor/*" -exec wc -l {} \; | sort -rn | head -30
```
</details>

### 1.2 Function-level complexity

- [ ] Run `radon cc {source_root}/ -a -nc` to measure cyclomatic complexity (install with `pip install radon` if needed)
- [ ] Identify functions over 50 lines (candidates for extraction)
- [ ] Identify functions with cyclomatic complexity > 10
- [ ] Identify deeply nested code (> 4 indentation levels)

> **Tool-first rule:** Always run the extraction commands below and parse the output. Do not estimate metrics by reading code — tools are faster and more accurate.

<details><summary>🤖 Extraction commands — Python</summary>

```bash
# Install radon for Python complexity analysis
pip install radon

# Cyclomatic complexity (shows functions rated C or worse)
radon cc app/ -a -nc

# Maintainability index per file
radon mi app/ -s

# Find long functions (basic heuristic: lines between def/class)
grep -n "def \|class " app/**/*.py | head -50
```
</details>

<details><summary>🤖 Extraction commands — TypeScript</summary>

```bash
# Install complexity reporter
npx ts-complexity src/

# Or use eslint with complexity rule
npx eslint src/ --rule '{"complexity": ["warn", 10]}' --no-eslintrc
```
</details>

### 1.3 Code duplication

- [ ] Run duplication analysis
- [ ] List blocks duplicated in 3+ places
- [ ] Estimate percentage of duplicated code

<details><summary>🤖 Extraction commands</summary>

```bash
# Python — find duplicate blocks
pip install pylint
pylint app/ --disable=all --enable=duplicate-code --min-similarity-lines=6

# General — jscpd (works for any language)
npx jscpd app/ --min-lines 5 --min-tokens 50

# Quick manual check — find identical function signatures
grep -rn "def " app/ --include="*.py" | awk -F: '{print $3}' | sort | uniq -c | sort -rn | head -20
```
</details>

**Record findings:**
```
Files over 300 lines: ___
Files over 500 lines: ___
Functions over 50 lines: ___
Functions with CC > 10: ___
Duplication percentage: ___%
```

---

## Part 2 — Dependency Analysis (30 minutes)

### 2.1 Internal dependency graph

- [ ] Map which modules import from which other modules
- [ ] Identify circular dependencies
- [ ] Identify modules with > 10 internal importers (high coupling)
- [ ] Identify modules that import from > 5 other internal modules (high fan-out)

<details><summary>🤖 Extraction commands — Python</summary>

```bash
# Map all internal imports
grep -rn "from app\." app/ --include="*.py" | \
  sed 's/.*from \(app\.[a-zA-Z_.]*\).*/\1/' | sort | uniq -c | sort -rn

# Find circular imports (using pydeps)
pip install pydeps
pydeps app/ --cluster --no-show

# Find most-imported modules
grep -rn "from app\." app/ --include="*.py" | \
  sed 's/.*from \(app\.[a-zA-Z_.]*\) import.*/\1/' | sort | uniq -c | sort -rn | head -15

# Find modules with highest fan-out
for f in $(find app/ -name "*.py"); do
  count=$(grep -c "from app\." "$f" 2>/dev/null)
  [ "$count" -gt 5 ] && echo "$count $f"
done | sort -rn
```
</details>

<details><summary>🤖 Extraction commands — TypeScript</summary>

```bash
# Map internal imports
grep -rn "from '\.\./\|from '\./\|from '@/" src/ --include="*.ts" | head -40

# Find most-imported modules
grep -rn "from.*import" src/ --include="*.ts" | \
  sed "s/.*from ['\"]//;s/['\"].*//" | sort | uniq -c | sort -rn | head -15
```
</details>

### 2.2 Layering violations

- [ ] Identify your intended architecture layers (e.g., routes → services → repositories → models)
- [ ] Check for violations (e.g., routes importing directly from DB models)
- [ ] List all layer-crossing imports

<details><summary>🤖 Extraction commands — Python (FastAPI pattern)</summary>

```bash
# Routes should not import from db directly
grep -rn "from app.db" app/api/ --include="*.py"

# Services should not import from api
grep -rn "from app.api" app/services/ --include="*.py"

# Models should not import from services
grep -rn "from app.services" app/db/ --include="*.py"
```
</details>

### 2.3 God modules

- [ ] Identify modules that do too many things (> 5 unrelated responsibilities)
- [ ] Identify "utils" or "helpers" modules that are catch-all dumping grounds
- [ ] Identify modules where the name no longer matches the content

**Record findings:**
```
Circular dependencies: ___
High-coupling modules (>10 importers): ___
High-fan-out modules (>5 imports): ___
Layering violations: ___
God modules: ___
```

---

## Part 3 — Change Hotspots (15 minutes)

### 3.1 Git history analysis

Files that change frequently are the highest-value refactoring targets — they're where developers spend the most time.

- [ ] Identify the 20 most frequently changed files
- [ ] Cross-reference with complexity: high churn + high complexity = top priority
- [ ] Identify files that often change together (coupling evidence)

<details><summary>🤖 Extraction commands</summary>

```bash
# Most frequently changed files (last 6 months)
git log --since="6 months ago" --name-only --pretty=format: | \
  grep -v "^$" | sort | uniq -c | sort -rn | head -20

# Files changed together most often (co-change analysis)
git log --since="6 months ago" --name-only --pretty=format:"---" | \
  awk '/^---$/{if(NR>1) for(i in files) for(j in files) if(i<j) print i" + "j; delete files; next} {files[$0]=1}' | \
  sort | uniq -c | sort -rn | head -20

# Churn × complexity hotspots (manual cross-reference)
# Compare the churn list above with the complexity output from Part 1
```
</details>

**Record findings:**
```
Top 5 hotspot files:
1. _______________
2. _______________
3. _______________
4. _______________
5. _______________
```

---

## Part 4 — Test Coverage (15 minutes)

### 4.1 Coverage by module

- [ ] Run test coverage and record per-module percentages
- [ ] Identify modules with < 50% coverage
- [ ] Identify modules with 0% coverage
- [ ] Cross-reference: modules targeted for refactoring must have adequate coverage first

<details><summary>🤖 Extraction commands — Python</summary>

```bash
# Run coverage
pytest --cov=app --cov-report=term-missing --cov-report=html

# Coverage per module
pytest --cov=app --cov-report=term | grep -E "^app/" | sort -t% -k4 -n

# Find untested files
pytest --cov=app --cov-report=term | grep " 0%"
```
</details>

<details><summary>🤖 Extraction commands — TypeScript</summary>

```bash
# Run coverage
npx jest --coverage

# Or vitest
npx vitest run --coverage
```
</details>

### 4.2 Test quality assessment

- [ ] Are tests mostly unit tests, integration tests, or end-to-end?
- [ ] Do tests test behavior (what) or implementation (how)?
- [ ] Are there flaky tests?
- [ ] How long does the test suite take to run?

**Record findings:**
```
Overall coverage: ___%
Modules below 50%: ___
Modules at 0%: ___
Test suite runtime: ___
Flaky tests: ___
```

---

## Part 5 — Code Smells (15 minutes)

### 5.1 Known smell patterns

Check for these common structural problems:

- [ ] **Long parameter lists** — functions with > 5 parameters
- [ ] **Feature envy** — functions that use more data from other modules than their own
- [ ] **Shotgun surgery** — a single logical change requires editing 5+ files
- [ ] **Divergent change** — one file changes for many different reasons
- [ ] **Data clumps** — same group of values passed together repeatedly
- [ ] **Primitive obsession** — using strings/dicts where domain objects would be clearer
- [ ] **Dead code** — functions/classes that are never called
- [ ] **Magic numbers/strings** — literals scattered through the code

<details><summary>🤖 Extraction commands</summary>

```bash
# Find long parameter lists (Python)
grep -rn "def " app/ --include="*.py" | awk -F',' '{if(NF>5) print NR": "$0}'

# Find potentially dead code (Python — vulture)
pip install vulture
vulture app/ --min-confidence 80

# Find magic strings/numbers
grep -rn "['\"][a-z_]*['\"]" app/ --include="*.py" | grep -v "import\|#\|def \|class " | head -30
```
</details>

### 5.2 Team pain points

- [ ] Ask the team: "What part of the code do you dread changing?"
- [ ] Ask: "What area causes the most bugs?"
- [ ] Ask: "What takes longest to understand when onboarding?"
- [ ] Ask: "Where do you wish there were better abstractions?"

Record answers — these are often the highest-impact refactoring targets, even if metrics don't flag them.

---

## Part 6 — Assessment Summary

### Health scorecard

| Dimension | Score (1–5) | Notes |
|-----------|-------------|-------|
| Complexity | ___ | 5 = low complexity, 1 = many complex files |
| Coupling | ___ | 5 = loose coupling, 1 = circular/tight coupling |
| Coverage | ___ | 5 = >80%, 1 = <30% |
| Duplication | ___ | 5 = <5%, 1 = >20% |
| Naming | ___ | 5 = clear, 1 = misleading |
| Layering | ___ | 5 = clean layers, 1 = no discernible layers |

### Top refactoring targets

Ranked by impact × frequency × risk:

| Rank | Target | Problem | Impact | Frequency | Score |
|------|--------|---------|--------|-----------|-------|
| 1 | ___ | ___ | ___ | ___ | ___ |
| 2 | ___ | ___ | ___ | ___ | ___ |
| 3 | ___ | ___ | ___ | ___ | ___ |
| 4 | ___ | ___ | ___ | ___ | ___ |
| 5 | ___ | ___ | ___ | ___ | ___ |

### Verdict

```
Overall code health: good / acceptable / needs work / critical
Recommended scope: targeted / moderate / broad
Estimated phases: ___
Prerequisites before refactoring: ___
```
