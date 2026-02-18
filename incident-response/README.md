# Incident Response Scaffold

> *"Production is broken right now — what do I do?"*

The **incident-response** scaffold is a structured methodology for handling production incidents under pressure. It is the **emergency** companion — designed to be useful *during* the crisis, not just before or after.

---

## When to use this scaffold

- Something is broken in production RIGHT NOW
- Users are impacted and you need to act fast
- You need a structured approach to diagnosis under pressure
- You want to prevent the same incident from recurring
- You need to write a post-mortem and extract action items

## How to use this scaffold

1. Read [00-philosophy.md](00-philosophy.md) before touching production
2. Follow [01-process-overview.md](01-process-overview.md) for phase order
3. Triage with [02-triage-and-severity.md](02-triage-and-severity.md)
4. Mitigate quickly using [03-mitigation-playbook.md](03-mitigation-playbook.md)
5. Diagnose and fix with [04-diagnosis-and-fix.md](04-diagnosis-and-fix.md)
6. Write the post-mortem using [05-post-mortem-guide.md](05-post-mortem-guide.md)
7. Set agent behavior via [06-agents-md-for-incidents.md](06-agents-md-for-incidents.md)
8. Execute with [07-agent-prompts.md](07-agent-prompts.md)
9. Drive follow-up in [08-prevention-and-improvement.md](08-prevention-and-improvement.md)

## Core lifecycle

| Phase | Question answered | Key output |
|-------|------------------|-----------|
| **Alert & Capture** | What's happening? | Incident report with symptoms |
| **Triage** | How bad is it? | Severity classification + scope |
| **Mitigate** | How do we stop the bleeding? | Immediate relief (not a fix) |
| **Diagnose** | What caused it? | Root cause identification |
| **Fix** | How do we actually fix it? | Verified fix deployed |
| **Post-Mortem** | What do we learn? | Timeline, root cause, action items |
| **Prevention** | How do we prevent recurrence? | Monitoring, tests, process changes |

---

## Document index

| File | Purpose |
|------|---------|
| [00-philosophy.md](00-philosophy.md) | Core principles for incident response |
| [01-process-overview.md](01-process-overview.md) | Full lifecycle walkthrough |
| [02-triage-and-severity.md](02-triage-and-severity.md) | Classifying severity and scope |
| [03-mitigation-playbook.md](03-mitigation-playbook.md) | Common mitigation patterns |
| [04-diagnosis-and-fix.md](04-diagnosis-and-fix.md) | Finding and fixing root cause under pressure |
| [05-post-mortem-guide.md](05-post-mortem-guide.md) | Writing useful post-mortems |
| [06-agents-md-for-incidents.md](06-agents-md-for-incidents.md) | How to orient an agent during an incident |
| [07-agent-prompts.md](07-agent-prompts.md) | Copy-paste prompts for each phase |
| [08-prevention-and-improvement.md](08-prevention-and-improvement.md) | Turning incidents into improvements |

## Templates

| Template | Purpose |
|----------|---------|
| [AGENTS.md.template](templates/AGENTS.md.template) | Agent orientation during an incident |
| [incident-report.md.template](templates/incident-report.md.template) | Live incident tracking document |
| [triage-checklist.md.template](templates/triage-checklist.md.template) | Quick severity and scope assessment |
| [mitigation-log.md.template](templates/mitigation-log.md.template) | Tracking mitigation attempts |
| [post-mortem.md.template](templates/post-mortem.md.template) | Structured post-mortem document |
| [prevention-backlog.md.template](templates/prevention-backlog.md.template) | Action items from incidents |
