# Karan (BA/Scrum Master) Research Findings

## User Story Templates and Acceptance Criteria

### User Story Format
Following the INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable):

**Template:**
```
As a [type of user],
I want [some goal] 
so that [some reason or benefit].
```

**Acceptance Criteria Format:**
- Given [some precondition]
- When [some action by the user]
- Then [some observable outcome]

### Epic: User Authentication and Profile Management
**User Stories:**
1. As a new user, I want to sign up with email/password so that I can create an account and access the application.
   - AC: Valid email format required
   - AC: Password must be at least 8 characters with complexity requirements
   - AC: Email verification sent upon signup
   - AC: Successful login after verification

2. As a user, I want to log in with my credentials so that I can access my personalized data.
   - AC: Valid credentials grant access
   - AC: Invalid credentials show error message
   - AC: Account locked after 5 failed attempts
   - AC: "Remember me" option available

3. As a user, I want to sign in with Google so that I can quickly create an account.
   - AC: Google OAuth flow works
   - AC: New users redirected to profile completion
   - AC: Existing Google users logged in directly
   - AC: Error handling for failed Google auth

4. As a user, I want to view and edit my profile so that I can keep my information up to date.
   - AC: All profile fields visible and editable
   - AC: Validation on fields (age range, numbers, etc.)
   - AC: Changes saved successfully
   - AC: Confirmation message after save

### Epic: AI Conversational Coach
**User Stories:**
1. As a user, I want to ask fitness/nutrition questions so that I can get reliable guidance.
   - AC: Questions processed within 5 seconds
   - AC: Responses include source citations when from knowledge base
   - AC: Safety checks prevent medical advice
   - AC: Conversational tone maintained

2. As a user, I want to create a personalized workout plan so that I have a routine to follow.
   - AC: Plan based on user profile (goals, equipment, schedule)
   - AC: Plan includes warm-up, main workout, cool-down
   - AC: Exercises match available equipment
   - AC: User can save and name the plan

3. As a user, I want to modify my workout for today so that I can adapt to changing circumstances.
   - AC: Can adjust duration, equipment, intensity
   - AC: Modified workout still aligns with overall goals
   - AC: Changes apply only to today unless user specifies otherwise
   - AC: Original plan preserved for future days

4. As a user, I want to log my workout completion so that I can track my progress.
   - AC: Can log sets, reps, weight for each exercise
   - AC: Can mark workout as complete/incomplete
   - AC: Optional fields for RPE, energy, soreness
   - AC: Success confirmation after logging

### Epic: Progress Tracking and Analytics
**User Stories:**
1. As a user, I want to record body measurements so that I can track physical changes over time.
   - AC: Can record weight, waist, neck, hip measurements
   - AC: Measurements stored with date
   - AC: Estimated body fat calculated and stored
   - AC: Validation prevents unrealistic values

2. As a user, I want to view my progress trends so that I can see how I'm improving.
   - AC: Weight chart shows trends over time
   - AC: Measurement trends visible
   - AC: Workout frequency visible
   - AC: Can filter by time period (week, month, 3 months)

3. As a user, I want to see workout statistics so that I understand my training patterns.
   - AC: Total workouts per week/month
   - AC: Exercise distribution (push/pull/legs, etc.)
   - AC: Volume trends (sets × reps × weight)
   - AC: Average workout duration

### Epic: Knowledge and Learning
**User Stories:**
1. As a user, I want to browse exercise library so that I can learn proper form and variations.
   - AC: Exercises searchable by name, muscle group, equipment
   - AC: Each exercise shows primary/secondary muscles
   - AC: Equipment requirements displayed
   - AC: Difficulty level indicated

2. As a user, I want to access nutrition guidance so that I can make informed dietary choices.
   - AC: Information on macronutrients, micronutrients
   - AC: General healthy eating principles
   - AC: Hydration and supplement basics
   - AC: Clear disclaimer that this is not medical advice

### Epic: Administrative and System
**User Stories:**
1. As an administrator, I want to view system metrics so that I can monitor performance.
   - AC: Dashboard shows active users, response times
   - AC: Error rates and latency metrics
   - AC: Database performance indicators
   - AC: External API call statistics

2. As a user, I want to export my data so that I have a backup or can move to another service.
   - AC: Can export profile, plans, progress data
   - AC: Export in standard format (JSON/CSV)
   - AC: Includes all user-generated content
   - AC: Excludes system/internal data

## Sprint Planning Framework for 1-2 Week Timeline

### Sprint Structure (Assuming 2 One-Week Sprints)
**Sprint 1: Foundation and Core MVP**
- Goal: Implement walking skeleton with auth, basic chat, and profile
- Team Capacity: 2 developers (backend/frontend focus)
- Key Activities:
  - Day 1: Project setup, repo creation, basic CI/CD
  - Day 2: Authentication system (signup/login)
  - Day 3: User profile management
  - Day 4: Basic chat interface with LLM integration
  - Day 5: Safety gateway implementation
  - Day 6: Integration and testing
  - Day 7: Review, retrospective, prep for Sprint 2

**Sprint 2: Feature Enhancement and Polish**
- Goal: Add workout planning, progress tracking, and refine UX
- Team Capacity: 2 developers
- Key Activities:
  - Day 1: Exercise library and basic plan templates
  - Day 2: Personalized plan generation
  - Day 3: Plan modification functionality
  - Day 4: Progress tracking and measurement logging
  - Day 5: Body-fat calculator implementation
  - Day 6: UI/UX improvements and responsiveness
  - Day 7: Testing, bug fixing, demo preparation

### Definition of Done (DoD)
A story is considered Done when:
1. **Code Complete**: All functionality implemented per acceptance criteria
2. **Code Reviewed**: At least one team member has reviewed and approved
3. **Tested**: 
   - Unit tests written and passing (minimum 70% coverage for new code)
   - Integration tests for API endpoints
   - Manual testing completed
4. **Documented**: 
   - Code comments where necessary
   - API endpoints documented in OpenAPI/Swagger
   - User-facing documentation if needed
5. **Integrated**: 
   - Code merged to main branch
   - Deployed to staging environment
   - No merge conflicts
6. **Demoable**: 
   - Can be demonstrated to stakeholders
   - Meets Definition of Ready for next sprint if applicable
7. **Clean**: 
   - No new technical debt introduced intentionally
   - Any debt taken on is tracked and planned for repayment
8. **Accepted**: 
   - Product Owner has accepted the story
   - Stakeholder feedback incorporated if requested

### Sprint Planning Process
1. **Pre-Planning (Before Sprint Start)**:
   - Product Owner refines and prioritizes backlog
   - Team estimates stories during backlog refinement
   - Capacity planning based on team availability
   
2. **Sprint Planning Meeting**:
   - Review sprint goal and objective
   - Select stories from backlog that fit capacity
   - Break stories into tasks if needed
   - Assign story points based on effort estimation
   - Confirm Definition of Done understanding
   
3. **During Sprint**:
   - Daily standups (15 minutes max)
   - Track progress on task board (To Do, In Progress, Done)
   - Update remaining effort estimates
   - Identify and address blockers immediately
   
4. **Sprint Review**:
   - Demonstrate completed work to stakeholders
   - Collect feedback
   - Review what was done vs. what was planned
   - Adjust backlog based on feedback
   
5. **Sprint Retrospective**:
   - What went well?
   - What could be improved?
   - Action items for next sprint
   - Process improvement commitments

### Backlog Prioritization Framework (MoSCoW + Value/Effort)
**MoSCoW Method**:
- **Must Have**: Essential for MVP to provide value
- **Should Have**: Important but not critical for initial launch
- **Could Have**: Nice to have, optional enhancements
- **Won't Have (this time)**: Explicitly excluded from current scope

**Value vs. Effort Quadrant**:
- **High Value, Low Effort**: Quick wins - prioritize first
- **High Value, High Effort**: Major features - schedule carefully
- **Low Value, Low Effort**: Fill-in work - do when capacity allows
- **Low Value, High Effort**: Avoid or reconsider

### Estimation Techniques
1. **Story Points** (Fibonacci-like sequence: 1, 2, 3, 5, 8, 13):
   - 1: Trivial, minimal effort
   - 2: Small, well-understood task
   - 3: Medium effort, some uncertainty
   - 5: Larger effort, notable uncertainty
   - 8: Significant effort, requires research/spiking
   - 13: Epic, needs to be broken down
   
2. **Planning Poker** for team estimation
3. **T-Shirt Sizing** (XS, S, M, L, XL) for initial high-level estimates
4. **Ideal Time** estimation for very well-understood tasks
5. **Affinity Estimation** for grouping similar-sized stories

### Risk Management in Sprints
1. **Identify Risks Early**: During backlog refinement and planning
2. **Risk Categories**:
   - Technical (unknown tech, integration complexity)
   - Dependencies (external APIs, team availability)
   - Requirements (unclear or changing needs)
   - Environmental (infrastructure, tooling issues)
3. **Mitigation Strategies**:
   - Spike solutions for technical uncertainties
   - Buffer time for known dependencies
   - Regular clarification sessions for requirements
   - Redundancy planning for critical paths
4. **Burndown Charts**: Track progress and identify slowing trends
5. **Velocity Tracking**: Measure completed story points per sprint for forecasting

## Definition of Done (DoD) and Retrospective Formats

### Comprehensive Definition of Done Checklist

#### Coding Standards
- [ ] Code follows team-agreed style guide (PEP 8 for Python, ESLint for JS)
- [ ] No TODO/FIXME comments left in code (except with tracking ticket)
- [ ] Meaningful variable and function names
- [ ] Functions are appropriately sized (<50 lines preferred)
- [ ] Proper error handling and logging
- [ ] Security best practices implemented (input validation, etc.)
- [ ] Performance considerations (no obvious N+1 queries, etc.)
- [ ] Dependencies are justified and licensed appropriately

#### Testing
- [ ] Unit tests written for new functionality
- [ ] Unit tests passing locally and in CI
- [ ] Integration tests for API endpoints/workflows
- [ ] Manual testing completed per acceptance criteria
- [ ] Test coverage meets minimum threshold (70% for new code)
- [ ] Tests are maintainable and not overly brittle
- [ ] Edge cases considered and tested
- [ ] Security testing performed (where applicable)

#### Documentation
- [ ] Code commented where intent is not obvious
- [ ] Public APIs documented (docstrings, OpenAPI/Swagger)
- [ ] Architecture decisions recorded (ADRs if used)
- [ ] Database schema changes documented
- [ ] User-facing documentation updated if needed
- [ ] Deployment/configuration instructions updated
- [ ] Testing instructions included if non-standard

#### Integration and Deployment
- [ ] Code merges cleanly to main branch
- [ ] No merge conflicts
- [ ] Builds successfully in CI/CD pipeline
- [ ] Deploys to staging environment without errors
- [ ] Health checks pass after deployment
- [ ] Rollback procedure tested/documented
- [ ] Database migrations run successfully (if applicable)
- [ ] Environment variables/configuration validated

#### Quality and Non-Functional Requirements
- [ ] Accessibility considerations reviewed (WCAG AA where applicable)
- [ ] Responsive design verified (mobile, tablet, desktop)
- [ ] Browser compatibility checked (if web app)
- [ ] Performance benchmarks met (page load <3s, API <2s)
- [ ] Security scans pass (no critical/vulnerabilities)
- [ ] Legal/compliance requirements met (privacy, terms)
- [ ] Internationalization/i18n readiness (if applicable)
- [ ] Observability (logging, metrics, tracing) implemented

#### Acceptance and Review
- [ ] All acceptance criteria met
- [ ] Product Owner has reviewed and accepted
- [ ] Stakeholder demo completed (if applicable)
- [ ] Feedback incorporated from review
- [ ] Definition of Done understood by entire team
- [ ] Retrospective actions from previous sprint considered

#### Team and Process
- [ ] Work is properly tracked in task board
- [ ] Time spent recorded (if time tracking used)
- [ ] Knowledge shared with team (if applicable)
- [ ] Any technical debt incurred is tracked and visible
- [ ] Process followed (standups, reviews, etc.)
- [ ] Estimates updated based on actual effort

### Retrospective Formats

#### 1. Start-Stop-Continue
- **Start**: What should we start doing?
- **Stop**: What should we stop doing?
- **Continue**: What should we continue doing?
- **Benefits**: Simple, quick, good for new teams
- **Timebox**: 15-20 minutes

#### 2. Mad-Sad-Glad
- **Mad**: What made us angry or frustrated?
- **Sad**: What disappointed us or let us down?
- **Glad**: What made us happy or satisfied?
- **Benefits**: Focuses on emotions and team morale
- **Timebox**: 20-30 minutes

#### 3. 4Ls (Liked, Learned, Lacked, Longed For)
- **Liked**: What did we like about the sprint?
- **Learned**: What did we learn?
- **Lacked**: What did we lack or wish we had more of?
- **Longed For**: What do we want in the next sprint?
- **Benefits**: Balanced positive/negative, forward-looking
- **Timebox**: 20-30 minutes

#### 5. Sailboat Retrospective
- **Wind**: What helped us move forward?
- **Anchor**: What held us back?
- **Rocks**: What risks did we see?
- **Island**: What is our goal/destination?
- **Benefits**: Visual, good for strategic thinking
- **Timebox**: 25-35 minutes

#### 6. Starfish Retrospective
- **Keep Doing**: What should we keep doing?
- **Less Of**: What should we do less of?
- **More Of**: What should we do more of?
- **Stop Doing**: What should we stop doing?
- **Start Doing**: What should we start doing?
- **Benefits**: More detailed than Start-Stop-Continue
- **Timebox**: 20-30 minutes

#### 7. Timeline Retrospective
- **Create timeline** of sprint events
- **Add emotions** (positive/negative) to timeline points
- **Discuss patterns** and insights
- **Benefits**: Good for understanding sprint flow and events
- **Timebox**: 30-45 minutes (better for longer sprints)

#### 8. Appreciation Retrospective
- **Focus on team appreciation** and recognition
- **Each person shares** what they appreciate about others
- **Builds team cohesion** and positive culture
- **Benefits**: Great for team building, especially after tough sprints
- **Timebox**: 15-20 minutes

### Retrospective Best Practices
1. **Psychological Safety**: Ensure everyone feels safe to speak honestly
2. **Action-Oriented**: End with clear, actionable improvement items
3. **Follow-Up**: Review action items from previous retrospective
4. **Timeboxed**: Keep to agreed time limit to respect everyone's time
5. **Facilitated**: Have a neutral facilitator (can rotate)
6. **Visible**: Make action items visible and track progress
7. **Varied Formats**: Rotate formats to keep fresh and address different aspects
8. **Inclusive**: Ensure all voices are heard, not just loudest
9. **Focus on Process**: Focus on how we work, not just what we worked on
10. **Celebrate Successes**: Recognize what went well, not just problems

### Continuous Improvement Tracking
1. **Action Item Board**: Track retrospective action items
2. **Metrics**: Measure improvement over time (cycle time, defect rate, etc.)
3. **Experiments**: Treat improvements as experiments with hypotheses
4. **Review Cadence**: Review action items every sprint
5. **Escalation**: Bring systemic issues to appropriate leadership
6. **Celebration**: Recognize when improvements are achieved
7. **Documentation**: Keep record of what was tried and results
8. **Sharing**: Share learnings with other teams if applicable
9. **Adaptation**: Be willing to abandon changes that don't work
10. **Scrum of Scrums**: For multiple teams, coordinate improvements

## Key Recommendations for MVP Implementation

### User Story Management
1. Start with epics broken into small, valuable user stories
2. Use INVEST criteria to refine stories
3. Write acceptance criteria in Given/When/Then format
4. Estimate stories as a team using Planning Poker
5. Prioritize backlog using MoSCoW and Value/Effort quadrants
6. Keep backlog groomed and refined regularly
7. Limit work in progress (WIP) to improve flow
8. Review and update estimates as needed
9. Split stories that are too large (>8 points)
10. Spike uncertain technical approaches before committing to implementation

### Sprint Execution
1. Use 1-week sprints for rapid feedback and adjustment
2. Maintain consistent sprint rhythm (same start/end days)
3. Protect the sprint goal from scope changes mid-sprint
4. Daily standups: 15 minutes, same time/place, focused on progress
5. Visual task board (physical or digital) for transparency
6. Sprint review: Demonstrate working software, collect feedback
7. Sprint retrospective: Focus on process improvements, not blame
8. Track velocity for forecasting but don't punish variation
9. Adjust sprint length/process based on team feedback
10. Celebrate sprint successes and learning

### Definition of Done Application
1. Define DoD collaboratively and get team agreement
2. Make DoD visible and reference it regularly
3. Apply DoD consistently to all stories
4. Update DoD as team learns and improves
5. Use DoD as checklist during sprint review
6. Don't consider story done until all DoD items are checked
7. Be realistic about what can be achieved in MVP timeframe
8. Prioritize completeness over perfection for MVP
9. Document any intentional exceptions to DoD
10. Use DoD to build quality culture and shared understanding

### Retrospective Implementation
1. Schedule retrospectives at same time each sprint
2. Rotate facilitator role to build facilitation skills
3. Start with simple formats (Start-Stop-Continue) for new team
4. Focus on actionable improvements, not just discussion
5. Limit to 2-3 improvement actions per sprint maximum
6. Track action item completion in next sprint
7. Celebrate when improvements are implemented successfully
8. Be honest about what's not working and why
9. Protect retrospective time as sacred for team improvement
10. Use retrospectives to build team cohesion and trust

### Scaling for MVP Constraints
1. **For 1-2 Week Timeline**:
   - Focus on Minimum Marketable Features (MMF)
   - Accept technical debt where it doesn't jeopardize core value
   - Prioritize learning and feedback over completeness
   - Use spike and validate approach for risky decisions
   
2. **For Limited Team Size**:
   - Limit WIP to prevent context switching
   - Pair program on complex or critical components
   - Swarm on blockers to resolve quickly
   - Cross-train to reduce single points of failure
   
3. **For Zero Budget**:
   - Leverage free tiers and open source tools
   - Accept limited functionality in exchange for cost savings
   - Invest time in learning free tools rather than money
   - Plan for eventual migration if free limits exceeded
   
4. **For Portfolio/Project Goals**:
   - Prioritize features that demonstrate architectural thinking
   - Include observable quality practices (testing, CI/CD, etc.)
   - Design for extensibility even if not implementing all features
   - Document decisions and tradeoffs for future reference
   - Focus on clean, maintainable code over rapid hacking

### Communication and Transparency
1. Keep stakeholders informed with regular demos
2. Use information radiators (task board, burn-down charts)
3. Share metrics transparently (velocity, defect rates, etc.)
4. Document decisions and rationale for future reference
5. Encourage open communication and psychological safety
6. Hold regular 1:1s to check in on team members
7. Share both successes and failures for learning
8. Make work visible to build trust and accountability
9. Use asynchronous communication effectively for distributed work
10. Respect time zones and working hours if team distributed

### Final Recommendations for FitnessRAG MVP
1. **Sprint 1 Focus**: Authentication, profile management, basic chat with safety
2. **Sprint 2 Focus**: Workout planning, progress tracking, body-fat calculator
3. **DoD Emphasis**: Testing, security, accessibility, documentation
4. **Retrospective Cadence**: End of each sprint with clear action items
5. **Communication**: Daily standups, sprint reviews, demos for stakeholders
6. **Quality Over Speed**: Build maintainable foundation for future enhancement
7. **Learning Mindset**: Treat each sprint as experiment to validate assumptions
8. **Technical Excellence**: Implement good practices from day one (CI, testing, etc.)
9. **User-Centered**: Keep founder's personal use case central to decisions
10. **Documentation**: Capture architecture decisions, research findings, lessons learned