---
description: Phase 5 - Execute changes with mandatory checkpoints
---

# Phase 5: IMPLEMENT

**Purpose**: Execute the planned changes with proper session logging.

**Time**: 1-40 hours (varies by task)  
**Next Phase**: VALIDATE

---

## Implementation Approach

### For PM (Antigravity)
1. Create implementation prompt for Claude Code
2. Update TODO_NOW.md with [/] in-progress marker
3. Update SPRINT_TRACKER feature lifecycle: "In Progress"
4. Monitor Claude Code progress
5. **Create session logs at checkpoints**

### For CC (Claude Code)
1. Read all steering files (`.kiro/steering/`)
2. Read assigned prompt fully
3. Execute step-by-step
4. Run verification commands as specified
5. Report results

---

## Session Checkpoint Protocol (MANDATORY)

### When to Create Checkpoints

**Mandatory for**:
- Multi-session work (>4 hours)
- End of each implementation phase
- Before/after breaking changes
- **At least once per day** for multi-day work

**Checkpoint criteria**:
- Testable unit of work complete
- No blocking errors
- State is committable
- Progress can be verified

### Checkpoint Actions

1. **Create session log** using `SESSION_LOG_ENHANCED.template.md`
2. **Run basic tests** appropriate to current phase
3. **Update sprint tracker** feature lifecycle
4. **Commit changes locally** (optional but recommended)

---

## Session Log Creation

**Template**: `app/backend/.project/prompts/templates/SESSION_LOG_ENHANCED.template.md`

**Location**: `.project/history/sessions/weekN/[feature-name]-checkpoint-N.md`

**Naming conventions**:
```
[feature-name]-checkpoint-1.md   # First checkpoint
[feature-name]-checkpoint-2.md   # Second checkpoint
[feature-name]-final.md          # Final implementation
[feature-name]-iteration-1.md    # If iteration needed
```

**Must include**:
- RRPAI Progress Tracker (mark Phase 5 as 🔄 In Progress)
- Key actions taken
- Files changed
- Tests run
- Decisions made
- Blockers (if any)
- Next steps

---

## Error Handling During Implementation

```
Error encountered?
├─ Syntax/Import → Fix immediately, continue
├─ Simple logic bug → Fix, note in session log, continue
├─ Design issue → STOP, escalate to ITERATE phase
└─ Blocker (unknown) → STOP, escalate to user
```

### Error Escalation Criteria

**Escalate to ITERATE if**:
- Design approach is flawed
- Multiple similar errors (pattern)
- Unknown blocker >15 min to debug

**Escalate to USER if**:
- Breaking changes needed
- Requirements unclear
- Timeline impact significant

---

## PM/CC Handoff Protocol

### PM → CC (Delegation)
1. PM creates prompt in `.project/prompts/weekN/`
2. PM updates TODO_NOW.md and SPRINT_TRACKER
3. PM notifies user: "Prompt ready for CC"
4. User copies prompt to Claude Code
5. CC executes implementation

### CC → PM (Checkpoint)
1. CC completes checkpoint unit of work
2. CC creates checkpoint session log
3. CC reports results to user
4. User notifies PM of checkpoint completion
5. PM reviews and approves continuation OR suggests changes

### CC → PM (Completion)
1. CC completes full implementation
2. CC creates final session log
3. CC reports results to user
4. User notifies PM of completion
5. PM proceeds to VALIDATE phase

---

## Implementation Outputs

- [ ] Code changes implemented
- [ ] Tests written (as per plan)
- [ ] Session logs at checkpoints
- [ ] SPRINT_TRACKER updated
- [ ] No blocking errors

### Decision Log (append after each major discussion)
- ✅ **Decision Made**: [what was agreed]
- ❓ **Open Question**: [what needs more research]
- 🚫 **Rejected**: [what was dropped and why]
- 📌 **Action Item**: [what happens next]
- ⚠️ **Risk Flagged**: [new risks identified]

---

## Success Criteria

✅ **Proceed to VALIDATE when**:
- Implementation matches plan
- Code follows project conventions
- Basic functionality works
- **Session log created**
- No blockers (minor issues acceptable)

❌ **DON'T proceed if**:
- Major deviation from plan
- Blocking errors exist
- Session log not created
- No tests written

---

## Quick Commands

### Update Tracking
```bash
# Mark task in progress
# Update TODO_NOW.md: [ ] → [/]

# Update sprint tracker
# Feature Lifecycle: "Planning" → "In Progress"
```

### Create Session Log
```bash
# Copy template
cp app/backend/.project/prompts/templates/SESSION_LOG_ENHANCED.template.md \
   app/backend/.project/history/sessions/weekN/[feature]-checkpoint-1.md

# Edit and fill in
```

---

**Next**: [Phase 6: VALIDATE](file://.agent/workflows/validate.md)  
**Previous**: [Phase 4: APPROVE](file://.agent/workflows/approve.md)  
**Back**: [Master Workflow](file://.agent/workflows/rrpai.md)
