# Implementation Prompt: Priya (CPO/Product Owner) - Sprint 2

## Context
Based on Sprint 2 Plan decisions:
1. Sprint 1 is complete - all checkpoints done and validated
2. Sprint 2 ("Feature Complete MVP") begins 2026-09-08
3. Focus areas: Enhanced Auth & AI Memory (Days 1-2), Plan Generation & Management (Days 2-4), Progress Tracking & Workout Logging (Days 3-5)
4. Definition of Done must be followed for all tasks
5. Session logs required at checkpoints (use SESSION_LOG_ENHANCED.template.md)
6. Responsible for: Product vision, requirements, approvals, stakeholder communication, acceptance criteria

## Tasks for Priya (CPO/Product Owner)

### Ongoing Throughout Sprint

#### Backlog Refinement & Clarification
- Review all user stories in Sprint 2 backlog for clarity
- Ensure each story has clear acceptance criteria
- Answer questions from development team regarding requirements
- Clarify any ambiguities in user stories
- Update PRODUCT_BACKLOG.md with refined stories as needed
- Maintain backlog priority order based on business value

#### Stakeholder Communication & Updates
- Provide daily sprint summary to stakeholders
- Communicate progress against sprint goal
- Flag any blockers or risks that require attention
- Coordinate with marketing/demo preparation for sprint review
- Update stakeholders on any scope changes (should be minimal)
- Facilitate communication between team members as needed

#### Acceptance Criteria Validation
- Work with team to ensure acceptance criteria are testable
- Verify that Definition of Done is understood and followed
- Participate in informal reviews of completed work
- Confirm that completed stories meet user expectations
- Provide feedback on usability and user experience
- Ensure non-functional requirements are addressed (performance, security)

### Specific Sprint Activities

#### Day 1-2: Enhanced Auth & AI Memory Focus
- Review Google OAuth implementation for security and usability
- Verify password reset flow is user-friendly and secure
- Confirm AI memory implementation aligns with privacy expectations
- Validate safety audit log provides necessary transparency
- Ensure all auth-related stories meet INVEST criteria

#### Day 2-4: Plan Generation & Management Focus
- Review plan template variety and suitability for target users
- Validate AI plan generation produces safe, effective workouts
- Confirm plan display is clear and actionable
- Verify plan versioning provides adequate audit trail
- Ensure workout plan creation via chat is intuitive

#### Day 3-5: Progress Tracking & Workout Logging Focus
- Review body measurement UI for ease of use
- Validate body composition calculation includes proper disclaimers
- Confirm progress charts show meaningful trends
- Verify workout logging captures sufficient detail
- Ensure workout statistics provide actionable insights

#### Day 5-7: Integration, Polish & Release Focus
- Participate in integration testing scenarios
- Verify performance targets are met (<2s API response, Lighthouse ≥ 70)
- Confirm accessibility audit passes (WCAG 2.1 AA)
- Review security scan results and remediation
- Participate in final polish and bug bash
- Validate documentation is complete and accurate
- Conduct acceptance testing for MVP release criteria

### Sprint Ceremonies

#### Sprint Planning (Day 0 - 2026-09-07)
- Review Sprint 2 goal and backlog with team
- Confirm team capacity and velocity expectations
- Facilitate story selection and commitment
- Ensure sprint goal is clear and measurable
- Document any assumptions or dependencies

#### Daily Standups (Each Day)
- Attend or review async standup updates
- Identify and help resolve blockers
- Confirm progress toward sprint goal
- Note any concerns or risks raised by team
- Facilitate quick decisions when needed

#### Sprint Review (Day 7 - 2026-09-14)
- Prepare demo environment and data
- Present completed features to stakeholders
- Gather feedback on implemented functionality
- Review against original sprint goal and acceptance criteria
- Document what was completed vs. what was moved to backlog
- Celebrate team accomplishments

#### Sprint Retrospective (Day 7 - 2026-09-14)
- Facilitate retrospective discussion
- Identify what went well during sprint
- Identify areas for improvement
- Create actionable improvement items for next sprint
- Ensure retrospective is blameless and constructive
- Document retrospective outcomes

## Verification & Approval Process

### Definition of Done Validation
For each completed task, verify:
- [ ] Code is formatted and linted
- [ ] No hardcoded secrets or API keys
- [ ] Code has been peer-reviewed (via /code-review or equivalent)
- [ ] Unit tests written for new business logic
- [ ] Integration tests verify component works with database/external APIs
- [ ] `pytest` (or equivalent) passes locally with no regressions
- [ ] Test coverage for modified component is >80%
- [ ] Changes adhere to architectural boundaries
- [ ] Safety constraints respected (no medical diagnosis, non-clinical only)
- [ ] Inline code documentation (docstrings) updated
- [ ] README or specific component documentation updated if setup changed
- [ ] Checkpoint/session log created using SESSION_LOG_ENHANCED.template.md
- [ ] Feature meets all Acceptance Criteria defined in User Story
- [ ] User (Product Owner) has approved changes via /approve workflow or explicit chat confirmation

### Sprint Approval Criteria
Sprint 2 is considered complete when:
- [ ] All committed stories are moved to DONE in SPRINT_TRACKER_WEEK2.md
- [ ] Definition of Done validated for all completed stories
- [ ] Integration testing scenarios pass
- [ ] Performance targets met (API <2s, Lighthouse ≥ 70)
- [ ] Accessibility audit passes (WCAG 2.1 AA)
- [ ] Security scan shows no high/severe issues
- [ ] Documentation is complete and accurate
- [ ] Sprint review and retrospective completed
- [ ] Release preparation finished (tag v1.0.0, deployment runbook)

## Deliverables
- Updated PRODUCT_BACKLOG.md with refined stories
- Sprint review presentation and feedback document
- Sprint retrospective outcomes and action items
- Definition of Done validation checklist for each story
- Session logs for Product Owner activities
- SPRINT_TRACKER_WEEK2.md updated with final status
- Release readiness confirmation

## Checkpoints
- End of Day 1: Backlog refined, questions answered, initial progress reviewed
- End of Day 2: Mid-sprint check - validate pace and address any blockers
- End of Day 3: Review progress toward sprint goal, adjust if needed
- End of Day 4: Pre-integration check - ensure readiness for testing
- End of Day 5: Pre-review check - validate completion status
- End of Day 6: Final preparation for sprint review and retrospective
- End of Day 7: Sprint review completed, retrospective finished, release ready