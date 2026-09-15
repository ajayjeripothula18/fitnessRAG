---
description: Systematic debugging workflow for Antigravity PM and CC agents
---

# Debugging Workflow for Antigravity

**Version**: 1.0  
**Last Updated**: 2026-01-04  
**Purpose**: Systematic approach to debugging issues in Antigravity workflows

---

## When to Use This Workflow

### ✅ Use For:
- Unexpected errors during RRPAI phases
- Implementation failures (tests not passing)
- Integration issues (API, database, dependencies)
- Performance problems
- Mysterious bugs or edge cases

### ❌ Use ITERATE Phase Instead:
- Validation failures after implementation
- Design flaws discovered during testing
- Requirements misunderstood

---

## The 6-Step Debugging Cycle

```
1. REPRODUCE → Make the bug reliably appear
2. GATHER → Collect all evidence (logs, traces, errors)
3. ISOLATE → Narrow down to specific code/module
4. HYPOTHESIZE → Form theories about root cause
5. TEST → Validate hypotheses systematically
6. VERIFY → Confirm fix and prevent regression
```

---

## Step 1: REPRODUCE the Issue

### Purpose
Consistently reproduce the bug to validate fixes.

### Actions

#### 1. Document the Bug Report
```markdown
## Bug Report

**Symptom**: [What goes wrong]
**Expected**: [What should happen]
**Actual**: [What actually happens]
**Frequency**: Always / Intermittent / First occurrence
**Environment**: Dev / Test / Production
**First Observed**: [Date/commit]
```

#### 2. Create Minimal Reproduction

**For API issues**:
```bash
# Save exact cURL command that triggers bug
curl -X POST http://agency.localhost:8000/api/endpoint/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"minimal": "payload"}'
```

**For Django issues**:
```python
# Create minimal test case
# Save in debugging_temp.py

from django.test import TestCase

class ReproduceTest(TestCase):
    def test_reproduce_bug(self):
        # Minimal code to trigger bug
        result = broken_function(minimal_input)
        # Assert what fails
```

#### 3. Verify Reproducibility

- [ ] Can reproduce on demand (>90% of the time)
- [ ] Documented exact steps to trigger
- [ ] Identified triggering data/conditions
- [ ] Confirmed happens in clean environment

---

## Step 2: GATHER Evidence

### Purpose
Collect comprehensive information about the bug.

### Evidence Collection Checklist

#### A. Error Messages & Stack Traces

**Django (with DEBUG=True)**:
```bash
# Full error page shows:
# - Exception type and message
# - Full stack trace
# - Local variables at each frame
# - Request/response details
```

**Python Traceback Analysis**:
```
Focus on:
1. BOTTOM of trace → Where error was raised
2. YOUR CODE frames → Skip library frames
3. Variable values → State when it failed
```

#### B. Log Files

**Check application logs**:
// turbo
```bash
# Recent logs
tail -100 app/backend/logs/debug.log

# Search for errors
grep -i "error\|exception\|traceback" app/backend/logs/debug.log | tail -50
```

**Check Django logs**:
```python
# Add temporary logging
import logging
logger = logging.getLogger(__name__)

logger.debug(f"Variable state: {data}")
logger.error(f"Failed at step: {step}", exc_info=True)
```

#### C. Database State

```bash
# Enter Django shell
cd app/backend
python manage.py shell
```

```python
# Inspect data
from apps.feature.models import MyModel

# Check record existence
MyModel.objects.filter(id=suspicious_id)

# Check relationships
instance = MyModel.objects.get(id=123)
instance.related_set.all()

# Raw SQL inspection
from django.db import connection
print(connection.queries[-5:])  # Last 5 queries
```

#### D. Request/Response Details

**For API debugging**:
- Request headers
- Request body (sanitize sensitive data)
- Response status code
- Response body
- Response time

**Save as**:
```bash
# Detailed request logging
curl -v -X POST... > debug_request.log 2>&1
```

---

## Step 3: ISOLATE the Problem

### Purpose
Narrow down to the exact location causing the bug.

### Isolation Techniques

#### A. Binary Search Debugging

**Disable half the code, test, repeat**:

```python
def complex_function(data):
    step1 = process_step1(data)
    step2 = process_step2(step1)
    # COMMENT OUT bottom half
    # step3 = process_step3(step2)
    # step4 = process_step4(step3)
    # return step4
    return step2  # TEMPORARY - test where it breaks
```

If error gone → Bug is in commented section
If error persists → Bug is in active section

#### B. Add Debug Breakpoints

**Using Python debugger (pdb)**:
```python
# Insert at suspicious location
import pdb; pdb.set_trace()

# Or use Python 3.7+ breakpoint()
breakpoint()
```

**PDB commands**:
```
n - next line
s - step into function
c - continue execution
p variable_name - print variable
l - list code around current line
q - quit debugger
```

#### C. Print Statement Debugging

```python
# Strategic print placements
print(f"DEBUG [1]: Entering function, data={data}")
result = risky_operation(data)
print(f"DEBUG [2]: After operation, result={result}")
```

**Use prefixes** for easy grep:
```bash
# Find all debug prints
grep "DEBUG \[" app/backend/logs/output.log
```

#### D. Module Isolation

```python
# Test module in isolation
python manage.py shell
>>> from apps.feature.utils import suspicious_function
>>> suspicious_function(test_input)
# Trace error directly
```

---

## Step 4: HYPOTHESIZE Root Cause

### Purpose
Form testable theories about why the bug occurs.

### Hypothesis Framework

#### Common Bug Categories

| Category | Hypothesis Template | Check |
|----------|-------------------|-------|
| **Logic Error** | "Function X assumes Y but input is Z" | Review conditionals, edge cases |
| **Data Issue** | "Database record is in invalid state" | Inspect data, check migrations |
| **Race Condition** | "Operation A and B conflict when concurrent" | Check async code, locks |
| **Missing Validation** | "Input not validated before use" | Check serializers, forms |
| **Side Effect** | "Function X modifies shared state Y" | Check global vars, class attrs |
| **Integration** | "External service S returned unexpected format" | Check API contracts, mocks |
| **Environment** | "Works locally, fails in staging" | Compare env vars, database states |

#### Form Hypothesis

```markdown
## Hypothesis: [Theory about root cause]

**Evidence**:
- Log shows: [specific evidence]
- Stack trace indicates: [specific location]
- Data inspection reveals: [specific state]

**Prediction**: If this is the cause, then:
1. [Expected observation 1]
2. [Expected observation 2]

**Test**: [How to validate this hypothesis]
```

---

## Step 5: TEST Hypothesis

### Purpose
Validate or invalidate each hypothesis systematically.

### Testing Strategies

#### A. Add Validation Tests

```python
# Test your hypothesis with explicit assertion
def test_hypothesis_validation(self):
    """Test: Function fails when input is None"""
    # Setup condition that hypothesis predicts
    with self.assertRaises(ExpectedError):
        broken_function(None)
```

#### B. Modify Code to Prove Theory

**Add defensive checks**:
```python
# BEFORE (hypothesis: data can be None)
def process(data):
    return data.transform()

# AFTER (test hypothesis)
def process(data):
    if data is None:
        raise ValueError("DEBUG: Data was None! Hypothesis confirmed")
    return data.transform()
```

#### C. Use Django Debug Toolbar

```bash
# Install if not present
pip install django-debug-toolbar

# Add to INSTALLED_APPS in settings.py
```

**Inspect**:
- SQL queries (N+1 problems?)
- Template context (missing variables?)
- Request timing (slow operations?)
- Cache hits/misses

#### D. Profile Performance Issues

```python
import cProfile
import pstats

# Profile specific function
profiler = cProfile.Profile()
profiler.enable()

slow_function()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 slowest
```

---

## Step 6: VERIFY the Fix

### Purpose
Confirm the bug is fixed and won't regress.

### Verification Checklist

#### A. Regression Test

```python
# Create permanent test for this bug
class TestBugFix(TestCase):
    def test_issue_XYZ_fixed(self):
        """Regression test for bug: [description]"""
        # Exact scenario that triggered original bug
        result = function_that_was_broken(problematic_input)
        
        # Assert it now works correctly
        self.assertEqual(result, expected_output)
```

#### B. Integration Testing

**Test full workflow**:
// turbo
```bash
# Run complete test suite
cd app/backend
python manage.py test
```

**Manual API check**:
```bash
# Test the exact scenario from bug report
curl -X POST http://agency.localhost:8000/api/endpoint/ \
  -H "Authorization: Bearer $TOKEN" \
  -d @bug_reproduction_payload.json
```

#### C. Check for Side Effects

- [ ] Original bug is fixed
- [ ] No new errors introduced
- [ ] Performance not degraded
- [ ] Edge cases still handled
- [ ] Related features still work

#### D. Update Documentation

```markdown
## Session Log - Bug Fix

**Bug**: [Bug ID/description]
**Root Cause**: [What was wrong]
**Fix**: [What changed]
**Testing**: [How verified]
**Prevented By**: [Test added / validation added]
```

---

## Django-Specific Debugging

### Common Django Issues

#### 1. URL/View Errors

**"Page not found (404)"** or **"Reverse not found"**:

```bash
# Check URL configuration
python manage.py show_urls | grep "pattern"

# Verify URL name
grep "name='view_name'" app/backend/apps/*/urls.py
```

#### 2. Migration Issues

**"Table doesn't exist"** or **"Column not found"**:

```bash
# Check migration status
python manage.py showmigrations

# Create missing migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check SQL for migration
python manage.py sqlmigrate app_name 0001
```

#### 3. ORM Query Problems

**N+1 Query Problem**:
```python
# BAD - N+1 queries
for booking in Booking.objects.all():
    print(booking.agency.name)  # Query per booking!

# GOOD - 2 queries total
for booking in Booking.objects.select_related('agency'):
    print(booking.agency.name)
```

**Debug ORM queries**:
```python
from django.db import connection, reset_queries

reset_queries()
# Your ORM operations
queryset = MyModel.objects.filter(...).select_related(...)

print(f"Query count: {len(connection.queries)}")
for q in connection.queries:
    print(q['sql'])
```

#### 4. Template Rendering Issues

```python
# Enable template debugging
# settings.py
TEMPLATES = [{
    'OPTIONS': {
        'debug': True,  # Shows template errors clearly
    }
}]
```

#### 5. Signal/Async Issues

```python
# Add debug logging to signals
import logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=MyModel)
def debug_signal(sender, instance, **kwargs):
    logger.debug(f"Signal triggered for {instance.id}")
    # Signal logic
    logger.debug(f"Signal completed for {instance.id}")
```

---

## Advanced Techniques

### Rubber Duck Debugging

**For complex/mysterious bugs**:

1. **Explain code out loud** (or to a colleague/rubber duck)
2. **Walk through line-by-line** what the code does
3. **Question assumptions** you've made

Often, explaining forces you to notice gaps in logic.

### Time-Travel Debugging (Git Bisect)

**Find which commit introduced the bug**:

```bash
# Start bisect
git bisect start
git bisect bad  # Current commit is bad
git bisect good v1.0.0  # Known good commit

# Git will checkout commits to test
# For each commit, test and mark:
git bisect good  # If bug doesn't exist
git bisect bad   # If bug exists

# Git identifies problematic commit
git bisect reset  # Exit bisect mode
```

### Remote Production Debugging

**⚠️ NEVER use pdb in production!**

Instead:

```python
# Use comprehensive logging
logger.error(
    f"Unexpected state in production",
    extra={
        'user_id': user.id,
        'request_data': sanitized_data,
        'state': current_state,
    },
    exc_info=True  # Include traceback
)

# Use error monitoring service (Sentry, Rollbar)
# Captures full context automatically
```

---

## Error Complexity & Escalation

Use this to determine how much debugging to invest:

| Complexity | Characteristics | Time Budget | Escalation |
|------------|----------------|-------------|------------|
| **Trivial** | Typo, missing import, obvious fix | <5 min | Fix immediately |
| **Simple** | Logic bug, off-by-one, null check | 15-30 min | Document in session log |
| **Medium** | State management, API mismatch | 1-2 hours | May need ITERATE phase |
| **Complex** | Race condition, ORM optimization | 2-4 hours | Consider pairing/research |
| **Critical** | Security, data corruption, mystery | >4 hours or uncertain | **Escalate to user** |

**Escalation criteria**:
- [ ] >2 hours spent with no clear progress
- [ ] Requires architectural changes
- [ ] Impacts other features
- [ ] Security or data integrity concerns
- [ ] Can't reproduce reliably

---

## Quick Reference

### Debugging Commands

```bash
# Django debugging
python manage.py shell  # Interactive environment
python manage.py dbshell  # Direct database access
python manage.py check  # System check
python manage.py showmigrations  # Migration status

# Logs
tail -f app/backend/logs/debug.log  # Live logs
grep -i error app/backend/logs/*.log  # Find errors

# Testing
python manage.py test apps.myapp  # Run tests
python manage.py test apps.myapp.tests.test_file.TestClass.test_method  # Specific test
```

### PDB Quick Reference

```
# Breakpoint insertion
import pdb; pdb.set_trace()
breakpoint()  # Python 3.7+

# Commands
n - Next line
s - Step into
c - Continue
p var - Print variable
pp var - Pretty print
l - List code
w - Where am I (stack)
u - Up stack frame
d - Down stack frame
q - Quit
```

---

## Integration with RRPAI

**Debugging fits into RRPAI at multiple points**:

1. **During IMPLEMENT**: Minor bugs → Fix and continue
2. **During VALIDATE**: Test failures → Debug before ITERATE
3. **During ITERATE**: Root cause analysis uses debugging

**When debugging takes >30 min**:
- Document in session log
- Update sprint tracker with blocker
- If >2 hours, escalate via ITERATE phase

---

**Last Updated**: 2026-01-04  
**Version**: 1.0  
**Integrated with**: RRPAI v3.1  
**Next**: `/rrpai/iterate` for major issues
