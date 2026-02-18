# 07 — Agent Automation Prompts

## Purpose

This guide provides **concrete, executable prompts** that an AI agent can use to auto-generate each documentation layer. Instead of a human reading code and writing prose, an agent runs these extraction patterns and populates templates directly.

This is the difference between a documentation *process* and a documentation *machine*.

## How to use these prompts

For each documentation layer, there's a set of prompts that:

1. **Extract** — pull structured information from the codebase
2. **Populate** — fill in the corresponding template
3. **Verify** — check the output against the actual code

Give the agent the relevant prompt block along with the template. The agent reads the code, fills the template, and marks anything it can't determine with `[UNVERIFIED]`.

---

## Layer 0 — Reconnaissance Prompts

### Prompt: Repository inventory

```
Analyze this repository and produce a complete reconnaissance report:

1. DIRECTORY STRUCTURE: Run `tree` (or list all directories depth-2) and describe
   the top-level organization pattern (monorepo, single app, frontend+backend, etc.).

2. TECH STACK: Read the package manifest ({pyproject.toml / package.json / go.mod /
   Cargo.toml}) and list:
   - Language + version
   - Framework
   - All runtime dependencies grouped by purpose
   - All dev dependencies
   
3. ENTRY POINTS: Search for all application entry points:
   - Python: look for `if __name__ == "__main__"`, uvicorn/gunicorn references,
     [tool.poetry.scripts], console_scripts, Click/Typer groups
   - Node: look for `"main"`, `"scripts"` in package.json, bin entries
   - Go: look for `func main()` in cmd/ or main.go
   - General: look for Dockerfile CMD/ENTRYPOINT, docker-compose command fields,
     CI/CD start commands
   
4. EXISTING DOCS: List every .md file, note its last-modified date, and assess
   coverage as: ✅ Current / ⚠️ Stale / ❌ Missing / 🔲 Placeholder

5. CONFIGURATION: Find all environment variable references and list them with
   their default values.

Output: a completed reconnaissance checklist using the template.
```

### Stack-specific extraction commands

#### Python (FastAPI / Django / Flask)

```bash
# Find all entry points
grep -r "if __name__" app/ --include="*.py" -l
grep -r "uvicorn\|gunicorn\|app\.run" . --include="*.py" -l

# Find all API route registrations
grep -rn "include_router\|app\.route\|@app\.\(get\|post\|put\|delete\|patch\)" app/ --include="*.py"

# Find all SQLAlchemy models
grep -rn "class.*Base\)\|__tablename__" app/ --include="*.py"

# Find all Pydantic schemas
grep -rn "class.*BaseModel\)\|class.*BaseSchema\)" app/ --include="*.py"

# Find all env var references
grep -rn "os\.environ\|os\.getenv\|env\.\|settings\.\|config\." app/ --include="*.py" | grep -v __pycache__

# Find all scheduled jobs / cron entries
grep -rn "scheduler\|cron\|APScheduler\|celery\|@periodic" app/ --include="*.py"

# Find all external HTTP calls
grep -rn "httpx\|requests\.\(get\|post\|put\|delete\)\|aiohttp" app/ --include="*.py"
```

#### Node.js (Express / Next.js / Fastify)

```bash
# Find all route definitions
grep -rn "router\.\(get\|post\|put\|delete\|patch\)\|app\.\(get\|post\|put\|delete\)" src/ --include="*.ts" --include="*.js"

# Find all model/schema definitions
grep -rn "Schema\|model\|interface.*{" src/ --include="*.ts" --include="*.js"

# Find all env var references
grep -rn "process\.env\.\|env\." src/ --include="*.ts" --include="*.js"

# Find all external API calls
grep -rn "fetch\|axios\|got\.\|node-fetch" src/ --include="*.ts" --include="*.js"
```

---

## Layer 1 — Architecture Prompts

### Prompt: Architecture extraction

```
Produce an architecture overview for this repository.

STEP 1 — TRACE THE MAIN FLOW
Read the main entry point file(s) and trace the complete request/data flow:
- What starts the application?
- What middleware or initialization runs?
- How are routes/handlers registered?
- What services do routes call?
- What data stores are accessed?
- What external services are called?

STEP 2 — IDENTIFY RUNTIME PROCESSES
From docker-compose.yml, Procfile, render.yaml, or deployment config:
- List every distinct process that runs
- For each: entry point, role, how it communicates with others

STEP 3 — MAP INTER-PROCESS COMMUNICATION
How do processes share data?
- Shared database tables?
- Message queue?
- HTTP calls between services?
- Redis pub/sub?

STEP 4 — DRAW SYSTEM DIAGRAM
Create a text-based diagram showing:
- All runtime processes (boxes)
- All data stores (boxes)
- All external services (boxes)
- Data flow arrows between them

STEP 5 — SECURITY MODEL
From auth middleware, route decorators, and config:
- How is authentication handled?
- How is authorization enforced?
- Where are secrets stored?

Output: Populate the architecture-overview.md template.
Mark anything inferred (not directly traced in code) with [UNVERIFIED].
```

### Prompt: Service map extraction

```
Create a complete service map of this codebase.

For EVERY top-level directory/package under the source root:

1. Read the __init__.py (or index.ts/mod.rs/etc.)
2. List every file in the module
3. For each file, read the first 50 lines and all class/function definitions
4. Write a one-line purpose for each file
5. Identify cross-cutting concerns (logging, config, auth, error handling)
6. Map which modules import from which other modules

Output: Populate the service-map.md template with every module covered.
No module should be left out — breadth is more important than depth.
```

---

## Layer 2 — Interface Prompts

### Prompt: API surface extraction

```
Document every API endpoint in this codebase.

EXTRACTION STEPS:
1. Find all route registration files (routers, controllers, handlers)
2. For each route, extract:
   - HTTP method
   - URL path
   - Handler function name and location
   - Authentication requirements (decorators, middleware)
   - Request body schema (Pydantic model, TypeScript interface, etc.)
   - Response schema
   - Status codes (from explicit returns and error handlers)
3. Group endpoints by functional area (auth, admin, core resources, etc.)
4. For the 5 most complex endpoints, document full request/response shapes

Also extract:
- All CLI commands (Click groups, argparse, Typer commands, npm scripts)
- All utility scripts in scripts/ with their purpose and arguments

Output: Populate the api-surface.md template.
Cite the source file for every endpoint.
```

### Prompt: Data model extraction

```
Document every data model / database table in this codebase.

EXTRACTION STEPS:
1. Find all model definitions (SQLAlchemy models, Django models, Prisma schema,
   Mongoose schemas, etc.)
2. For each model/table, extract:
   - Table name
   - Every column with: name, type, constraints, default value
   - Indexes
   - Foreign keys and relationships
3. Find all enum/constant definitions used in models
4. Identify state machines:
   - Find columns with status/state semantics
   - Trace all code that changes these values to discover transitions
   - Document allowed transitions with triggers
5. Read migration files to identify notable schema changes

Output: Populate the data-model.md template.
Draw a text-based ER diagram showing relationships.
```

---

## Layer 3 — Configuration Prompts

### Prompt: Configuration extraction

```
Document every configuration variable in this codebase.

EXTRACTION STEPS:
1. Read the config/settings module (e.g., app/core/config.py, src/config.ts)
2. Read .env.example or .env.template
3. Search all source files for env var references:
   - Python: os.environ, os.getenv, pydantic Settings fields
   - Node: process.env.VARIABLE_NAME
   - Go: os.Getenv
4. For each variable found, determine:
   - Name
   - Type (string, int, bool, URL, etc.)
   - Required or optional (has default?)
   - Default value
   - Purpose (from variable name, comments, or usage context)
5. Group variables by category (core, database, cache, security, external APIs, etc.)
6. Identify feature flags (boolean env vars that enable/disable functionality)

Output: Populate the configuration-guide.md template.
Mark any variable whose purpose is unclear with [UNVERIFIED].
```

### Prompt: Dependency inventory extraction

```
Document every dependency in this codebase.

EXTRACTION STEPS:
1. Read the package manifest and list every dependency with version
2. For each runtime dependency, categorize it:
   - Core framework
   - Database / ORM
   - External communication (HTTP clients, API SDKs)
   - Security / auth
   - Observability (logging, metrics, tracing)
   - Other
3. For each dev dependency, note its purpose (testing, linting, formatting, etc.)
4. Search code for external API calls and document each integration:
   - Service name and purpose
   - Auth method
   - Config variables
   - Link to official docs
5. List infrastructure dependencies (databases, caches, message brokers)
   with versions required

Output: Populate the dependency-inventory.md template.
```

---

## Layer 4 — Operations Prompts

### Prompt: Onboarding guide generation

```
Generate a step-by-step onboarding guide for this codebase.

EXTRACTION STEPS:
1. Read README.md for existing setup instructions
2. Read docker-compose.yml for service definitions
3. Read Makefile / package.json scripts / pyproject.toml scripts for commands
4. Read .env.example for required variables
5. Identify prerequisites from the package manifest (language version, tools)
6. Test (or mentally trace) the complete flow:
   - Clone → install deps → configure env → start services → verify → run tests

For each step, provide the EXACT command to run.
Include troubleshooting for the 3 most common first-run failures.

Output: Populate the codebase-onboarding.md template.
Every command should be copy-pasteable.
```

### Prompt: Deployment extraction

```
Document the deployment model for this codebase.

EXTRACTION STEPS:
1. Read all deployment config files:
   - render.yaml / Procfile / fly.toml / docker-compose.prod.yml
   - .github/workflows / .gitlab-ci.yml / Jenkinsfile
   - Dockerfile(s)
   - Terraform / Pulumi / CDK files
2. For each environment (local, staging, production), document:
   - What runs where
   - How it's triggered (git push, manual, CI)
   - Environment-specific config
3. Document the build and start commands
4. Document database migration process
5. Document rollback procedure

Output: Populate the deployment-and-infra.md template.
```

---

## Layer 5 — Gap Analysis Prompt

### Prompt: Automated gap detection

```
Perform a comprehensive documentation gap analysis.

STEP 1 — COVERAGE AUDIT
For every module in the source tree:
- Check if it appears in docs/service-map.md
- Check if its API endpoints appear in docs/api-surface.md
- Check if its data models appear in docs/data-model.md
- Mark coverage as: Full / Partial / None

STEP 2 — MARKER SWEEP
Search all docs/ files for these markers and collect them:
- [UNVERIFIED] — list each with document and claim
- [TODO] — list each with document and description
- [OUTDATED] — list each with document and issue
- [ASK] — list each with document and question

STEP 3 — DRIFT DETECTION
Compare docs against code for common drift:
- API surface: are there routes in code not in docs?
- Data model: are there columns in models not in docs?
- Config: are there env vars in code not in docs?
- Dependencies: are there packages in manifest not in docs?

STEP 4 — PRIORITIZE
For each gap found:
- P0 if it blocks an agent from completing a task
- P1 if it reduces efficiency but doesn't block

Output: Populate the documentation-gap-analysis.md template.
```

---

## Layer 6 — AGENTS.md Generation Prompt

### Prompt: Agent entry point

```
Write AGENTS.md for this repository.

INPUTS: Read all docs/ files that have been generated.

REQUIREMENTS:
- Under 150 lines total
- Mission: one sentence
- Repository map: numbered reading order of all docs
- System architecture: 3-5 line quick reference
- Key modules: table with module → purpose → key files for EVERY package
- Non-negotiable constraints: rules not suggestions
- Coding conventions: extracted from linter config, existing code patterns
- Common tasks: the 3-5 most frequent change patterns with step-by-step
- Known gotchas: non-obvious things discovered during documentation
- Safety: secrets handling, escalation triggers

Important:
- Every file referenced MUST exist
- Every module in the source tree MUST appear in the key modules table
- Constraints must be verifiable (not "write clean code" but "run ruff check before commit")
```

---

## Composition pattern

For full automated documentation, give the agent this master prompt:

```
You are documenting an existing repository. Follow the repo-documentation
scaffold from coc_scaffold/repo-documentation/.

Execute layers 0–6 in order. For each layer:
1. Read the relevant agent prompt from 07-agent-prompts.md
2. Run the extraction steps
3. Populate the corresponding template from templates/
4. Run the verification checks from 08-verification-and-quality.md
5. Mark anything uncertain with [UNVERIFIED]
6. Move to the next layer

Output all documents into the target repo's docs/ directory.
Output AGENTS.md at the repo root.
```
