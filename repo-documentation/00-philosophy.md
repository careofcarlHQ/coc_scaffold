# 00 — Philosophy: Documenting Existing Code

## The core insight

Most codebases aren't undocumented — they're **unevenly** documented. README is outdated, some modules have great docstrings while others have none, operational knowledge lives in Slack, and the deployment process is in someone's head.

The goal isn't to write documentation from scratch. It's to **systematically discover what exists, fill the critical gaps, and create a navigable structure** that both humans and agents can use.

## Principles

### 1. Code is the source of truth, docs are the map

Documentation for an existing repo describes **what is**, not what was planned. When docs and code disagree, the code wins. This means:

- Read the code before writing about it
- Verify claims against actual behavior
- Date-stamp docs so readers know when they were last confirmed
- Mark anything unverified with `[UNVERIFIED]`

### 2. Document for the next person (human or agent)

The primary reader of your documentation is someone — or something — encountering this codebase for the first time. Every document should answer one of these questions:

- **What is this?** → Architecture overview, service map
- **How does it work?** → Data flow, state machines, API contracts
- **How do I run it?** → Bootstrap guide, configuration
- **How do I operate it?** → Runbooks, monitoring, troubleshooting
- **How do I change it?** → Coding conventions, test strategy, deployment

### 3. Progressive disclosure, not information dumps

Start with a 30-second orientation (AGENTS.md / README), then link to deeper documents. Nobody reads a 500-line architecture doc — they scan for the section they need.

Structure your docs as a tree:

```
AGENTS.md (entry point, <150 lines)
  └── docs/README.md (index of all docs)
       ├── architecture-overview.md (system shape)
       ├── api-surface.md (all endpoints)
       ├── data-model.md (all tables/schemas)
       └── ... (focused documents)
```

### 4. Breadth first, depth second

It's more valuable to have a one-paragraph description of every module than a 20-page deep-dive on one module. Cover the entire surface area at a shallow level first, then deepen the areas that matter most.

Priority order:
1. What does the system do? (1 paragraph)
2. What are the main components? (1 paragraph each)
3. How do I run it locally? (step-by-step)
4. What are the API endpoints? (list with descriptions)
5. What does the data model look like? (table list + relationships)
6. How is it deployed? (environment + process)
7. Deep dives on complex subsystems (only where needed)

### 5. Evidence over assumption

Every architectural claim should be traceable to code:

```markdown
# ❌ Bad
The system uses event sourcing for order processing.

# ✅ Good
Events are dispatched through `app/dispatch/worker.py` which polls
the `dispatch_queue` table (see `app/db/models/dispatch.py`).
Events are batched per destination and forwarded via HTTP.
This is a queue-based dispatch pattern, not event sourcing.
```

### 6. Mark what you don't know

Honest gaps are more useful than confident guesses. Use explicit markers:

```markdown
- `[UNVERIFIED]` — Believed to be true but not confirmed against code
- `[OUTDATED]` — Was true at some point but may have changed
- `[TODO]` — Known gap, needs investigation
- `[ASK]` — Requires input from someone with context
```

### 7. Docs live in the repo, not beside it

Documentation in Confluence, Google Docs, or Notion is invisible to agents and drifts from the code. Put docs in a `docs/` directory in the repo. If external docs exist, create a link inventory pointing to them.

### 8. Small, focused documents beat monoliths

Each document should cover **one topic** and be **readable in under 5 minutes**. If a document is getting long, split it.

| ❌ One big doc | ✅ Focused docs |
|---|---|
| `architecture.md` (800 lines) | `architecture-overview.md` (100 lines) |
| | `data-model.md` (150 lines) |
| | `api-surface.md` (200 lines) |
| | `deployment.md` (80 lines) |

### 9. Date everything

Every document should have a `Last verified: YYYY-MM-DD` header. This lets readers assess freshness and prioritize re-verification.

### 10. Documentation is a maintenance task, not a project

Don't try to document everything in a single sprint. Document what you discover as you work. Set up a regular cadence (weekly or per-PR) to keep docs current. Small continuous updates beat big occasional rewrites.

---

## Lessons from documenting coc_capi

### What we found

1. **README existed but was incomplete** — it described the high-level purpose but not the actual architecture, data flow, or deployment model.

2. **docs/ directory existed but was sprawling** — 20+ subdirectories with inconsistent depth. Some areas well-documented, others empty placeholders.

3. **Operational knowledge was scattered** — deployment was in `render.yaml` + `deploy/`, operations were partially in `docs/operations/` and partially tribal knowledge.

4. **Agent orientation was minimal** — `agents.md` was 3 lines, not enough for an agent to understand the repo.

5. **The code was the best documentation** — module structure, naming conventions, and type hints told a clearer story than most docs.

### What worked

1. **Starting with `tree` and `pyproject.toml`** — the directory structure and dependencies told us 80% of the architecture in 5 minutes.

2. **Documenting the module map first** — listing every package and its one-line purpose created a foundation for deeper docs.

3. **Writing the AGENTS.md last** — after documenting everything, the agent entry point practically wrote itself.

4. **Using `[UNVERIFIED]` liberally** — marking uncertain claims kept the docs honest and created a natural TODO list.
