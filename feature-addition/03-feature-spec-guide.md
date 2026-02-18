# 03 — Feature Spec Guide

## Purpose

A feature spec is a scoped contract for what you're adding. It's smaller than a PRD (which covers an entire project) and more specific than an architecture doc. It gives agents everything they need to implement the feature without asking questions.

## When to write a feature spec

Always. Even for small features. The discipline of writing the spec catches ambiguity before it becomes bugs.

For small features (2–4 hours), the spec might be 20 lines. For large features (3+ days), it might be 2 pages. Scale the spec to the feature, but never skip it.

## Structure

### 1. Feature Summary

One paragraph. What is being added and why.

```markdown
## Summary

Add a `/api/v1/exports/{id}/download` endpoint that returns a signed URL 
for downloading completed export files. This enables the admin UI to provide 
one-click download links instead of requiring manual S3 bucket access.
```

### 2. Motivation

Why this feature, why now. Link to the user need or technical requirement.

```markdown
## Motivation

Export files are currently only accessible via direct S3 console access. 
Admin users need a way to download exports from the UI. This was identified 
as a P1 gap in the Phase 2 review.
```

### 3. Scope

What's IN scope and what's NOT. The "not in scope" list is as important as the "in scope" list.

```markdown
## Scope

### In scope
- New download endpoint for completed exports
- Signed URL generation with 1-hour expiry
- Access control (admin role required)

### Not in scope
- Bulk download (future feature)
- Export file format changes
- Public/unauthenticated download links
```

### 4. Database Changes

Exact schema changes. If none, state "No database changes."

```markdown
## Database Changes

No new tables. Add column to existing `exports` table:

| Column | Type | Nullable | Default | Purpose |
|--------|------|----------|---------|---------|
| storage_key | VARCHAR(500) | YES | NULL | S3 object key for completed export |

Migration: Add column (nullable, no backfill needed for existing rows).
```

### 5. API Changes

For each new or modified endpoint, specify completely:

```markdown
## API Changes

### New: GET /api/v1/exports/{id}/download

**Authentication**: Required (admin role)

**Path parameters**:
| Param | Type | Description |
|-------|------|-------------|
| id | UUID | Export ID |

**Response 200**:
```json
{
  "download_url": "https://s3.../signed-url",
  "expires_at": "2026-02-18T15:00:00Z",
  "filename": "export-2026-02-18.csv"
}
```

**Error responses**:
| Status | Condition |
|--------|-----------|
| 404 | Export not found |
| 409 | Export not in "completed" state |
| 403 | User lacks admin role |
```

### 6. Business Logic

Rules, validations, and behavior. Be specific about edge cases.

```markdown
## Business Logic

1. Only exports in "completed" state can be downloaded
2. Signed URLs expire after 1 hour
3. Each download request generates a fresh signed URL
4. Download attempts are logged (export_id, user_id, timestamp)
5. If storage_key is NULL for a completed export, return 500 with error detail
```

### 7. Compatibility

What existing behavior must be preserved.

```markdown
## Compatibility

- Existing export creation endpoint unchanged
- Existing export list endpoint unchanged
- No changes to export state machine
- Export model gains one nullable column (backward compatible)
```

### 8. Test Requirements

Concrete test cases, not vague "should be tested."

```markdown
## Test Requirements

### Unit tests
- Signed URL generation with correct expiry
- Rejection of non-completed exports (409)
- Rejection of non-existent exports (404)
- Logging of download attempts

### Integration tests
- Full flow: create export → complete → download
- Auth: unauthenticated request returns 401
- Auth: non-admin request returns 403

### Edge cases
- Export completed but storage_key is NULL → 500 with detail
- Expired export (if applicable)
```

### 9. Acceptance Criteria

Objective, testable conditions that define "done."

```markdown
## Acceptance Criteria

- [ ] Migration runs up and down without errors
- [ ] GET /api/v1/exports/{id}/download returns signed URL for completed export
- [ ] Non-completed exports return 409
- [ ] Missing exports return 404
- [ ] Unauthenticated requests return 401
- [ ] Non-admin requests return 403
- [ ] All existing tests continue to pass
- [ ] Download attempt is logged
```

---

## Common mistakes in feature specs

| Mistake | Problem | Fix |
|---------|---------|-----|
| Ambiguous error handling | Agent guesses wrong | Specify exact status codes and conditions |
| Missing edge cases | Bugs in production | List every state combination |
| "Should work like X" | Agent doesn't know what X does | Spell out the behavior explicitly |
| No scope boundaries | Feature grows during implementation | Write explicit "not in scope" list |
| Spec references external docs | Agent can't find them | Make spec self-contained for its scope |
| No test requirements | Tests skipped or superficial | List concrete test cases per layer |

## Spec size guidelines

| Feature size | Spec length | Time to write |
|-------------|-------------|---------------|
| Small (hours) | 20–40 lines | 15 minutes |
| Medium (1–2 days) | 50–100 lines | 30–60 minutes |
| Large (3–5 days) | 100–200 lines | 1–2 hours |
| Too large | 200+ lines | Decompose into smaller features |
