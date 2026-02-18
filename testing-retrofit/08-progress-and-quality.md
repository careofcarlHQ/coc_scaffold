# 08 — Progress and Quality

> Tracking coverage growth, test quality, and retrofit momentum. Numbers matter — they tell you whether the safety net is actually growing.

---

## Tracking Coverage Growth

### Coverage timeline

Update this after every testing phase or significant batch of tests:

| Date | Phase | Tests added | Total tests | Coverage | Delta | Floor |
|------|-------|-----------|------------|----------|-------|-------|
| {date} | Baseline | 0 | {N} | {N}% | — | — |
| {date} | Characterization | {N} | {N} | {N}% | +{N}% | — |
| {date} | Unit tests | {N} | {N} | {N}% | +{N}% | {N}% |
| {date} | Integration | {N} | {N} | {N}% | +{N}% | {N}% |

### Module-level tracking

Track coverage growth per module, focusing on the risk map priorities:

| Module | Baseline | Current | Target | Tests | Status |
|--------|----------|---------|--------|-------|--------|
| {critical module 1} | 0% | {N}% | 80% | {N} | {status} |
| {critical module 2} | 5% | {N}% | 80% | {N} | {status} |
| {other module} | 0% | {N}% | 50% | {N} | {status} |

---

## Test Quality Metrics

Raw coverage percentage is necessary but not sufficient. Track these quality indicators:

### Test effectiveness

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Test pass rate | 100% | {N}% | {status} |
| Flaky test count | 0 | {N} | {status} |
| Skipped tests | 0 | {N} | {status} |
| Average test duration | < 100ms | {N}ms | {status} |
| Full suite duration | < 5 min | {N} min | {status} |
| Tests with assertions | 100% | {N}% | {status} |

### Test distribution

| Type | Count | % of total | Target % |
|------|-------|-----------|----------|
| Unit | {N} | {N}% | 60-70% |
| Integration | {N} | {N}% | 20-30% |
| Characterization | {N} | {N}% | 5-15% |
| E2E | {N} | {N}% | < 5% |

The ideal distribution follows the test pyramid: many unit tests, fewer integration tests, even fewer E2E tests.

---

## Quality Gates by Phase

### Phase 1: Infrastructure
- [ ] Test framework runs with zero errors
- [ ] Coverage tool generates reports
- [ ] At least one test passes
- [ ] Test directory structure created

### Phase 2: Characterization Tests
- [ ] Top 5 risk map modules have characterization tests
- [ ] All characterization tests pass
- [ ] Surprising behaviors documented in test comments
- [ ] Coverage increased from baseline

### Phase 3: Unit Tests
- [ ] High-risk business logic has unit tests
- [ ] Unit test suite runs in < 30 seconds
- [ ] Coverage increased by ≥ 15 percentage points
- [ ] Test pattern catalog established

### Phase 4: Integration Tests
- [ ] Critical user paths have integration tests
- [ ] Integration tests use real test database
- [ ] Full test suite runs in < 5 minutes
- [ ] No test interdependencies

### Phase 5: CI Gates
- [ ] CI runs tests on every push/PR
- [ ] Coverage floor set and enforced
- [ ] Merges blocked on test failure
- [ ] Coverage reported in PRs

---

## Ongoing Health Checks

### Weekly check
- [ ] Test pass rate still 100%
- [ ] No new flaky tests
- [ ] Coverage holding steady or increasing
- [ ] Test suite still fast

### Monthly check
- [ ] Coverage floor ratcheted up (if coverage grew 5+ points)
- [ ] No skipped tests without documented reason
- [ ] No quarantined tests older than 2 weeks
- [ ] Test pattern catalog still accurate
- [ ] New modules added with tests

### Quarterly check
- [ ] Coverage growth trend positive
- [ ] Test suite speed still acceptable
- [ ] Risk map reviewed — priorities still correct?
- [ ] Test infrastructure keeping up with codebase growth

---

## Retrofit Completion Criteria

The testing retrofit is "complete enough" when:

1. **Critical coverage**: All modules on the risk priority map have ≥ 80% coverage
2. **Overall coverage**: Total coverage ≥ 50% (ambitious: 70%)
3. **CI enforced**: All merges require passing tests
4. **Floor set**: Coverage floor prevents regression
5. **Habits formed**: New code consistently includes tests
6. **Self-sustaining**: Coverage grows organically with every change

Note: "Complete" doesn't mean "done." The **feature-addition** scaffold ensures new features have tests. The **bug-investigation** scaffold ensures every bug gets a regression test. The **refactoring** scaffold ensures refactoring is preceded by characterization tests. The retrofit is complete when the *habit* is established.

---

## Common problems and solutions

| Problem | Likely cause | Solution |
|---------|-------------|----------|
| Coverage plateau | Testing easy code, avoiding hard code | Revisit risk map, target low-coverage critical modules |
| Tests pass but bugs ship | Tests are shallow (happy path only) | Add edge case and error path tests |
| Test suite getting slow | Too many integration tests | Refactor integration tests into unit tests where possible |
| Flaky tests appearing | Shared state, timing, external deps | Quarantine and fix immediately |
| Developers skip tests | Tests too slow or too flaky | Fix speed and reliability first |
| Coverage drops on merge | New code without tests | Enforce CI gate stricter |
