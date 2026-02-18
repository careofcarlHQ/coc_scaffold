# 02 — Spike Charter Guide

> The charter defines what you're exploring, why, and how you'll know when you're done. A spike without a charter is just random exploration.

---

## The Spike Question

The most important thing in the charter is the **question**. A good spike question is:

### Specific
- Bad: "Explore caching"
- Good: "Can we add Redis caching to /api/products to reduce response time below 100ms?"

### Answerable
- Bad: "What's the best database?"
- Good: "Can we migrate from SQLite to PostgreSQL without changing the ORM layer?"

### Scoped
- Bad: "Redesign the API"
- Good: "Can we add pagination to list endpoints using cursor-based pagination without breaking existing consumers?"

### Measurable
- Bad: "Is this library good?"
- Good: "Can this library handle 1000 concurrent WebSocket connections on our Render instance?"

---

## Charter Template

A spike charter should include these sections:

### 1. Question
The specific question this spike answers.

### 2. Context
Why this question matters now. What decision depends on the answer.

### 3. Success criteria
What does a positive answer look like? Be specific:
- "The prototype achieves <100ms response time with 1000 items"
- "The library integrates with our auth system without custom patches"
- "Migration is possible with zero downtime using this approach"

### 4. Failure criteria
What would convince you the approach won't work? Be specific:
- "Response time exceeds 500ms even with optimization"
- "Library requires Python 3.12 and we're locked to 3.11"
- "Integration requires exposing internal APIs to the public"

### 5. Scope boundaries
What you're NOT exploring in this spike. Be explicit about:
- Which alternatives you're not evaluating
- Which integration points you're not testing
- Which edge cases you're explicitly ignoring

### 6. Time box
- Start: {date/time}
- Deadline: {date/time}
- Total hours: {N}

### 7. Resources needed
- Documentation to read
- Accounts or credentials needed
- Test data or environment
- Libraries to install (in isolation)

---

## Multiple Approaches

If the spike is about choosing between approaches, the charter should define:

| Approach | Description | What to test |
|----------|------------|-------------|
| A — {name} | {brief description} | {what to build/test} |
| B — {name} | {brief description} | {what to build/test} |
| C — {name} | {brief description} | {what to build/test} |

**Evaluation criteria** (weighted):

| Criterion | Weight | How to evaluate |
|-----------|--------|----------------|
| Performance | {1-5} | {measurement method} |
| Complexity | {1-5} | {assessment method} |
| Maintainability | {1-5} | {assessment method} |
| Community/support | {1-5} | {assessment method} |
| Integration effort | {1-5} | {assessment method} |

---

## Charter review checklist

Before starting the exploration:

- [ ] Question is specific and answerable
- [ ] Success criteria are measurable
- [ ] Failure criteria are defined
- [ ] Scope boundaries are clear
- [ ] Time box is set and reasonable
- [ ] Resources are available (accounts, docs, etc.)
- [ ] If comparing approaches: evaluation criteria defined

---

## Example charters

### Quick check (2–4 hours)
> **Question**: Can we use `httpx` as a drop-in replacement for `requests` in our service layer to get async support?
>
> **Success**: All current API calls can be made with httpx. Async variant works. No breaking changes.
> **Failure**: httpx API is incompatible, or our Render setup can't handle async.
> **Time box**: 3 hours
> **Scope**: Only the service layer. Not testing async endpoints yet.

### Focused exploration (1 day)
> **Question**: Can we implement rate limiting using Redis without adding significant latency to every request?
>
> **Success**: Rate limiting works, adds <5ms per request, and our Render Redis add-on can handle the volume.
> **Failure**: Latency >20ms per request, or Redis add-on is too expensive for our tier.
> **Time box**: 1 day
> **Scope**: Rate limiting only. Not implementing full caching.

### Deep investigation (3 days)
> **Question**: Should we use Celery, Dramatiq, or our current in-process approach for background job processing?
>
> **Comparing**: Celery vs. Dramatiq vs. status quo
> **Success criteria**: One approach clearly wins on reliability, monitorability, and operational simplicity.
> **Time box**: 3 days (1 day per approach)
