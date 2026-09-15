# Implementation Prompt: Ravi (Tech Lead) - Sprint 2

## Context
Based on Sprint 2 Plan decisions:
1. Sprint 1 is complete - all checkpoints done and validated
2. Sprint 2 ("Feature Complete MVP") begins 2026-09-08
3. Focus areas: Enhanced Auth & AI Memory (Days 1-2), Plan Generation & Management (Days 2-4), Progress Tracking & Workout Logging (Days 3-5)
4. Definition of Done must be followed for all tasks
5. Session logs required at checkpoints (use SESSION_LOG_ENHANCED.template.md)

## Tasks for Ravi (Tech Lead)

### Day 1-2: Enhanced Auth & AI Memory

#### US-203: AI memory & preferences
- Design memory schema: user_id, key, value, created_at, updated_at
- Create CRUD endpoints for user memories (`/api/v1/users/{id}/memories`)
- Modify chat context injection to include user memories
- Add validation for memory keys/values (size limits, sanitization)
- Write unit tests for memory service
- Update API contracts in docs/api_contracts.md

### Day 2-4: Plan Generation & Management

#### US-401: Curated plan templates
- Create plan_templates table: id, name, description, difficulty_level, duration_weeks, exercises_json, is_active
- Create CRUD endpoints for plan templates (`/api/v1/plan-templates`)
- Seed database with initial templates (beginner, intermediate, advanced)
- Write unit tests for template service
- Update API contracts

#### US-402: AI-powered plan generation
- Design plan generation prompt template with placeholders for user profile, goals, preferences
- Create structured output schema for workout plans (Pydantic models)
- Implement plan generation service that:
  1. Takes user profile, goals, duration, equipment constraints
  2. Retrieves relevant knowledge chunks from RAG
  3. Generates prompt for LLM with structured output instructions
  4. Parses LLM response into structured plan object
  5. Validates plan against exercise constraints and safety rules
- Integrate with existing LangGraph chat system
- Create endpoint to generate plan (`/api/v1/plans/generate`)
- Write unit tests for plan generation service
- Test with various user profiles and constraints
- Update API contracts

#### US-204: Workout plan creation via chat
- Extend chat service to recognize plan creation intents
- Create handler that extracts workout goals from conversation
- Invokes plan generation service with context
- Returns formatted plan to user for approval
- Add command to save generated plan to user's active plan
- Write unit tests for chat-plan integration
- Update API contracts if needed

### Day 3-5: Progress Tracking & Workout Logging

#### US-206: Chat-based workout logging
- Extend chat service to recognize workout logging intents
- Create handler that parses natural language for:
  - Exercise names
  - Sets, reps, weight
  - Duration, distance (for cardio)
  - RPE, perceived exertion
- Map parsed data to workout log structure
- Create endpoint to log workouts (`/api/v1/users/{id}/workouts`)
- Write unit tests for workout logging parsing
- Test various formats: "3 sets of 10 push ups", "ran 5k in 25 minutes", etc.
- Update API contracts

## Verification & Testing
- Run backend tests to ensure all new endpoints work correctly
- Test AI memory storage and retrieval
- Test plan generation with various user profiles
- Test structured output parsing and validation
- Test chat integration for plan creation and workout logging
- Verify API contracts are updated
- Create session logs at end of each day using SESSION_LOG_ENHANCED.template.md
- Run full backend test suite to ensure no regressions

## Deliverables
- All code changes committed to git
- Unit tests written and passing
- API contracts updated
- Session logs created for each work session
- SPRINT_TRACKER_WEEK2.md updated with task status

## Checkpoints
- End of Day 1: AI memory foundations implemented
- End of Day 2: Plan template system ready
- End of Day 3: AI plan generation service working
- End of Day 4: Chat integration for plan creation completed
- End of Day 5: Workout logging parsing implemented