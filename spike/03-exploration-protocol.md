# 03 — Exploration Protocol

> How to explore systematically without getting lost. The exploration log is your lifeline — if you didn't write it down, it didn't happen.

---

## The Exploration Loop

For each thing you try during the spike:

```
1. State what you're trying and why
2. Do it
3. Record what happened
4. Decide: dig deeper, try alternative, or move on
```

This loop prevents the two most common spike failures: going down rabbit holes (no "why") and forgetting what you learned (no "record").

---

## Exploration Log Format

Keep a running log as you work. Rough is fine — completeness matters more than polish.

```markdown
### {timestamp} — {what you're trying}

**Goal**: {what you hope to learn from this}
**Method**: {what you did — commands, code, configuration}
**Result**: {what happened — success, failure, unexpected}
**Observation**: {what this tells you}
**Next**: {what to try next based on this result}
```

### Example entry

```markdown
### 10:15 — Test Redis connection from Render

**Goal**: Verify we can connect to Render's Redis add-on from our web service
**Method**: Added `redis` package, wrote a simple set/get test script
**Result**: Connection works. Latency ~2ms for set, ~1ms for get.
**Observation**: Much faster than expected. The internal network must route directly.
**Next**: Test with larger payloads (1KB, 10KB, 100KB) to see how latency scales.
```

---

## Research Phase

Before building anything, spend time reading:

### Documentation review
- [ ] Official docs for the technology
- [ ] Getting started / quickstart guide
- [ ] API reference (skim the scope)
- [ ] Known limitations or caveats
- [ ] Changelog (for recent breaking changes)

### Community intelligence
- [ ] GitHub issues — common problems?
- [ ] Stack Overflow — what do people struggle with?
- [ ] Release cadence — is it actively maintained?
- [ ] License — compatible with your project?

### Project fit
- [ ] Python version compatibility?
- [ ] Dependency conflicts with current stack?
- [ ] Deployment compatibility (Render, Docker, etc.)?
- [ ] Match with current architecture patterns?

---

## Prototype Rules

### Do
- Build in an isolated directory (`temp/spike-{name}/`)
- Use hardcoded values for configuration
- Copy-paste from examples and tutorials
- Focus on the core question — skip everything else
- Try the simplest possible approach first
- Time-box each experiment (15-30 min before reassessing)

### Don't
- Install packages in the main project
- Modify existing source code
- Write tests or handle errors
- Optimize for performance (unless performance IS the question)
- Build a complete solution — just enough to answer the question
- Exceed the time box without a conscious decision

---

## Dealing with Getting Stuck

If you've been stuck for 30+ minutes:

1. **Write down what you're stuck on** — formulating the problem often reveals the path
2. **Check whether you're answering the right question** — are you still on the spike charter, or have you drifted?
3. **Try a completely different approach** — if the library approach isn't working, try the manual approach (or vice versa)
4. **Accept "it's too hard" as a finding** — difficulty is useful information
5. **Check if the time box is up** — if so, stop and document what you know

---

## Comparing Multiple Approaches

When the spike evaluates alternatives, use a structured comparison:

### Give each approach equal time

Divide the time box evenly. Don't spend 80% on your favorite and 20% on the alternative — that's confirmation bias.

### Use the same test scenario for each

Define a single representative scenario and test ALL approaches against it:

```markdown
## Test scenario
Build a prototype that:
1. {Step 1 — same for all approaches}
2. {Step 2 — same for all approaches}
3. {Step 3 — same for all approaches}

Measure:
- Time to implement
- Lines of code
- Performance (if relevant)
- Complexity/readability
```

### Score against the charter criteria

After testing each approach, score them against the evaluation criteria from the charter. Don't decide based on gut feeling when you have a defined scoring system.

---

## When to Stop Early

Stop the spike before the time box if:

- **You answered the question** — no need to keep exploring
- **You hit a hard blocker** — the approach is definitely not viable
- **The question changed** — you discovered the real question is different (write a new charter)
- **Diminishing returns** — more exploration won't change your recommendation

Always document WHY you stopped early. An early stop is not a failure — it's efficiency.
