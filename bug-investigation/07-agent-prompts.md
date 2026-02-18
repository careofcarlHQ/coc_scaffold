# 07 — Agent Prompts for Bug Investigation

## Purpose

Concrete, copy-paste prompts for each phase of bug investigation. Use these to brief agents on specific debugging tasks.

---

## Symptom Analysis Prompt

```
A bug has been reported. Analyze the symptom and prepare for investigation.

Symptom: [paste error message, traceback, or behavior description]

Tasks:
1. Parse the error/symptom — what type of error is this?
2. Identify the code path from the traceback (if available)
3. List the files and functions involved
4. Check recent git history on those files — what changed recently?
5. Classify severity: critical / high / medium / low
6. Suggest initial hypotheses (at least 2)

Output a structured symptom analysis.
```

---

## Reproduction Prompt

```
I need to reproduce this bug reliably.

Symptom: [paste symptom description]
Suspected area: [file/module if known]

Tasks:
1. Read the code path that produces this error
2. Identify what inputs/conditions would trigger it
3. Write a minimal test case that triggers the bug
4. Run the test case and confirm it fails with the expected error
5. If you can't reproduce, identify what conditions might be missing

Output:
- Reproduction steps
- Minimal test case (code)
- Test result (does it reproduce?)
- If no: list what conditions you think are needed
```

---

## Hypothesis Investigation Prompt

```
I'm investigating a bug. Test the following hypothesis.

Hypothesis: [state the hypothesis]
Expected evidence if true: [what we'd see]
Expected evidence if false: [what we'd see instead]

Tasks:
1. Gather the evidence needed to confirm or reject this hypothesis
2. Read relevant code, check data, run queries, or add logging as needed
3. Report: confirmed / rejected / inconclusive
4. If confirmed: suggest the next question (trace deeper)
5. If rejected: suggest an alternative hypothesis

Document your findings in hypothesis-log format:
- Hypothesis
- Test performed
- Result
- Time spent
- Next step
```

---

## Root Cause Analysis Prompt

```
The bug has been isolated to this area:

Location: [file:line or function]
Condition: [what triggers it]
Current hypotheses tested: [reference hypothesis-log.md]

Tasks:
1. Read the isolated code carefully
2. Trace the causal chain — WHY does this condition exist?
3. Identify the root cause (not just the symptoms)
4. Check for sibling bugs — does the same pattern exist elsewhere?
5. Assess scope — how many users/records are affected?

Output a root cause analysis with:
- Root cause statement
- Causal chain (root → intermediate → symptom)
- Sibling bugs found
- Scope assessment
- Suggested fix approach
```

---

## Fix Implementation Prompt

```
Implement a fix for this bug.

Root cause: [reference root-cause-analysis.md]
Fix spec: [reference fix-spec.md or describe the planned fix]

Tasks:
1. Write a regression test FIRST that reproduces the bug (should FAIL)
2. Apply the fix as described in the fix spec
3. Run the regression test (should now PASS)
4. Run the full existing test suite (zero new failures)
5. Verify the original reproduction steps no longer trigger the bug

Rules:
- Fix ONLY what the fix spec describes
- Do NOT refactor nearby code
- Do NOT add features while fixing
- If you find other bugs, log them separately — do not fix them
- Keep changes minimal

Output:
- Regression test (code)
- Fix applied (diff summary)
- Test results (regression test + full suite)
- Any bugs discovered but not fixed (logged separately)
```

---

## Sibling Bug Search Prompt

```
We found a bug caused by [pattern description].
Check if the same pattern exists elsewhere in the codebase.

Pattern: [describe the specific bug pattern]
Example: [reference the bug that was found]

Tasks:
1. Search the codebase for the same pattern
2. For each instance found:
   - Location (file:line)
   - Risk level (could it trigger the same type of failure?)
   - Current protection (is there a guard? is it tested?)
3. Prioritize findings: which ones are most likely to cause production issues?

Output a list of sibling bug locations with risk assessment.
```

---

## Post-Fix Prevention Prompt

```
A bug was fixed. Help identify systemic improvements to prevent this class of bug.

Root cause: [brief description]
Fix applied: [brief description]

Tasks:
1. What CLASS of bug is this? (null access, race condition, state violation, etc.)
2. Would a type annotation prevent this? (e.g., Non-null type)
3. Would a linter rule catch this? (e.g., no unguarded attribute access)
4. Would a test pattern prevent this? (e.g., property-based testing for edge cases)
5. Would an architectural change prevent this? (e.g., make impossible states unrepresentable)
6. Are there sibling bugs that the same prevention would catch?

Output:
- Prevention recommendations (actionable, specific)
- Effort estimate for each
- Priority (how many bugs would each prevention catch?)
```
