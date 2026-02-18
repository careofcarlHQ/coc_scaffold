# 00 — Philosophy

> Incident response is not about blame. It's about restoring service, understanding what happened, and making the system stronger.

---

## Core Principles

### 1. Mitigate first, diagnose second
When production is on fire, your first job is to stop the bleeding. Roll back, toggle off, redirect traffic — whatever gets users back to a working state. Root cause analysis happens *after* the immediate pain stops.

### 2. Time is the enemy
Every minute of an incident costs trust, money, or both. Bias toward action. A quick mitigation that's imperfect beats a perfect fix that takes two hours. You can always improve the fix later — you can't un-lose the users who gave up.

### 3. Capture everything in real time
Write things down *as they happen*. Timestamps, observations, actions taken, results observed. Your memory under stress is unreliable. The incident report is your flight recorder — it makes the post-mortem possible and accurate.

### 4. Don't make it worse
Under pressure, it's tempting to try aggressive fixes. Every action you take during an incident carries risk. Before doing anything, ask: "what's the worst case if this action fails?" If it could make things worse, step back and think.

### 5. Blame the system, not the person
Incidents happen because systems fail — because there wasn't a test, a check, a guard rail, or a monitoring alert. Blaming people teaches them to hide problems. Blaming systems creates improvements.

### 6. Every incident is a gift
Each incident reveals something about your system that you didn't know or hadn't addressed. The cheapest way to learn is from incidents that have already happened. The post-mortem turns pain into prevention.

### 7. Scope before you leap
Before you start fixing, understand the blast radius. Is it affecting all users or one? One endpoint or the whole service? One region or all? Knowing the scope determines the urgency and the response strategy.

### 8. Rollback is always an option
If you deployed recently, rolling back is almost always the fastest mitigation. Keep rollback trivial. If rolling back is hard or scary, that's a problem to fix *after* the incident.

### 9. Communicate clearly and often
If users are affected, tell them what you know, when you expect resolution, and when you'll update them next. "We're aware and investigating" is infinitely better than silence. Over-communicate during incidents.

### 10. Follow up or it was pointless
An incident without a post-mortem is a wasted crisis. A post-mortem without action items is theater. Action items without follow-through are lies. Complete the loop: incident → post-mortem → action items → implementation → verification.
