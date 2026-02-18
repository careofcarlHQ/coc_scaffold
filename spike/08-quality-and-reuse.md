# 08 — Quality and Reuse

> Making spike output reusable and the spike process itself better over time.

---

## Spike Quality Criteria

A spike is high-quality when:

### The question was answered
- [ ] The spike question has a clear answer (yes / no / it depends)
- [ ] The answer is supported by evidence (measurements, observations, code)
- [ ] The answer addresses the success/failure criteria from the charter

### The findings are reusable
- [ ] Someone who wasn't part of the spike can understand the findings
- [ ] Trade-offs are clearly documented
- [ ] The effort estimate (if "go") is broken down and has confidence levels
- [ ] Remaining unknowns are honestly stated

### The process was efficient
- [ ] Time box was respected (finished on time or stopped early with reason)
- [ ] Scope didn't creep (stayed on the charter question)
- [ ] Exploration log was maintained throughout
- [ ] No spike code leaked into the main project

### The decision is actionable
- [ ] Clear go/no-go/pivot decision
- [ ] Next steps are defined
- [ ] Conditions for revisiting the decision are documented
- [ ] Archive location is findable

---

## Reusing Spike Knowledge

### Within the current project

When a spike leads to "go," the transition to implementation should reference the spike:

```markdown
## Background
Validated by spike: spikes/{name}/
Question: {question}
Decision: Go (see spikes/{name}/decision.md)
Key finding: {the most important thing learned}
Effort estimate: {from the findings} ({confidence level})
```

### For future spikes

Common patterns that make future spikes more efficient:

1. **Reuse the charter template** — don't start from scratch every time
2. **Reference past spikes** — "We explored this before, see spikes/{name}/"
3. **Build a technology radar** — track which technologies you've evaluated and the outcomes

### Technology Radar

Maintain a simple technology radar:

| Technology | Status | Last evaluated | Spike link | Notes |
|-----------|--------|---------------|-----------|-------|
| Redis | Adopted | 2024-01 | spikes/redis-caching/ | Using for response caching |
| GraphQL | Rejected | 2024-02 | spikes/graphql-api/ | Too complex for our consumer base |
| Celery | Evaluating | 2024-03 | spikes/celery-jobs/ | Promising, needs deeper spike |
| HTMX | Not assessed | — | — | Potential future spike |

---

## Spike Metrics

Track these over time to improve your spiking process:

| Metric | What it tells you |
|--------|------------------|
| Spikes per month | How often you're reducing uncertainty before committing |
| Time box hit rate | % of spikes completed within time box |
| Go/no-go ratio | Balance of exploration (too many "go"s may mean you're not being critical enough) |
| Spike → implementation lag | Time from "go" to starting implementation |
| "Wish we'd spiked" incidents | Times you regretted NOT spiking before building |

### Healthy patterns

- **2-4 spikes per quarter** for an active project — shows you're exploring before committing
- **30-50% no-go rate** — means you're discovering things that wouldn't have worked
- **Time box respected 80%+ of the time** — discipline is working
- **Spike → implementation within 2 weeks** — momentum is maintained

### Warning signs

| Signal | What it means | Fix |
|--------|--------------|-----|
| Never spiking | Jumping into implementation without validation | Schedule spikes for uncertain work |
| Always "go" | Not being critical, or only spiking safe things | Spike harder problems, evaluate honestly |
| Never finishing on time | Scope too broad, or not focused enough | Narrower questions, stricter scope |
| Spike code in production | Discipline breakdown | Enforce the "no deploy" rule |
| Spikes never referenced | Findings not connected to implementation | Improve the handoff process |

---

## Continuous Improvement

After every 5 spikes, do a brief retrospective:

1. **Are our spike questions getting sharper?** — They should narrow over time as you learn what makes a good charter
2. **Are we exploring the right things?** — Are spikes answering real uncertainties or just validating comfortable decisions?
3. **Is the findings format useful?** — Can you actually reference past spikes when making decisions?
4. **Is the time box working?** — Too long (wasting time)? Too short (incomplete answers)?
5. **Are we following through?** — Do "go" decisions lead to implementation? Are "no-go" decisions respected?
