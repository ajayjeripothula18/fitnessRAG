# Implementation Prompt: Meera (Backend Lead) - Sprint 2

## Context
Based on Sprint 2 Plan decisions:
1. Sprint 1 is complete - all checkpoints done and validated
2. Sprint 2 ("Feature Complete MVP") begins 2026-09-08
3. Focus areas: Enhanced Auth & AI Memory (Days 1-2), Plan Generation & Management (Days 2-4), Progress Tracking & Workout Logging (Days 3-5)
4. Definition of Done must be followed for all tasks
5. Session logs required at checkpoints (use SESSION_LOG_ENHANCED.template.md)

## Tasks for Meera (Backend Lead)

### Day 1-2: Enhanced Auth & AI Memory

#### US-103: Google OAuth sign-in
- Implement Google OAuth2 flow using authlib library
- Create `/api/v1/auth/google/login` and `/api/v1/auth/google/callback` endpoints
- Update User model to store Google ID and link to existing accounts
- Ensure secure handling of OAuth tokens
- Add login button to frontend login page
- Write unit tests for OAuth flow
- Update API contracts in docs/api_contracts.md

#### US-106: Password reset flow
- Implement password reset using email tokens
- Create `/api/v1/auth/forgot-password` and `/api/v1/auth/reset-password` endpoints
- Generate secure, time-limited tokens for reset
- Update email service to send reset links
- Add forgot password link to login page
- Write unit tests for password reset flow
- Update API contracts

#### US-203: AI memory & preferences
- Design memory schema: user_id, key, value, created_at, updated_at
- Create CRUD endpoints for user memories (`/api/v1/users/{id}/memories`)
- Modify chat context injection to include user memories
- Add validation for memory keys/values (size limits, sanitization)
- Write unit tests for memory service
- Update API contracts

#### US-304: Safety audit log dashboard
- Create safety log model: id, user_id, timestamp, safety_tier, reason, original_message, action_taken
- Create endpoint to retrieve safety logs (`/api/v1/safety/logs`)
- Add pagination and filtering (by date, tier, reason)
- Ensure logs are immutable (append-only)
- Write unit tests for safety logging
- Update API contracts

### Day 2-4: Plan Generation & Management

#### US-401: Curated plan templates
- Create plan_templates table: id, name, description, difficulty_level, duration_weeks, exercises_json, is_active
- Create CRUD endpoints for plan templates (`/api/v1/plan-templates`)
- Seed database with initial templates (beginner, intermediate, advanced)
- Write unit tests for template service
- Update API contracts

#### US-404: Plan versioning & rollback
- Modify plans table: add version_number (default 1), is_active_version boolean
- When plan is modified, create new version with incremented version_number
- Create endpoint to get plan versions (`/api/v1/plans/{id}/versions`)
- Create endpoint to rollback to specific version (`/api/v1/plans/{id}/rollback/{version}`)
- Ensure only one active version per plan at a time
- Write unit tests for versioning logic
- Update API contracts

### Day 3-5: Progress Tracking & Workout Logging

#### US-501: Body measurement recording
- Create body_measurements table: id, user_id, weight, waist, neck, hip, timestamp
- Create CRUD endpoints for body measurements (`/api/v1/users/{id}/body-measurements`)
- Add validation for measurement ranges (positive values, realistic limits)
- Write unit tests for measurement service
- Update API contracts

#### US-502: Body composition calculator
- Implement Navy body fat percentage formula:
  - Men: % fat = 86.010 * log10(waist - neck) - 70.041 * log10(height) + 36.76
  - Women: % fat = 163.205 * log10(waist + hip - neck) - 97.684 * log10(height) - 78.387
- Create endpoint to calculate body composition (`/api/v1/users/{id}/body-composition`)
- Add disclaimer: "Estimate only, not clinical measurement"
- Store calculated body fat % with measurements
- Write unit tests for calculation accuracy
- Update API contracts

## Verification & Testing
- Run backend tests to ensure all new endpoints work correctly
- Test OAuth flow with actual Google credentials (use test account)
- Test password reset token generation and validation
- Test memory CRUD operations
- Test safety logging and retrieval
- Test plan template CRUD and seeding
- Test plan versioning and rollback functionality
- Test body measurement validation and storage
- Test body composition calculation accuracy
- Verify API contracts are updated
- Create session logs at end of each day using SESSION_LOG_ENHANCED.template.md

## Deliverables
- All code changes committed to git
- Unit tests written and passing
- API contracts updated
- Session logs created for each work session
- SPRINT_TRACKER_WEEK2.md updated with task status

## Checkpoints
- End of Day 1: Google OAuth and Password reset implemented
- End of Day 2: AI memory and Safety audit log implemented
- End of Day 3: Plan templates and Versioning implemented
- End of Day 4: Plan generation core completed
- End of Day 5: Body measurement and composition implemented