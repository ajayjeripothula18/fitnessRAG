---
description: Phase 6 - Test and verify implementation
---

# Phase 6: VALIDATE

**Purpose**: Verify implementation correctness through systematic testing.

**Time**: 15 min - 2 hours  
**Next Phase**: COMPLETE (if pass) or ITERATE (if fail)

---

## Test Pyramid Strategy

```
       ┌─────────────┐
       │   E2E Tests │  ← Full workflow (Newman/Browser)
       ├─────────────┤
       │ Integration │  ← API smoke tests (cURL)
       ├─────────────┤
       │ Unit Tests  │  ← Django TestCase (PRIMARY)
       └─────────────┘
```

---

## Validation Steps

### 1. Unit Tests (ALWAYS REQUIRED)

// turbo
```bash
cd app/backend
source venv/bin/activate
python manage.py test apps.[app_name]
```

**Expected**: All tests pass

**If tests fail**:
- 1-2 failures, simple fixes → Back to IMPLEMENT
- Multiple failures, design issues → ITERATE

### 2. Integration Tests (API Endpoints)

**cURL smoke tests**:

```bash
# Test endpoint happy path
curl -X POST http://agency.localhost:8000/api/endpoint/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

**Verify**:
- [ ] Happy path works
- [ ] Error handling works
- [ ] Response format correct

### 3. E2E Tests (If Applicable)

**For full workflows**:
```bash
cd app/backend
newman run .project/postman/collection.json -e environment.json
```

OR browser-based testing for frontend features

---

## Multi-Perspective Validation Checklist

- [ ] Functionality: Does it do what the spec says?
- [ ] UX: Walk through from user's perspective
- [ ] Security: Auth, input validation, data exposure
- [ ] Performance: Query optimization, load times
- [ ] Edge cases: What happens when X fails?
- [ ] Operations: What happens at 2 AM on a Sunday?

---

## Decision Point

```
Test Results?
├─ All Pass → COMPLETE ✅
├─ Minor Issues → Back to IMPLEMENT
│   Examples:
│   • 1-3 small, well-defined bugs
│   • Typos, UI tweaks
│   • Missing validation message
│   • Can be fixed in <30 min
│
└─ Major Issues → ITERATE
    Examples:
    • Wrong approach/design
    • Multiple test failures (>3)
    • Missing requirements
    • Blocker with no clear fix
```

---

## Outputs

- [ ] Test results documented
- [ ] Session log updated with validation results
- [ ] Decision made (complete/implement/iterate)
- [ ] Issues logged (if any)

### Decision Log (append after each major discussion)
- ✅ **Decision Made**: [what was agreed]
- ❓ **Open Question**: [what needs more research]
- 🚫 **Rejected**: [what was dropped and why]
- 📌 **Action Item**: [what happens next]
- ⚠️ **Risk Flagged**: [new risks identified]

---

## Success Criteria

### ✅ To Mark COMPLETE

ALL must be true:
- [ ] All tests pass (unit, integration, E2E)
- [ ] Acceptance criteria met (from PLAN phase)
- [ ] No blocking issues
- [ ] User tested (if manual verification needed)
- [ ] Session log complete

### ⚠️ To Return to IMPLEMENT (Minor Fixes)

- 1-3 small, well-defined bugs
- Implementation approach is correct
- Can be fixed quickly (<30 min)

### ❌ To Escalate to ITERATE (Major Issues)

- Design is flawed
- Requirements were misunderstood
- Multiple test failures (>3)
- Blocker issues with no clear fix
- Performance beyond acceptable range

---

## Test Commands Reference

### Django Tests
```bash
# All tests
python manage.py test

# Specific app
python manage.py test apps.[app_name]

# Specific test file
python manage.py test apps.[app].tests.test_[feature]

# Specific test
python manage.py test apps.[app].tests.test_[feature].TestClass.test_method
```

### Newman (Postman CLI)
```bash
newman run collection.json -e environment.json --reporters cli,json
```

### cURL Template
```bash
curl -X [METHOD] http://[HOST]/api/endpoint/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

---

**Next**: COMPLETE ✅ or [Phase 7: ITERATE](file://.agent/workflows/iterate.md)  
**Previous**: [Phase 5: IMPLEMENT](file://.agent/workflows/implement.md)  
**Back**: [Master Workflow](file://.agent/workflows/rrpai.md)
