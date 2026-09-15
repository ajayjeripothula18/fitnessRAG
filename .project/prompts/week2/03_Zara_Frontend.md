# Implementation Prompt: Zara (Frontend Lead) - Sprint 2

## Context
Based on Sprint 2 Plan decisions:
1. Sprint 1 is complete - all checkpoints done and validated
2. Sprint 2 ("Feature Complete MVP") begins 2026-09-08
3. Focus areas: Enhanced Auth & AI Memory (Days 1-2), Plan Generation & Management (Days 2-4), Progress Tracking & Workout Logging (Days 3-5)
4. Definition of Done must be followed for all tasks
5. Session logs required at checkpoints (use SESSION_LOG_ENHANCED.template.md)
6. Frontend tech stack: React 18, TypeScript, Vite, TanStack Query, Zustand, Lucide icons

## Tasks for Zara (Frontend Lead)

### Day 1-2: Enhanced Auth & AI Memory

#### US-103: Google OAuth sign-in
- Add Google Sign-In button to LoginPage
- Implement OAuth flow using auth service
- Handle Google callback and token storage
- Update authService to include Google login method
- Create GoogleOAuthButton component
- Add proper loading and error states
- Write unit tests for auth service Google methods
- Update README with Google login instructions

#### US-106: Password reset flow
- Create ForgotPasswordPage
- Create ResetPasswordPage with token validation
- Implement form validation for email and password
- Connect to authService forgot/reset methods
- Add links between login, forgot password, and reset password pages
- Write unit tests for password reset pages
- Update navigation and route protection

#### US-203: AI memory & preferences
- Create UserMemories component to view/edit memories
- Add memory management to user settings/profile
- Create memory input component with validation
- Connect to userService for memory CRUD operations
- Display memories in chat context indicator
- Write unit tests for memory components
- Update settings page to include memory management

#### US-304: Safety audit log dashboard
- Create SafetyLogTable component
- Implement pagination and filtering controls
- Connect to safetyService to fetch logs
- Display safety tier with color-coded indicators
- Show original message and action taken
- Write unit tests for safety log components
- Add safety logs link to admin/user settings

### Day 2-4: Plan Generation & Management

#### US-401: Curated plan templates
- Create PlanTemplatesList component
- Implement template browsing and filtering
- Connect to planTemplateService to fetch templates
- Display template details (name, description, difficulty, duration)
- Write unit tests for template components
- Add templates browsing to plans section

#### US-402: AI-powered plan generation
- Enhance ChatContainer to recognize plan creation requests
- Create PlanGenerationModal for user inputs (goal, duration, equipment, etc.)
- Connect to chatService to send plan generation requests
- Display generated plan in modal for approval
- Add "Save as My Plan" button
- Write unit tests for plan generation flow
- Update chat service to handle plan generation responses

#### US-403: Plan display (day-by-day view)
- Create PlanViewer component
- Implement day-by-day workout display
- Show exercises with sets, reps, weight
- Add exercise substitution UI
- Connect to planService to fetch plan details
- Create responsive layout for mobile viewing
- Write unit tests for plan viewer
- Add plan viewer to plans section

#### US-404: Plan versioning & rollback
- Create PlanVersions component
- Display version history with dates and change summaries
- Implement rollback functionality with confirmation
- Connect to planService for version operations
- Show current active version indicator
- Write unit tests for versioning components
- Add version history to plan viewer

### Day 3-5: Progress Tracking & Workout Logging

#### US-501: Body measurement recording
- Create BodyMeasurementsForm component
- Implement form with weight, waist, neck, hip fields
- Add validation for measurement ranges
- Connect to userService to save measurements
- Show last recorded measurements
- Write unit tests for measurement form
- Add to profile/settings page

#### US-502: Body composition calculator
- Create BodyCompositionDisplay component
- Implement Navy formula calculation
- Show body fat percentage with disclaimer
- Display historical body fat trend
- Connect to userService to get measurements
- Write unit tests for calculation accuracy
- Add to profile/progress section

#### US-503: Progress trend charts
- Install recharts library: `npm install recharts`
- Create ProgressCharts component
- Implement weight trend chart (line chart)
- Implement body fat percentage trend chart
- Add customizable date ranges (1mo, 3mo, 6mo, 1y)
- Connect to userService to fetch measurement history
- Write unit tests for chart components
- Add charts to progress page
- Ensure mobile-responsive chart containers

#### US-504: Workout statistics
- Create WorkoutStats component
- Calculate and display:
  - Total workouts this month
  - Average workout duration
  - Most frequent exercises
  - Volume trends (sets x reps x weight)
  - Workout streak
- Connect to workoutService to fetch statistics
- Write unit tests for stats calculations
- Add stats to progress page
- Create workout log form for manual entry

### Day 5-7: Integration, Polish & Release

#### Accessibility audit (WCAG 2.1 AA)
- Run axe-core accessibility testing
- Fix all WCAG 2.1 AA violations
- Ensure proper ARIA labels and roles
- Check color contrast ratios
- Test keyboard navigation
- Test screen reader compatibility
- Document fixes in accessibility report

#### PWA optimization (Lighthouse score ≥ 70)
- Run Lighthouse audit
- Optimize for performance:
  - Implement proper caching strategies
  - Optimize image loading
  - Minimize main-thread work
  - Reduce JavaScript bundle size
- Ensure offline functionality works
- Add manifest.json improvements
- Update service worker caching strategies
- Target Lighthouse score ≥ 70

#### Bug fixes and final polish
- Address all bugs found during integration testing
- Polish UI/UX based on feedback
- Ensure consistent spacing and typography
- Verify all responsive breakpoints
- Add loading states and empty states where needed
- Finalize all animations and transitions

## Verification & Testing
- Run frontend tests: `npm test`
- Conduct manual testing of all new features
- Verify responsive design on mobile and tablet
- Test OAuth flow with Google account
- Test password reset flow end-to-end
- Test AI memory storage and retrieval
- Test plan generation and display
- Test workout logging and statistics
- Test body measurement recording and calculation
- Test progress charts with sample data
- Conduct accessibility audit (WCAG 2.1 AA)
- Run Lighthouse and target score ≥ 70
- Create session logs at end of each day using SESSION_LOG_ENHANCED.template.md

## Deliverables
- All code changes committed to git
- Frontend tests written and passing
- Session logs created for each work session
- SPRINT_TRACKER_WEEK2.md updated with task status
- Updated documentation in README if needed

## Checkpoints
- End of Day 1: Google OAuth and Password reset UI implemented
- End of Day 2: Auth enhancements and memory UI completed
- End of Day 3: Plan templates and generation UI working
- End of Day 4: Plan display and versioning completed
- End of Day 5: Body measurement and composition UI implemented
- End of Day 6: Progress charts and workout stats completed
- End of Day 7: Accessibility audit passed, Lighthouse ≥ 70, ready for release