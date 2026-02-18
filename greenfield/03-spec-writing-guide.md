# 03 — Spec Writing Guide

## Why specs matter for agent-first development

Specs are the primary mechanism for transferring intent from human to agent. A well-written spec allows an agent to implement correctly without back-and-forth clarification. A vague spec produces vague code.

## The spec hierarchy

```
PRD (why + what)
  └── Architecture (how, high-level)
       ├── Data Model (schemas + state machine)
       ├── API Contract (endpoints + payloads)
       ├── Job Contract (queue + retries)
       └── Bootstrap (how to run)
  └── Policies (constraints)
       ├── Cost Control
       ├── Guardrails
       └── Escalation
  └── Checklists (build order)
       ├── Phase 1 Checklist
       ├── Phase 2 Checklist
       └── ...
```

## Writing rules

### 1. Be concrete, not aspirational

```markdown
# ❌ Bad
The API should handle errors gracefully.

# ✅ Good
Error responses use this format:
- 400: `{"detail": "Validation error", "errors": [...]}`
- 401: `{"detail": "Invalid or missing admin token"}`
- 409: `{"detail": "State transition not allowed", "current_state": "...", "requested_state": "..."}`
- 422: `{"detail": "Policy violation", "policy": "...", "context": "..."}`
- 500: `{"detail": "Internal server error"}`
```

### 2. Define state machines explicitly

```markdown
# ❌ Bad
Tasks move through various states.

# ✅ Good
States:
1. `intake`
2. `planned`
3. `implementing`
4. `reviewing`

Allowed transitions:
- `intake → planned`
- `planned → implementing`
- `implementing → reviewing`
- `reviewing → implementing` (changes requested)
```

### 3. Show table schemas with types

```markdown
# ❌ Bad
We need a tasks table with relevant fields.

# ✅ Good
### `tasks`
- `id` (uuid, pk)
- `task_id` (text, unique)
- `repo` (text, not null)
- `state` (text, not null, default: 'intake')
- `created_at` (timestamp, not null, default: now())
```

### 4. Specify API endpoints with request/response shapes

```markdown
### POST /api/v1/tasks

Request:
```json
{
  "task_id": "string (required, unique)",
  "repo": "string (required)",
  "branch": "string (required)",
  "change_class": "feature | bugfix | chore | refactor",
  "risk_tier": "low | medium | high",
  "problem_statement": "string (required)"
}
```

Response (201):
```json
{
  "id": "uuid",
  "task_id": "string",
  "state": "intake",
  "created_at": "ISO 8601"
}
```

Errors:
- 409: task_id already exists
- 422: missing required fields
```

### 5. Include acceptance criteria in checklists

Every stage in a checklist needs an acceptance gate — objective pass/fail criteria, not subjective judgment:

```markdown
## Stage 1 — Project Skeleton

- [ ] Create folder structure per architecture spec
- [ ] Add dependency management
- [ ] Add health endpoint (`/healthz`)

Acceptance gate:
- [ ] API process starts locally and `/healthz` returns `{"status":"ok"}`
```

### 6. Write policies as rules, not guidelines

```markdown
# ❌ Bad
Try to keep costs reasonable.

# ✅ Good
## Budget Layers
1. Per-request max tokens: 12,000
2. Per-task max tokens: 60,000
3. Daily global max tokens: 300,000

If any limit is reached, execution stops and requires human decision.
```

## Spec document templates

### Architecture spec structure

1. Stack decision (what and why)
2. Service boundaries (responsibilities per service)
3. Repository structure (folder layout)
4. Runtime model (how processes interact)
5. Security baseline
6. Non-goals (what this architecture does NOT solve)
7. Definition of implementable (when can we start coding?)

### Data model spec structure

1. State machine (states + allowed transitions)
2. Core tables with column types
3. Indexes and constraints
4. Migration strategy

### API contract spec structure

1. Auth model
2. Base URL and versioning
3. Endpoints grouped by resource
4. Request/response schemas per endpoint
5. Error response format
6. Status code semantics

### Policy spec structure

1. Purpose (one line)
2. Rules (numbered, unambiguous)
3. Escalation triggers
4. Enforcement mechanism
5. Breach response

## Common mistakes

| Mistake | Why it fails | Fix |
|---------|-------------|-----|
| Mixing spec and implementation | Agent doesn't know which parts to implement | Separate specs from code |
| Using "should" without criteria | Agent can't verify compliance | Replace with "must" + testable condition |
| Undocumented error cases | Agent produces happy-path-only code | List every error code and response shape |
| Unversioned state machines | Agent adds states without updating transitions | Keep state machine diagram in sync |
| Huge single spec file | Agent loses focus in large context | Split by concern, link from index |
