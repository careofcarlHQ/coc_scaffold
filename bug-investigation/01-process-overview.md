# 01 — Process Overview: End-to-End Bug Investigation Workflow

## The investigation lifecycle

Bug investigation follows a predictable lifecycle. Each phase produces artifacts that make the next phase more effective.

```
┌─────────────────────────────────────────────────────────┐
│                BUG INVESTIGATION LIFECYCLE               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. CAPTURE            Document the symptom             │
│       │                                                 │
│       ▼                                                 │
│  2. REPRODUCE          Find minimal trigger             │
│       │                                                 │
│       ▼                                                 │
│  3. ISOLATE            Narrow the problem space         │
│       │                                                 │
│       ▼                                                 │
│  4. DIAGNOSE           Find root cause via hypotheses   │
│       │                                                 │
│       ▼                                                 │
│  5. SPEC THE FIX       Plan the change                  │
│       │                                                 │
│       ▼                                                 │
│  6. IMPLEMENT          Fix + regression test            │
│       │                                                 │
│       ▼                                                 │
│  7. VERIFY             Confirm fix, no regressions      │
│       │                                                 │
│       ▼                                                 │
│  8. PREVENT            Systemic improvements            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Phase breakdown

### 1. Capture (10 minutes)

**Input**: A bug report, error log, or observed misbehavior
**Output**: Symptom capture document

Activities:
- What is happening? (observed behavior)
- What should be happening? (expected behavior)
- When did it start? (first occurrence, any pattern)
- What changed recently? (deployments, config, data)
- Who is affected? (all users, specific cases, specific data)
- How severe is this? (data loss, broken flow, cosmetic)

Key document:
- `bugfix/symptom-capture.md`

Gate: Symptom is documented clearly enough that someone else could understand the problem.

### 2. Reproduce (15–60 minutes)

**Input**: Symptom capture
**Output**: Minimal, deterministic reproduction steps

Activities:
- Try to trigger the bug using the reported conditions
- Strip away unnecessary steps until you have the minimal trigger
- Document exact environment (versions, data state, config)
- Confirm the reproduction is deterministic (same steps → same bug)

If reproduction fails:
- Add logging/tracing to the suspected code path
- Check for environment differences (local vs. production)
- Check for data-dependent triggers (specific records)
- Check for timing/concurrency factors

Gate: Bug can be triggered reliably with documented steps.

### 3. Isolate (15–30 minutes)

**Input**: Reproduction steps
**Output**: Narrowed problem area (specific module, function, or line)

Activities:
- Binary search the code path: add logging at midpoints
- Check: is the input correct at point A? At point B? Where does it go wrong?
- Check: does the bug occur with different data? Different config?
- Identify the exact function or line where behavior diverges from expected

Techniques:
- **Log injection**: Add temporary logging at strategic points
- **Binary search**: Comment out half the logic, see if bug persists
- **Data variation**: Try different inputs to find the trigger condition
- **Config variation**: Change settings to isolate environment factors
- **Git bisect**: If the bug is recent, find the introducing commit

Gate: Problem is localized to a specific code area (file, function, or code block).

### 4. Diagnose (30 minutes – 2 hours)

**Input**: Isolated problem area
**Output**: Root cause analysis document

Activities:
- Formulate hypotheses for why the bug exists
- Test each hypothesis systematically
- Document confirmed/rejected hypotheses
- Trace the causal chain from root cause to symptom
- Check for sibling bugs (same pattern elsewhere)

Key document:
- `bugfix/hypothesis-log.md`
- `bugfix/root-cause-analysis.md`

Gate: Root cause identified and documented. Causal chain from root to symptom is clear.

### 5. Spec the Fix (15 minutes)

**Input**: Root cause analysis
**Output**: Fix specification

Activities:
- Define exactly what code changes are needed
- Assess risk: what could this change break?
- Define the regression test that will guard against recurrence
- Decide: root cause fix only, or also add defensive checks?
- Check: does this fix need a migration? Config change? Deployment step?

Key document:
- `bugfix/fix-spec.md`

Gate: Fix is scoped, risks identified, regression test defined.

### 6. Implement (30 minutes – 2 hours)

**Input**: Fix specification
**Output**: Code fix + regression test

Activities:
- Write the regression test FIRST (it should fail)
- Apply the fix
- Run the regression test (it should now pass)
- Run the full test suite (no regressions)

Rules:
- Fix only what the fix spec describes
- Don't refactor, don't add features, don't "improve" nearby code
- If you find other bugs during the fix, log them separately
- Keep the change as small as possible

Gate: Regression test fails before fix, passes after. Full test suite passes.

### 7. Verify (15 minutes)

**Input**: Implemented fix
**Output**: Verification evidence

Activities:
- Run the original reproduction steps — bug should be gone
- Run the regression test — should pass
- Run the full test suite — zero new failures
- Check for sibling bugs if applicable
- Verify no side effects on related functionality

Gate: Bug is gone. Regression test passes. No new failures. No side effects.

### 8. Prevent (15 minutes)

**Input**: Root cause analysis + fix
**Output**: Prevention items for systemic improvement

Activities:
- Ask: "What class of bug is this?"
- Ask: "Would a linter rule catch this?"
- Ask: "Would a type annotation prevent this?"
- Ask: "Should this test pattern be applied more broadly?"
- Add prevention items to the project backlog

Key document:
- Prevention items added to `bugfix/root-cause-analysis.md`

Gate: At least one prevention item identified and logged.

---

## Time budget

| Severity | Total time box | Typical breakdown |
|----------|---------------|-------------------|
| Trivial | 30 min | 5 + 5 + 5 + 5 + 5 + 5 minutes |
| Simple | 1–2 hours | 10 + 15 + 15 + 30 + 10 + 20 + 10 + 10 minutes |
| Medium | 2–4 hours | 10 + 30 + 30 + 60 + 15 + 45 + 15 + 15 minutes |
| Complex | 4–8 hours | Split across sessions with documented checkpoints |

If you exceed the time box, stop and:
1. Document what you've learned
2. Document what you've ruled out
3. Take a break or start a fresh agent session
4. Consider asking for help or a fresh perspective
