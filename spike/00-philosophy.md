# 00 — Philosophy

> A spike is not play time. It's a disciplined, time-boxed investment in reducing uncertainty before you commit resources to building something.

---

## Core Principles

### 1. Define the question before you start exploring
Every spike exists to answer a specific question. "Explore GraphQL" is not a spike — it's a rabbit hole. "Can we replace our REST endpoints with GraphQL without breaking existing consumers?" is a spike. If you can't state the question clearly, you're not ready to spike.

### 2. Time-box ruthlessly
A spike without a time box is just procrastination with a technical veneer. Set a deadline before you start. When the time box expires, you stop and report what you know — even if the answer is "we need more time" (which itself is a valuable finding). Typical time boxes: 2 hours, 4 hours, 1 day, 3 days. Never more than a week.

### 3. Optimize for learning, not for code quality
Spike code is disposable by design. Don't write tests, don't refactor, don't handle edge cases. Copy-paste from examples. Hardcode values. Skip error handling. The output of a spike is *knowledge*, not code. If the code happens to be useful later, that's a bonus, not a goal.

### 4. Record everything as you go
Your spike is worthless if you can't remember what you tried and what happened. Keep a running log: what you tried, what worked, what didn't, what surprised you. This log is the real deliverable — not the prototype code.

### 5. One question at a time
Resist the urge to explore everything at once. "Can we use Redis for caching, and also should we switch to async endpoints, and while we're at it let's try a new ORM" is three spikes, not one. Compound spikes produce muddled findings.

### 6. Failure is a valid outcome
A spike that concludes "this approach won't work for us, here's why" is just as valuable as one that says "it works, let's build it." The purpose is to reduce uncertainty, and ruling out an option is uncertainty reduction. Don't feel pressure to make the spike "succeed."

### 7. Don't deploy spike code
Spike code is exploratory. It has no tests, no error handling, and was written for speed, not correctness. If the spike validates an approach, the real implementation starts from scratch using the **feature-addition** or **greenfield** scaffold. Spike code is reference material, not a starting point.

### 8. Share the findings, not just the conclusion
"We should use approach A" is a conclusion. A useful spike documents *why* — what were the alternatives, what did you test, what surprised you, what are the trade-offs. This lets future-you (or anyone else) understand the reasoning without repeating the exploration.

### 9. Spike early, not late
The best time to spike is when you're uncertain and the cost of getting it wrong is high. Spiking before you commit to an approach saves days or weeks of building the wrong thing. Spiking after you've already built half of it is just confirming a sunk cost.

### 10. Archive, don't delete
When the spike is done, archive the code, log, and findings somewhere findable. Six months from now, when someone asks "why didn't we use GraphQL?" the archived spike answers the question with evidence.
