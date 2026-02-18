# 03 — Documentation Writing Guide

## Why good documentation matters for existing repos

Unlike spec-writing (which defines intent before code), documenting existing code is **descriptive, not prescriptive**. You're answering "what does this actually do?" not "what should this do?"

This is harder than it sounds. The temptation is to describe what the code *should* do based on names and comments. Resist this. Read the actual logic.

## Writing rules

### 1. Describe behavior, not intent

```markdown
# ❌ Bad (describes intent)
The dispatch worker processes events from the queue and sends them to destinations.

# ✅ Good (describes behavior)
The dispatch worker (`app/dispatch/worker.py`) polls the `dispatch_queue` table
every 5 seconds (configurable via `WORKER_POLL_INTERVAL`). It claims unclaimed rows
in batches, groups events by destination, and sends HTTP POST requests to each
destination's API endpoint. Failed sends are retried up to 3 times with exponential
backoff. After 3 failures, events move to `dead_letter` status.
```

### 2. Always cite source locations

Every factual claim should point to where in the code it comes from:

```markdown
# ❌ Bad
Authentication uses admin tokens.

# ✅ Good
Authentication uses a static admin token passed via the `X-Admin-Token` header.
The token is validated in `app/api/auth.py` against the `ADMIN_TOKEN` environment
variable. MFA (TOTP) is additionally required when `MFA_REQUIRED=true` (see
`app/core/security.py`).
```

### 3. Use consistent document structure

Every documentation file should follow this skeleton:

```markdown
# {Document Title}

> Last verified: YYYY-MM-DD
> Source: {primary source file or directory}

## Overview
One paragraph summary.

## Details
Main content, organized by topic.

## Related Documents
- [Link to related doc](path)
```

### 4. Tables for inventories, prose for explanations

Use tables when listing things (endpoints, tables, env vars). Use prose when explaining how things work together.

```markdown
# ❌ Bad — prose for a list
The system has an ingest endpoint at POST /ingest/event, a health endpoint
at GET /healthz, an admin stats endpoint at GET /admin/stats, ...

# ✅ Good — table for a list
| Method | Path | Purpose | Auth |
|--------|------|---------|------|
| POST | /ingest/event | Receive purchase events | API key |
| GET | /healthz | Health check | None |
| GET | /admin/stats | Event statistics | Admin token |
```

```markdown
# ❌ Bad — table for an explanation
| Step | Description |
|------|-------------|
| 1 | Event arrives at /ingest/event |
| 2 | Event is validated against schema |
| 3 | Event is written to events table |
| 4 | ... |

# ✅ Good — prose for an explanation
When an event arrives at `/ingest/event`, it's validated against the
`EventPayload` schema (`app/schemas/event.py`). Valid events are inserted
into the `events` table with status `pending`. The dispatch worker picks
them up on its next poll cycle and routes them based on the destination
configuration in `destinations.rollout_status`.
```

### 5. Show the actual types

When documenting data models or API shapes, show real types from the code:

```markdown
# ❌ Bad
The event has various fields including an ID and timestamp.

# ✅ Good
### `events` table
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | uuid | PK, default gen_random_uuid() | |
| order_id | text | not null | Askås order ID |
| event_type | text | not null | `purchase` / `refund` |
| status | text | not null, default `pending` | `pending` / `dispatched` / `failed` / `dead_letter` |
| payload | jsonb | not null | Raw event data |
| created_at | timestamptz | not null, default now() | |
| dispatched_at | timestamptz | nullable | Set when successfully sent |
```

### 6. Document the happy path first, then edge cases

Start with what happens when everything works. Then document error handling, retries, and failure modes.

```markdown
## Event Dispatch Flow

### Happy path
1. Worker polls `dispatch_queue` for unclaimed events
2. Claims a batch (sets `claimed_by` to worker ID)
3. Groups events by destination
4. Sends HTTP POST to destination API
5. Marks events as `dispatched`, sets `dispatched_at`

### Failure handling
- HTTP 4xx → marked as `failed`, no retry (permanent error)
- HTTP 5xx → retry up to 3 times with exponential backoff
- Timeout → treated as 5xx, retried
- After max retries → moved to `dead_letter` status
```

### 7. Use diagrams sparingly but effectively

Text-based ASCII diagrams work well for simple flows. Don't over-engineer diagrams for things that prose explains better.

```markdown
# Good: simple flow diagram
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌─────────────┐
│  Askås   │────▶│  Ingest  │────▶│  Queue   │────▶│ Destination │
│  Webhook │     │  API     │     │  (PG)    │     │   API       │
└──────────┘     └──────────┘     └──────────┘     └─────────────┘
                      │                                    │
                      ▼                                    ▼
                 ┌──────────┐                        ┌──────────┐
                 │  Events  │                        │  Audit   │
                 │  Table   │                        │  Log     │
                 └──────────┘                        └──────────┘
```

### 8. Mark verification status explicitly

```markdown
## Redis Usage

> Last verified: 2026-02-15

Redis is used for:
- Worker coordination and locking (verified in `app/core/redis.py`)
- Rate limiting [UNVERIFIED — saw rate limit code but unclear if active]
- Session storage [TODO — need to check if sessions use Redis or DB]
```

## Document types and when to use each

| Document type | When to write it | Key question it answers |
|---------------|-----------------|----------------------|
| Architecture overview | Phase 2 — after reconnaissance | "What is this system and how do the parts fit together?" |
| Service map | Phase 2 — for multi-process systems | "What does each module/service do?" |
| API surface | Phase 3 — after understanding architecture | "What endpoints/commands exist and what do they accept?" |
| Data model | Phase 3 — after understanding architecture | "What data is stored and how is it structured?" |
| Configuration guide | Phase 3 — from .env and config files | "What settings exist and what do they control?" |
| Dependency inventory | Phase 3 — from package manifest | "What external libraries and services does this use?" |
| Onboarding guide | Phase 4 — after you can run it | "How do I go from clone to running locally?" |
| Deployment guide | Phase 4 — from infra config | "How does this get to production?" |
| Operational runbook | Phase 4 — from operational experience | "How do I handle common operational tasks?" |
| Gap analysis | Phase 5 — after all other docs | "What's still missing or unverified?" |

## Quality checklist

Before considering a document complete:

- [ ] `Last verified` date is set
- [ ] Source file/directory is cited
- [ ] Every factual claim traces to code
- [ ] No `[UNVERIFIED]` markers remain (or they're acknowledged in gap analysis)
- [ ] Tables used for lists, prose for explanations
- [ ] Under 300 lines (split if longer)
- [ ] Cross-references to related docs are correct
- [ ] Someone unfamiliar with the repo could follow it
