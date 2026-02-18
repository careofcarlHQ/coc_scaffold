# 05 — Cleanup and Archival

> A spike isn't done when the exploration stops — it's done when the findings are archived and the mess is cleaned up.

---

## What to Archive

### Always archive

| Artifact | Why | Where |
|----------|-----|-------|
| Spike charter | Reference for "what were we trying to learn?" | `spikes/{name}/charter.md` |
| Exploration log | Detailed record of what was tried | `spikes/{name}/exploration-log.md` |
| Findings document | Summary of what was learned | `spikes/{name}/findings.md` |
| Decision record | What was decided and why | `spikes/{name}/decision.md` |

### Archive if useful

| Artifact | When to keep | Where |
|----------|-------------|-------|
| Prototype code | If it demonstrates a pattern that's hard to re-derive | `spikes/{name}/prototype/` |
| Configuration examples | If the real implementation will need similar config | `spikes/{name}/prototype/` |
| Performance benchmarks | If the decision was performance-based | Include in findings document |
| Screenshots/recordings | If visual evidence supports the findings | `spikes/{name}/evidence/` |

### Don't archive

- Temporary credentials or secrets (delete immediately)
- Downloaded large files or datasets
- `node_modules`, `.venv`, or other dependency directories
- Compiled output or build artifacts

---

## Cleanup Checklist

### Secrets and credentials
- [ ] Temporary API keys revoked
- [ ] Test accounts disabled
- [ ] No credentials in committed code
- [ ] `.env` files with secrets removed

### Infrastructure
- [ ] Test databases dropped
- [ ] Temporary services stopped
- [ ] Cloud resources deleted (test instances, queues, etc.)
- [ ] DNS/config changes reverted

### Local environment
- [ ] Prototype directory cleaned or moved to archive
- [ ] No spike dependencies in the main project
- [ ] No spike imports in the main codebase
- [ ] Working directory clean

### Documentation
- [ ] All findings documented
- [ ] Decision record written
- [ ] Exploration log complete
- [ ] Archive location is findable (linked from somewhere)

---

## Archive Structure

```
spikes/
├── {spike-name}/
│   ├── charter.md              # What we were exploring
│   ├── exploration-log.md      # What we tried
│   ├── findings.md             # What we learned
│   ├── decision.md             # What we decided
│   └── prototype/              # Code artifacts (if kept)
│       ├── README.md           # How to run the prototype
│       └── ...
├── {another-spike}/
│   └── ...
└── README.md                   # Index of all spikes
```

### Spikes index

Maintain an index file so spikes are discoverable:

```markdown
# Spikes Index

| Spike | Date | Question | Decision | Link |
|-------|------|----------|----------|------|
| redis-caching | 2024-01-15 | Can we use Redis for response caching? | Go | [→](redis-caching/) |
| graphql-api | 2024-02-01 | Should we switch from REST to GraphQL? | No-go | [→](graphql-api/) |
| celery-jobs | 2024-02-20 | Celery vs Dramatiq for background jobs? | Celery (go) | [→](celery-jobs/) |
```

---

## Transitioning to Implementation

When the decision is "go," the spike findings become input for the next scaffold:

### → Feature Addition scaffold
Use when the spike validates a new feature or capability.
- The spike findings become the basis for the feature spec
- The effort estimate becomes the phased plan

### → Migration scaffold
Use when the spike validates a technology change (new database, framework version, etc.).
- The spike findings become the target state definition
- The prototype reveals the gap map

### → Greenfield scaffold
Use when the spike validates a completely new project or subsystem.
- The spike findings become the project spec
- The prototype informs the architecture

### The handoff

When transitioning, include in the new project's documentation:

```markdown
## Background
This work was validated by spike {name}, completed {date}.
See spikes/{name}/findings.md for detailed analysis.
Decision: spikes/{name}/decision.md
```

This creates a traceable chain from "should we?" (spike) to "how do we?" (implementation).
