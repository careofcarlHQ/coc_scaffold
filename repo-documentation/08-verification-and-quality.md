# 08 — Verification and Quality

## Purpose

Documentation that _might_ be correct is marginally better than no documentation. Gold-standard documentation is **provably correct** — you can verify every claim against the actual code.

This guide provides verification techniques for each document type, a quality scoring model, and concrete checks an agent can run to validate documentation accuracy.

## The verification hierarchy

```
Level 0 — Exists           Document was created                     ⬜ Baseline
Level 1 — Structured       Template fully populated, no blank cells ⬜ Usable
Level 2 — Sourced          Every claim cites a file path            ⬜ Traceable
Level 3 — Verified         Claims checked against current code      ✅ Gold standard
Level 4 — Continuously     Auto-checks catch drift within 1 week   🏆 Self-healing
```

Most frameworks stop at Level 1. Gold standard means Level 3 minimum, with Level 4 for high-drift documents (API surface, config).

## Per-document verification

### Architecture overview

| Check | How to verify | Automated? |
|-------|--------------|------------|
| System diagram matches code | Compare processes in diagram vs docker-compose/deployment config | ✅ |
| Tech stack versions correct | Compare against package manifest | ✅ |
| Data flow is accurate | Trace from entry point through code | Partial — agent can trace |
| Security model correct | Compare against auth middleware | ✅ |
| Non-goals still valid | Requires human judgment | ❌ |

```bash
# Verify runtime processes match deployment config
grep -E "command:|startCommand:|CMD |ENTRYPOINT " docker-compose.yml render.yaml Dockerfile 2>/dev/null
```

### API surface

| Check | How to verify | Automated? |
|-------|--------------|------------|
| All routes documented | Compare doc endpoints vs code routes | ✅ |
| Methods correct | Compare HTTP methods | ✅ |
| Auth requirements correct | Check route decorators/middleware | ✅ |
| Request/response shapes correct | Compare schemas vs doc | ✅ |
| No undocumented endpoints | Diff code routes against doc | ✅ |

```bash
# Python/FastAPI: extract all routes from code
grep -rn "@.*\.\(get\|post\|put\|delete\|patch\)" app/api/ --include="*.py" | \
  sed 's/.*@.*\.\(get\|post\|put\|delete\|patch\)(\"\(.*\)\".*/\U\1 \2/'

# Compare against documented endpoints
grep -E "^\| (GET|POST|PUT|DELETE|PATCH)" docs/api-surface.md | awk '{print $2, $4}'
```

### Data model

| Check | How to verify | Automated? |
|-------|--------------|------------|
| All tables documented | Compare doc tables vs model files | ✅ |
| Column types match code | Compare doc types vs model definitions | ✅ |
| State transitions match code | Trace transition logic in code | Partial |
| Indexes documented | Compare against migration files | ✅ |
| No undocumented tables | Diff model files against doc | ✅ |

```bash
# Python/SQLAlchemy: extract all model classes
grep -rn "__tablename__" app/db/models/ --include="*.py"

# Compare against documented tables
grep -E "^### \`" docs/data-model.md
```

### Configuration guide

| Check | How to verify | Automated? |
|-------|--------------|------------|
| All env vars documented | Diff code references vs doc | ✅ |
| Types correct | Check config class / usage | ✅ |
| Defaults correct | Check config class / .env.example | ✅ |
| Required/optional correct | Check if var has default | ✅ |
| No undocumented vars | Search all source for env references | ✅ |

```bash
# Find all env vars referenced in code but not in docs
comm -23 \
  <(grep -roh '[A-Z_]\{3,\}' app/ --include="*.py" | sort -u) \
  <(grep -oh '`[A-Z_]\{3,\}`' docs/configuration-guide.md | tr -d '`' | sort -u)
```

### Service map

| Check | How to verify | Automated? |
|-------|--------------|------------|
| All modules listed | Diff source directories vs doc | ✅ |
| File lists current | Diff actual files vs doc | ✅ |
| Purposes accurate | Read code, compare to description | Partial |
| Dependency graph correct | Analyze imports | ✅ |

```bash
# List all modules in source tree
find app/ -maxdepth 1 -type d | sort

# Compare against documented modules
grep -E "^### \`" docs/service-map.md | sed "s/### \`\(.*\)\/\`.*/\1/"
```

## Quality scoring model

Score each document on these dimensions:

| Dimension | 0 | 1 | 2 | 3 |
|-----------|---|---|---|---|
| **Completeness** | Major sections empty | >50% populated | >90% populated | 100% populated |
| **Accuracy** | Not verified | Spot-checked | Systematically verified | Auto-verified |
| **Sourcing** | No file citations | Some citations | Every factual claim cited | Cited + line numbers |
| **Freshness** | No date | Date set, possibly stale | Date within freshness window | Auto-refreshed |
| **Usability** | Unstructured prose | Uses template | Follows writing guide | Tested with agent task |

**Scoring**: Sum all dimensions. Max = 15 per document.

| Score | Rating |
|-------|--------|
| 0–5 | ❌ Draft — not reliable |
| 6–9 | ⚠️ Working — usable with caution |
| 10–12 | ✅ Solid — reliable for daily use |
| 13–15 | 🏆 Gold — verified, sourced, fresh |

### Documentation health dashboard

```markdown
# Documentation Health — {project_name}

> Last assessed: YYYY-MM-DD

| Document | Complete | Accurate | Sourced | Fresh | Usable | Score | Rating |
|----------|----------|----------|---------|-------|--------|-------|--------|
| architecture-overview.md | /3 | /3 | /3 | /3 | /3 | /15 | |
| service-map.md | /3 | /3 | /3 | /3 | /3 | /15 | |
| api-surface.md | /3 | /3 | /3 | /3 | /3 | /15 | |
| data-model.md | /3 | /3 | /3 | /3 | /3 | /15 | |
| configuration-guide.md | /3 | /3 | /3 | /3 | /3 | /15 | |
| dependency-inventory.md | /3 | /3 | /3 | /3 | /3 | /15 | |
| codebase-onboarding.md | /3 | /3 | /3 | /3 | /3 | /15 | |
| deployment-and-infra.md | /3 | /3 | /3 | /3 | /3 | /15 | |
| operational-runbook.md | /3 | /3 | /3 | /3 | /3 | /15 | |
| AGENTS.md | /3 | /3 | /3 | /3 | /3 | /15 | |
| **Average** | | | | | | **/15** | |
```

## Agent verification prompt

Use this prompt after generating documentation to verify quality:

```
You just generated documentation for this repository. Now verify it.

For each document:

1. COMPLETENESS: Are there any empty sections, blank table cells, or
   unfilled placeholders? List them.

2. ACCURACY: For each factual claim, trace it to the source code.
   Flag any claim that doesn't match what the code actually does.
   Specifically check:
   - API endpoints: do they exist with the documented method and path?
   - Data model columns: do they exist with the documented types?
   - Config variables: do they exist with the documented defaults?
   - State transitions: do the documented transitions match the code?

3. SOURCING: Does every factual claim cite a source file?
   List any unsourced claims.

4. FRESHNESS: Set Last verified to today's date for any document
   that passes accuracy checks.

5. CROSS-REFERENCES: Does every linked document actually exist?
   Does AGENTS.md reference all key documents?

Output: A verification report listing each document, its score on
the 0-3 scale for each dimension, and specific items to fix.
```

## Automated drift detection

For Level 4 (self-healing) documentation, add these checks to CI or a scheduled agent task:

### API drift check
```python
"""Compare documented endpoints against actual route registrations."""
import re
from pathlib import Path

def extract_routes_from_code(api_dir: str) -> set:
    routes = set()
    for f in Path(api_dir).rglob("*.py"):
        content = f.read_text()
        for match in re.finditer(r'@\w+\.(get|post|put|delete|patch)\("([^"]+)"', content):
            routes.add(f"{match.group(1).upper()} {match.group(2)}")
    return routes

def extract_routes_from_docs(doc_path: str) -> set:
    routes = set()
    content = Path(doc_path).read_text()
    for match in re.finditer(r'\|\s*(GET|POST|PUT|DELETE|PATCH)\s*\|\s*(\S+)', content):
        routes.add(f"{match.group(1)} {match.group(2)}")
    return routes

code_routes = extract_routes_from_code("app/api")
doc_routes = extract_routes_from_docs("docs/api-surface.md")

undocumented = code_routes - doc_routes
phantom = doc_routes - code_routes

if undocumented:
    print(f"⚠️  UNDOCUMENTED routes: {undocumented}")
if phantom:
    print(f"⚠️  PHANTOM routes (in docs, not in code): {phantom}")
if not undocumented and not phantom:
    print("✅ API surface docs match code")
```

### Config drift check
```python
"""Compare documented env vars against actual references in code."""
import re
from pathlib import Path

def extract_vars_from_code(src_dir: str) -> set:
    vars = set()
    for f in Path(src_dir).rglob("*.py"):
        content = f.read_text()
        for match in re.finditer(r'os\.(?:environ|getenv)\(?["\']([A-Z_]+)', content):
            vars.add(match.group(1))
        # pydantic-settings fields (Field aliases or attribute names)
        for match in re.finditer(r'(\w+):\s*\w+\s*=\s*Field\(', content):
            vars.add(match.group(1).upper())
    return vars

def extract_vars_from_docs(doc_path: str) -> set:
    vars = set()
    content = Path(doc_path).read_text()
    for match in re.finditer(r'`([A-Z_]{3,})`', content):
        vars.add(match.group(1))
    return vars

code_vars = extract_vars_from_code("app")
doc_vars = extract_vars_from_docs("docs/configuration-guide.md")

undocumented = code_vars - doc_vars
if undocumented:
    print(f"⚠️  UNDOCUMENTED env vars: {undocumented}")
else:
    print("✅ Config docs match code")
```

## The gold standard test

Your documentation is gold standard when an agent can:

1. **Navigate**: Given only AGENTS.md, find the answer to any structural question about the repo
2. **Implement**: Add a new endpoint using only the docs and existing code patterns (no human guidance)
3. **Debug**: Diagnose a production issue using the runbook without prior operational knowledge
4. **Verify**: Run automated checks that confirm docs match code with zero false positives

Test this by giving an agent a concrete task (e.g., "add a new admin endpoint that returns destination health") and measuring whether it can complete it using only the repository documentation.
