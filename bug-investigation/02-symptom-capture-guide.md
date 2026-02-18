# 02 — Symptom Capture Guide

## Purpose

Accurate symptom capture is the foundation of effective debugging. A well-captured symptom saves hours of investigation. A vague symptom sends you in circles.

## The five questions

Every bug report must answer:

### 1. What is happening?
Describe the observed behavior exactly. Include error messages, status codes, and visible effects.

```markdown
# ❌ Vague
"The export feature is broken"

# ✅ Specific
"GET /api/v1/exports/123/download returns 500 with traceback:
TypeError: 'NoneType' object has no attribute 'key' at services/export.py:45"
```

### 2. What should be happening?
Describe the expected behavior. This defines the gap you're investigating.

```markdown
# ❌ Vague
"It should work"

# ✅ Specific
"Should return 200 with a JSON body containing download_url and expires_at"
```

### 3. When did it start?
Narrow the time window. If you know when it started, you know what changed.

```markdown
# ✅ Good answers
- "After the deploy on Feb 15"
- "Intermittent since last week, first noticed Feb 12"
- "Always been this way (discovered during testing)"
- "Unknown — first report today"
```

### 4. What changed recently?
List recent changes that could be related. Check:
- Recent deployments
- Recent database migrations
- Configuration changes
- Dependency upgrades
- Data changes (new records, imports, etc.)

### 5. Who/what is affected?
Understand the scope of impact:
- All users or specific users?
- All data or specific records?
- All environments or only production?
- Always or intermittently?

## Severity classification

| Severity | Criteria | Response time |
|----------|----------|---------------|
| **Critical** | Data loss, security breach, complete system down | Immediate — use [incident-response](../incident-response/) scaffold |
| **High** | Major feature broken for all users, no workaround | Same day |
| **Medium** | Feature broken for some users, or workaround exists | Within 2 days |
| **Low** | Cosmetic, minor UX issue, edge case | Next planning cycle |

## Capturing error context

### From logs
```markdown
## Error from logs
- **Timestamp**: 2026-02-18T14:23:45Z
- **Request**: GET /api/v1/exports/123/download
- **User**: admin@example.com
- **Error**: TypeError: 'NoneType' object has no attribute 'key'
- **Traceback**:
  File "app/api/routes/exports.py", line 34
  File "app/services/export.py", line 45
  File "app/services/storage.py", line 12
```

### From user reports
```markdown
## User report
- **Reporter**: [name or role]
- **Steps performed**: [what they did]
- **Expected result**: [what they expected]
- **Actual result**: [what happened — include screenshots if available]
- **Frequency**: [every time / sometimes / once]
- **Browser/client**: [if relevant]
```

### From monitoring
```markdown
## Monitoring alert
- **Alert**: Error rate > 5% on /api/v1/exports/*
- **Started**: 2026-02-18T14:00:00Z
- **Current rate**: 12% of requests failing
- **Affected endpoints**: GET /api/v1/exports/{id}/download
- **Error distribution**: 100% TypeError
```

## Context checklist

Before starting investigation, confirm you have:

- [ ] Exact error message or unexpected behavior description
- [ ] Expected behavior description
- [ ] Time of first occurrence (or "unknown")
- [ ] Environment details (production, staging, local?)
- [ ] Recent changes (deploys, migrations, config)
- [ ] Scope (all users? specific data? intermittent?)
- [ ] Severity classification
- [ ] Any relevant logs, tracebacks, or screenshots
