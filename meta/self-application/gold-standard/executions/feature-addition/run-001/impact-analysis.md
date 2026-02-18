# Impact Analysis — One-click solo merge automation

## Feature Summary
Add a single-command, agent-safe merge flow for protected branches, including protection mode toggling, safe restore, verification, and local cleanup.

## Database Layer

### New tables
| Table | Purpose |
|-------|---------|
| N/A | no database change |

### Modified tables
| Table | Change | Risk |
|-------|--------|------|
| N/A | none | low |

### Queried tables (unchanged)
| Table | Query pattern | Performance risk |
|-------|---------------|-----------------|
| N/A | none | low |

### Migration safety
- [x] Can run without downtime
- [x] Is reversible
- [x] Handles existing data correctly

## Service Layer

### New functions
| Module | Function | Purpose |
|--------|----------|---------|
| `scripts/solo-merge-pr.ps1` | `Resolve-GitHubToken` | Resolve token from env or `.env.local` |

### Modified functions
| Module | Function | Change | Callers affected |
|--------|----------|--------|-----------------|
| `scripts/set-branch-protection.ps1` | script flow | mode support + required check alignment | merge automation + operators |

### External dependencies
| Service | Interaction | Failure mode |
|---------|-------------|-------------|
| GitHub REST API | merge + branch protection endpoints | non-mergeable PR / auth / required-check mismatch |

## API Layer

### New endpoints
| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| N/A | N/A | N/A | N/A |

### Modified endpoints
| Method | Path | Change | Backward compatible? |
|--------|------|--------|---------------------|
| N/A | N/A | none | yes |

### Unchanged endpoints at risk
| Endpoint | Risk | Reason |
|----------|------|--------|
| GitHub merge API | medium | protected-branch rules can reject invalid preconditions |

## UI Layer

### New pages/components
| Component | Purpose |
|-----------|---------|
| N/A | none |

### Modified pages/components
| Component | Change |
|-----------|--------|
| README/PR template docs | operator guidance updates |

## Background Jobs

### New jobs
| Job | Trigger | Purpose |
|-----|---------|---------|
| N/A | N/A | N/A |

### Modified jobs
| Job | Change |
|-----|--------|
| N/A | none |

## Tests

### Existing tests covering affected code
| Test file | Tests | Status |
|-----------|-------|--------|
| `tests/test_ci_policy.py` | policy checks | passing |
| `tests/test_process_integrity.py` | template/readme contract checks | passing |

### New tests needed
| Layer | Test | Priority |
|-------|------|----------|
| process automation | check required context equals check-run context | P0 |
| docs consistency | ensure CI context naming consistent across key docs | P1 |

## Configuration

### New environment variables
| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| N/A | no | N/A | existing `GITHUB_TOKEN` reused |

## Impact Summary

- **Database**: 0 new tables, 0 modified tables
- **Services**: script-level logic added/updated
- **Endpoints**: 0 new endpoints, 0 modified endpoints
- **UI**: doc-level changes only
- **Jobs**: 0 new jobs, 0 modified jobs
- **Tests**: existing suite used as gate
- **Config**: no new env vars

### Risk Assessment
- **Blast radius**: medium (merge workflow behavior)
- **Backward compatibility**: preserved
- **Estimated implementation time**: 1 day
- **Rollback complexity**: simple

### Red Flags
- [ ] Modifies more than 5 existing modules
- [ ] Requires breaking API changes
- [ ] Modifies shared utility code
- [ ] Requires large data backfill
- [ ] Affects auth logic
- [ ] Low test coverage on affected code (< 50%)
