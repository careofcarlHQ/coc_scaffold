# 02 — Reconnaissance Checklist

Use this checklist to systematically inventory an existing repository. Complete this before writing any documentation — it tells you what you're working with and where the gaps are.

## Prerequisites

- [ ] Repository cloned locally
- [ ] Can build/run the project (or know why you can't)
- [ ] Access to production environment info (or know who has it)

---

## Part 1 — Repository Structure (15 minutes)

### 1.1 Directory layout

- [ ] Run `tree` (or equivalent) and save the output
- [ ] Identify the top-level structure pattern:
  - [ ] Monorepo / multi-package?
  - [ ] Single app with modules?
  - [ ] Frontend + backend split?
  - [ ] Other: _______________

<details><summary>🤖 Extraction commands</summary>

```bash
# Directory tree (depth 3)
find . -maxdepth 3 -type d \
  ! -path './.git/*' ! -path './node_modules/*' ! -path './__pycache__/*' \
  ! -path './.venv/*' ! -path './venv/*' ! -path './.mypy_cache/*' \
  | sort | sed 's|[^/]*/|  |g'

# Detect monorepo (look for multiple package manifests)
find . -maxdepth 3 \( -name "package.json" -o -name "pyproject.toml" -o -name "go.mod" \) \
  ! -path './node_modules/*' 2>/dev/null

# Count source files by language
find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.go" -o -name "*.rs" \) \
  ! -path './node_modules/*' ! -path './.venv/*' | sed 's/.*\.//' | sort | uniq -c | sort -rn
```
</details>

### 1.2 Key files at root

- [ ] README.md — exists? current? useful?
- [ ] AGENTS.md — exists? useful for agents?
- [ ] Package manifest (package.json / pyproject.toml / go.mod / Cargo.toml / etc.)
- [ ] Lock file (package-lock.json / poetry.lock / etc.)
- [ ] Config files (tsconfig.json / .eslintrc / ruff.toml / etc.)
- [ ] Docker files (Dockerfile / docker-compose.yml)
- [ ] CI/CD config (.github/workflows / .gitlab-ci.yml / render.yaml / etc.)
- [ ] Environment template (.env.example / .env.template)
- [ ] .gitignore

<details><summary>🤖 Extraction commands</summary>

```bash
# List all root-level files with modification dates
ls -la --time-style=long-iso *.md *.toml *.json *.yaml *.yml *.cfg *.ini \
  Dockerfile* docker-compose* .env* .gitignore 2>/dev/null | sort -k6

# Check for CI/CD configs
ls -la .github/workflows/*.yml .gitlab-ci.yml render.yaml \
  Jenkinsfile .circleci/config.yml 2>/dev/null

# README freshness
git log -1 --format="%ci %s" -- README.md
```
</details>

### 1.3 Documentation directory

- [ ] Does `docs/` exist?
- [ ] How many files/subdirectories?
- [ ] Is there a docs index (docs/README.md)?
- [ ] Quick freshness check: when were docs last modified?

<details><summary>🤖 Extraction commands</summary>

```bash
# Documentation inventory
find docs/ -type f 2>/dev/null | sort
find docs/ -type f 2>/dev/null | wc -l

# Freshness check — last modified dates
find docs/ -type f -name "*.md" -exec git log -1 --format="%ci  {}" {} \; 2>/dev/null | sort

# Find inline documentation (docstrings, JSDoc)
grep -rn '"""' app/ --include="*.py" | head -5   # Python docstrings
grep -rn '/\*\*' src/ --include="*.ts" | head -5  # JSDoc/TSDoc
```
</details>

**Record findings:**
```
Root structure: _______________
Package manager: _______________
Docs directory: exists / missing / partial
Last doc update: _______________
```

---

## Part 2 — Tech Stack Identification (15 minutes)

### 2.1 Languages and frameworks

Read the package manifest and source code to identify:

- [ ] Primary language: _______________
- [ ] Framework: _______________
- [ ] Runtime version: _______________

<details><summary>🤖 Extraction commands — Python</summary>

```bash
# Python version
python --version 2>/dev/null || python3 --version
grep -i "python" pyproject.toml setup.cfg setup.py 2>/dev/null | grep -i "version\|requires"

# Framework detection
grep -E "fastapi|django|flask|starlette|tornado|sanic|litestar" pyproject.toml requirements*.txt 2>/dev/null

# All dependencies (runtime)
grep -A100 "\[tool.poetry.dependencies\]" pyproject.toml | grep -B0 "^\[" | head -50
# or: pip list --format=columns 2>/dev/null | head -30
```
</details>

<details><summary>🤖 Extraction commands — Node.js</summary>

```bash
# Node/npm version
node --version 2>/dev/null; npm --version 2>/dev/null

# Framework detection
grep -E "express|next|nuxt|fastify|nest|koa|hono" package.json 2>/dev/null

# All dependencies
jq '.dependencies' package.json 2>/dev/null
```
</details>

### 2.2 Data stores

- [ ] Primary database: _______________
- [ ] Cache/queue: _______________
- [ ] File storage: _______________
- [ ] Other: _______________

<details><summary>🤖 Extraction commands</summary>

```bash
# Database detection from dependencies
grep -iE "postgres|mysql|sqlite|mongo|redis|elasticsearch|dynamodb|sqlalchemy|prisma|typeorm|sequelize|drizzle" \
  pyproject.toml package.json requirements*.txt 2>/dev/null

# Database URLs in config
grep -rn "DATABASE_URL\|REDIS_URL\|MONGO_URI\|DB_HOST" app/ src/ --include="*.py" --include="*.ts" 2>/dev/null

# Docker-compose services (often reveals data stores)
grep -A5 "image:" docker-compose.yml 2>/dev/null
```
</details>

### 2.3 External services / integrations

List all external APIs, services, or platforms the code communicates with:

- [ ] Service 1: _______________
- [ ] Service 2: _______________
- [ ] Service 3: _______________
- [ ] (add more as needed)

<details><summary>🤖 Extraction commands</summary>

```bash
# Find HTTP client calls (outbound integrations)
grep -rn "httpx\.\|requests\.\|aiohttp\.\|fetch(\|axios\.\|got(" app/ src/ --include="*.py" --include="*.ts" 2>/dev/null

# Find base URLs / API endpoints
grep -rn "https://\|http://" app/ src/ --include="*.py" --include="*.ts" 2>/dev/null | grep -v "localhost\|127.0.0.1\|test"

# Find webhook / callback handlers
grep -rn "webhook\|callback\|hook" app/ src/ --include="*.py" --include="*.ts" 2>/dev/null
```
</details>

### 2.4 Dev/test tools

- [ ] Test framework: _______________
- [ ] Linter: _______________
- [ ] Formatter: _______________
- [ ] Type checker: _______________
- [ ] CI system: _______________

<details><summary>🤖 Extraction commands</summary>

```bash
# Python dev tools
grep -E "pytest|ruff|black|isort|mypy|flake8|pylint|bandit|pre-commit" pyproject.toml 2>/dev/null

# Node.js dev tools
jq '.devDependencies' package.json 2>/dev/null

# Check for pre-commit hooks
cat .pre-commit-config.yaml 2>/dev/null | head -30
```
</details>

**Example (coc_capi):**
```
Language: Python 3.11
Framework: FastAPI + SQLAlchemy (async) + APScheduler
Database: PostgreSQL 15 (via asyncpg)
Cache/Queue: Redis 7
External: Meta CAPI, TikTok Events, Google Ads, GA4, Snapchat, Criteo, Askås, Bloomreach
Test: pytest + pytest-asyncio
Lint: ruff + black + isort + mypy
CI: Render (render.yaml)
```

---

## Part 3 — Entry Points and Runtime Model (20 minutes)

### 3.1 Application entry points

Find all ways the system starts or is invoked:

- [ ] Web server entry point: _______________
- [ ] Worker/background entry point: _______________
- [ ] CLI commands: _______________
- [ ] Cron/scheduled jobs: _______________
- [ ] Migration commands: _______________
- [ ] Scripts (one-off or utility): _______________

<details><summary>🤖 Extraction commands</summary>

```bash
# Python entry points (pyproject.toml scripts section)
grep -A20 "\[tool.poetry.scripts\]" pyproject.toml 2>/dev/null
grep -A20 "\[project.scripts\]" pyproject.toml 2>/dev/null

# Find __main__.py files (module entry points)
find . -name "__main__.py" ! -path "./.venv/*" 2>/dev/null

# Find uvicorn/gunicorn app references
grep -rn "uvicorn\|gunicorn\|app:app\|create_app" . --include="*.py" --include="*.yaml" --include="*.toml" 2>/dev/null

# Procfile / render.yaml / docker-compose commands
cat Procfile 2>/dev/null
grep "startCommand\|command:" render.yaml docker-compose.yml 2>/dev/null

# Node.js entry points
jq '.scripts' package.json 2>/dev/null
jq '.main, .bin' package.json 2>/dev/null

# Find CLI definitions
grep -rn "click.command\|typer\|argparse\|commander\|yargs" . --include="*.py" --include="*.ts" --include="*.js" 2>/dev/null
```
</details>

### 3.2 Runtime processes

How many distinct processes run in production?

- [ ] Process 1: _______________ (what it does)
- [ ] Process 2: _______________ (what it does)
- [ ] Process 3: _______________ (what it does)

<details><summary>🤖 Extraction commands</summary>

```bash
# Render.yaml services
grep -B2 "type:\|startCommand:" render.yaml 2>/dev/null

# Docker-compose services
grep "^\s*[a-z].*:" docker-compose.yml 2>/dev/null | grep -v "image:\|build:\|ports:\|volumes:\|environment:\|depends_on:\|command:"

# Procfile
cat Procfile 2>/dev/null

# Kubernetes deployments
find . -name "*.yaml" -path "*/k8s/*" -exec grep -l "kind: Deployment" {} \; 2>/dev/null
```
</details>

### 3.3 Inter-process communication

How do the processes communicate?

- [ ] Shared database
- [ ] Message queue / Redis pub-sub
- [ ] HTTP calls between services
- [ ] File system
- [ ] Other: _______________

**Example (coc_capi):**
```
Entry points:
  Web: uvicorn app.main:app
  Worker: poetry run python -m app.dispatch.worker
  Cron: poetry run python -m app.jobs.fetch_askas_orders (etc.)
  CLI: poetry run replay-dispatch

Runtime processes: 3 (web, worker, cron jobs)
Communication: Shared PostgreSQL + Redis
```

---

## Part 4 — Source Code Structure (30 minutes)

### 4.1 Module inventory

List every top-level package/module and its apparent purpose (one line each):

| Module | Apparent purpose |
|--------|-----------------|
| | |
| | |
| | |

<details><summary>🤖 Extraction commands</summary>

```bash
# Python: list top-level packages with their docstrings
for d in app/*/; do
  mod=$(basename "$d")
  doc=$(head -3 "$d/__init__.py" 2>/dev/null | grep -o '""".*"""' | tr -d '"')
  printf "%-20s %s\n" "$mod" "${doc:-[no docstring]}"
done

# Node.js: list top-level source directories
find src/ -maxdepth 1 -type d 2>/dev/null | tail -n+2

# File count per module (rough size indicator)
for d in app/*/; do
  echo "$(find "$d" -name "*.py" | wc -l) files  $d"
done | sort -rn
```
</details>

### 4.2 API surface

- [ ] Count of API routes/endpoints: ___
- [ ] Are routes defined in a single file or spread across modules?
- [ ] API versioning scheme: _______________
- [ ] Authentication mechanism: _______________

<details><summary>🤖 Extraction commands</summary>

```bash
# FastAPI / Starlette routes
grep -rn "@router\.\|@app\.\(get\|post\|put\|patch\|delete\)" app/ --include="*.py" 2>/dev/null

# Express / Fastify routes
grep -rn "router\.\(get\|post\|put\|patch\|delete\)\|app\.\(get\|post\|put\|patch\|delete\)" src/ --include="*.ts" --include="*.js" 2>/dev/null

# Router registration (how routes are mounted)
grep -rn "include_router\|app.use\|app.register" app/ src/ --include="*.py" --include="*.ts" 2>/dev/null

# Auth/middleware
grep -rn "Depends(\|middleware\|authenticate\|authorize\|Bearer\|api.key\|X-.*Token" app/ src/ --include="*.py" --include="*.ts" 2>/dev/null
```
</details>

### 4.3 Data model

- [ ] Count of database tables/models: ___
- [ ] ORM used: _______________
- [ ] Migration tool: _______________
- [ ] Are state machines/enums defined? Where?

<details><summary>🤖 Extraction commands</summary>

```bash
# SQLAlchemy models
grep -rn "class.*Base\)\|class.*Model\)\|__tablename__" app/ --include="*.py" 2>/dev/null

# Prisma models
grep -n "^model " prisma/schema.prisma 2>/dev/null

# Django models
grep -rn "class.*models.Model" . --include="*.py" 2>/dev/null

# Enums
grep -rn "class.*Enum\)\|class.*StrEnum\)" app/ --include="*.py" 2>/dev/null

# Alembic/migration count
ls alembic/versions/*.py 2>/dev/null | wc -l
ls migrations/*.py 2>/dev/null | wc -l
```
</details>

### 4.4 Background processing

- [ ] Queue mechanism: _______________
- [ ] Retry/backoff strategy: _______________
- [ ] Dead-letter handling: _______________

<details><summary>🤖 Extraction commands</summary>

```bash
# Job/task/worker patterns
grep -rn "celery\|dramatiq\|rq\|bull\|apscheduler\|cron\|schedule\|worker" app/ src/ --include="*.py" --include="*.ts" 2>/dev/null

# Retry patterns
grep -rn "retry\|backoff\|max_retries\|attempts\|exponential" app/ src/ --include="*.py" --include="*.ts" 2>/dev/null

# Scheduled job definitions
grep -rn "cron\|interval\|schedule\|every\|periodic" app/ src/ --include="*.py" --include="*.ts" 2>/dev/null
```
</details>

### 4.5 Observability

- [ ] Logging framework: _______________
- [ ] Metrics/monitoring: _______________
- [ ] Health check endpoint: _______________

<details><summary>🤖 Extraction commands</summary>

```bash
# Logging framework
grep -rn "structlog\|logging\|winston\|pino\|bunyan" app/ src/ --include="*.py" --include="*.ts" 2>/dev/null | head -5

# Metrics
grep -rn "prometheus\|datadog\|statsd\|opentelemetry\|newrelic" app/ src/ pyproject.toml package.json 2>/dev/null

# Health endpoints
grep -rn "health\|readiness\|liveness\|healthz\|ready" app/ src/ --include="*.py" --include="*.ts" 2>/dev/null
```
</details>

**Example (coc_capi):**
```
Modules:
  app/api/       — HTTP endpoints (admin, auth, ingest, health, events, destinations, collect)
  app/cli/       — CLI commands (replay)
  app/core/      — Configuration, crypto, security, Redis, logging
  app/db/        — Models, migrations, repository layer
  app/dispatch/  — Event dispatch worker
  app/ingestion/ — Event ingestion pipeline
  app/jobs/      — Scheduled jobs (fetch, retry, cleanup, reconcile)
  app/schemas/   — Pydantic request/response schemas
  app/services/  — Business logic (dispatch, replay, monitoring, stats, etc.)

API routes: ~30+ across 8 router modules
Auth: Admin token (X-Admin-Token header) + MFA (TOTP)
Database: ~10+ tables, SQLAlchemy async, Alembic migrations
Queue: PostgreSQL dispatch_queue table, polled by worker
Observability: structlog + prometheus-fastapi-instrumentator
Health: /healthz endpoint
```

---

## Part 5 — Deployment and Infrastructure (15 minutes)

### 5.1 Deployment target

- [ ] Where does it run? _______________
- [ ] Deployment method: _______________
- [ ] Infrastructure as code? (Terraform, Pulumi, render.yaml, etc.)

<details><summary>🤖 Extraction commands</summary>

```bash
# IaC files
ls render.yaml terraform/ pulumi/ cdk/ serverless.yml k8s/ 2>/dev/null

# Dockerfile analysis
head -5 Dockerfile 2>/dev/null   # base image
grep -i "expose\|port\|cmd\|entrypoint" Dockerfile 2>/dev/null

# CI/CD pipeline
cat .github/workflows/*.yml 2>/dev/null | grep -A3 "deploy\|release"
```
</details>

### 5.2 Environment configuration

- [ ] How are secrets managed? _______________
- [ ] How many environment variables? (estimate)
- [ ] Is there a .env.example? Complete?

<details><summary>🤖 Extraction commands</summary>

```bash
# All environment variable references in code
grep -rn "os.environ\|os.getenv\|process.env\|env(" app/ src/ --include="*.py" --include="*.ts" 2>/dev/null \
  | sed 's/.*\(os.environ\|os.getenv\|process.env\)\["\(.*\)"\].*/\2/' | sort -u

# Count env vars
grep -rn "os.environ\|os.getenv\|process.env" app/ src/ --include="*.py" --include="*.ts" 2>/dev/null | wc -l

# .env.example contents
cat .env.example .env.template 2>/dev/null
```
</details>

### 5.3 Database management

- [ ] How are migrations run? _______________
- [ ] Is there a seed/bootstrap process?
- [ ] Backup strategy: _______________

<details><summary>🤖 Extraction commands</summary>

```bash
# Migration tool config
cat alembic.ini 2>/dev/null | head -10
cat prisma/schema.prisma 2>/dev/null | head -10

# Migration history
ls alembic/versions/*.py 2>/dev/null
npx prisma migrate status 2>/dev/null

# Seed scripts
grep -rn "seed\|bootstrap\|init_db\|create_tables" . --include="*.py" --include="*.ts" --include="*.sh" 2>/dev/null
```
</details>

---

## Part 6 — Existing Documentation Audit (15 minutes)

### 6.1 Documentation inventory

For each existing doc, rate its status:

| Document | Location | Status |
|----------|----------|--------|
| | | ✅ Current / ⚠️ Stale / ❌ Missing / 🔲 Placeholder |
| | | |
| | | |

### 6.2 Documentation gaps

Based on the inventory, what's missing?

- [ ] Architecture overview
- [ ] API documentation
- [ ] Data model documentation
- [ ] Configuration/environment guide
- [ ] Local development setup
- [ ] Deployment guide
- [ ] Operational runbooks
- [ ] Troubleshooting guide
- [ ] Security documentation
- [ ] Onboarding guide
- [ ] AGENTS.md (agent-ready)

---

## Summary

After completing this checklist, you should be able to answer:

1. **What is this system?** (one paragraph)
2. **What tech stack does it use?** (language, framework, data stores, integrations)
3. **How many processes run?** (web, worker, cron, etc.)
4. **What does the code structure look like?** (modules and their purposes)
5. **How is it deployed?** (where, how, config)
6. **What documentation exists?** (and what's missing)

These answers form the foundation for all subsequent documentation work.
