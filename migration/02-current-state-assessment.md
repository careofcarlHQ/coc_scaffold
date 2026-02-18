# 02 — Current State Assessment

## Purpose

Before migrating, capture exactly what you have. This snapshot is your baseline — it defines the starting point, provides rollback reference, and ensures nothing is forgotten during transition.

## Assessment checklist

### Language & Runtime

- [ ] Language version: {e.g., Python 3.11.7}
- [ ] Runtime environment: {e.g., CPython, PyPy}
- [ ] Package manager: {e.g., Poetry 1.7, pip 24.0}
- [ ] Virtual environment: {e.g., venv, conda}

### Framework & Dependencies

- [ ] Framework: {e.g., FastAPI 0.109.0}
- [ ] ORM / data layer: {e.g., SQLAlchemy 2.0.25}
- [ ] Full dependency list exported: `pip freeze > requirements.current.txt` or `poetry export`
- [ ] Dependency count: {N direct, M total including transitive}
- [ ] Known deprecation warnings: {list}

### Database

- [ ] Database engine: {e.g., PostgreSQL 16.1}
- [ ] Table count: {N}
- [ ] Total data size: {GB}
- [ ] Migration tool: {e.g., Alembic}
- [ ] Migration count: {N migrations}
- [ ] Current migration head: {revision id}
- [ ] Backup strategy: {frequency, retention, location}

### Infrastructure

- [ ] Hosting platform: {e.g., Render, AWS, Heroku}
- [ ] Service type: {web service, worker, cron, static site}
- [ ] Region: {e.g., Oregon (us-west-2)}
- [ ] Plan/tier: {e.g., Standard}
- [ ] Custom domain: {yes/no, domain name}
- [ ] SSL: {auto/manual}
- [ ] CDN: {yes/no}

### Configuration

- [ ] Environment variables documented: {count}
- [ ] Secret management: {env vars, vault, etc.}
- [ ] Feature flags: {list active flags}
- [ ] Configuration files: {list non-env config files}

### External Integrations

| Integration | Type | Version/API | Auth method |
|-------------|------|-------------|-------------|
| {service} | {API / webhook / SDK} | {version} | {API key / OAuth / etc.} |

### Consumers

| Consumer | Protocol | Version constraint | Breaking change tolerance |
|----------|----------|-------------------|--------------------------|
| {client} | {REST API / webhook / etc.} | {v1 / any} | {low / medium / high} |

### Test Baseline

- [ ] Test suite runs: ✅ yes / ❌ no
- [ ] Test count: {N}
- [ ] Test results: {passed} passed, {failed} failed, {skipped} skipped
- [ ] Coverage: {N}%
- [ ] CI/CD pipeline: {tool, status}
- [ ] Build time: {seconds}

### Performance Baseline

| Metric | Value | Source |
|--------|-------|--------|
| Average response time | {ms} | {monitoring tool or manual} |
| P99 response time | {ms} | |
| Requests per second | {N} | |
| Memory usage | {MB} | |
| CPU usage | {%} | |

## How to capture

### Quick commands for snapshot data

```bash
# Python version
python --version

# Installed packages
pip freeze > migration/baseline-requirements.txt

# Database stats (PostgreSQL)
psql -c "SELECT count(*) FROM information_schema.tables WHERE table_schema='public';"
psql -c "SELECT pg_size_pretty(pg_database_size(current_database()));"

# Migration state
alembic current
alembic history --verbose | head -20

# Git state
git log --oneline -10
git describe --tags --always

# Test baseline
pytest --tb=no -q 2>&1 | tail -5
```

### Agent snapshot prompt

```
Analyze this codebase and produce a current-state snapshot covering:
1. Language and runtime versions
2. Framework and key dependency versions
3. Database engine and schema summary
4. Configuration (env vars, files)
5. External integrations
6. Test baseline (run pytest and report results)

Use the current-state-snapshot template and fill in every field.
Report "unknown" for anything that cannot be determined from the codebase alone.
```
