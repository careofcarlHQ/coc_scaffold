# 00 — Philosophy

> Testing retrofit is not about chasing a coverage number. It is about building confidence, one test at a time, in the places that matter most.

---

## Core Principles

### 1. Test what matters first
Not all code is equally risky. Start with the code that handles money, data integrity, authentication, and the paths users hit most. A 30% coverage that protects the critical paths is worth more than 80% coverage of utility functions.

### 2. Characterize before you specify
When you test existing code, the first question is *what does it actually do?* — not *what should it do?* Write characterization tests that lock the current behavior before you decide whether that behavior is correct. This gives you a safety net before changing anything.

### 3. Tests are documentation
Every test you write is a statement: "this is what the system does, and we intend to keep it this way." Good tests are the most reliable documentation because they fail when reality diverges from the description.

### 4. Start ugly, get clean
Your first tests for untested code will be awkward. They'll have too much setup, test too many things at once, and mock too much. That's fine. A rough test that runs is infinitely more valuable than an elegant test that doesn't exist. Refine later.

### 5. One test is infinitely more than zero
The hardest test to write is the first one for a module. It forces you to figure out imports, fixtures, database state, and configuration. Once you have one working test, the second is much easier. Prioritize getting one test per module before going deep.

### 6. Don't test the framework
You don't need to verify that SQLAlchemy executes SQL or that FastAPI routes HTTP requests. Test *your* logic — the business rules, the edge cases, the transformations. Trust the frameworks you chose.

### 7. Tests must be fast enough to run constantly
If running tests takes more than 30 seconds, developers (and agents) stop running them. Keep the fast tests fast. Separate slow integration tests into their own suite. Optimize the feedback loop.

### 8. Test isolation is non-negotiable
Every test must be independent. No test should depend on another test having run first, on a specific database state left by a previous test, or on external services being available. Tests that fail unpredictably teach people to ignore test failures.

### 9. Coverage is a compass, not a destination
Coverage percentage tells you where you haven't looked. It doesn't tell you whether the tests you have are any good. Use coverage to find blind spots, not as a goal to game.

### 10. Retrofit is ongoing, not a one-time project
You won't go from 0% to 80% in a sprint. Build the habit: every feature gets tests, every bug gets a regression test, every refactor is preceded by characterization tests. Coverage grows with every change.
