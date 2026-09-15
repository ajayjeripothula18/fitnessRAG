# FitnessRAG — Product Backlog
## Created by Karan (BA/Scrum Master) & Priya (CPO)
## Last Updated: 2026-08-31

> **Prioritization Method**: MoSCoW + Value/Effort Quadrant
> **Estimation**: Story Points (Fibonacci: 1, 2, 3, 5, 8, 13)
> **Sprint Cadence**: 1-week sprints

---

## Epic 1: Authentication & User Management
**Epic Owner**: Meera (Backend) + Zara (Frontend)
**Business Value**: Foundation — cannot use the app without auth

| ID | User Story | Priority | SP | Sprint | Acceptance Criteria |
|----|-----------|----------|-----|--------|---------------------|
| US-101 | As a new user, I want to sign up with email/password so that I can create an account | Must Have | 3 | S1 | • Valid email format required (RFC 5322) • Password ≥8 chars with 1 upper, 1 lower, 1 digit, 1 special • Confirmation email sent • User record created with `is_verified=false` • Duplicate email returns 409 |
| US-102 | As a user, I want to log in with my credentials so that I can access my personalized data | Must Have | 2 | S1 | • Valid credentials return JWT access + refresh tokens • Access token TTL = 15min, refresh = 7 days • Invalid credentials return 401 • Account locked after 5 failed attempts (locked_until set) • Login timestamp updated |
| US-103 | As a user, I want to sign in with Google OAuth so that I can quickly access my account | Should Have | 5 | S2 | • Google OAuth2 flow redirects and returns • New Google users get account created + redirected to profile completion • Existing Google users logged in directly • Error handling for failed OAuth flow |
| US-104 | As a user, I want to view and edit my profile so that I can keep my fitness information current | Must Have | 3 | S1 | • All profile fields visible and editable • Validation on fields (age_range format, enum values, numeric ranges) • Changes saved with `updated_at` timestamp • Confirmation feedback after save |
| US-105 | As a user, I want to log out so that my account is secure on shared devices | Must Have | 1 | S1 | • Refresh token invalidated on server • Client clears stored tokens • User redirected to login page |
| US-106 | As a user, I want to reset my forgotten password so that I can regain access | Should Have | 3 | S2 | • Reset request generates token (SHA-256 hashed, 1hr TTL) • Email sent with reset link • New password validated against strength rules • Token invalidated after use • Old sessions invalidated |

**Epic Total**: 17 SP

---

## Epic 2: Conversational AI Coach
**Epic Owner**: Ravi (Tech Lead) + Meera (Backend)
**Business Value**: Core differentiator — primary user interaction

| ID | User Story | Priority | SP | Sprint | Acceptance Criteria |
|----|-----------|----------|-----|--------|---------------------|
| US-201 | As a user, I want to ask fitness/nutrition questions so that I can get reliable guidance | Must Have | 8 | S1 | • Questions processed within 5 seconds (p95) • Responses include source citations when from knowledge base • Safety gateway filters medical/harmful content • Conversational tone maintained • Responses are context-aware (user profile data informs answers) |
| US-202 | As a user, I want my conversations to persist so that I can continue discussions later | Must Have | 3 | S1 | • Conversation history stored with thread_id • Previous messages loaded on conversation resume • Conversations listed by recency • Maximum context window managed (sliding window) |
| US-203 | As a user, I want the AI to remember my preferences so that responses are personalized | Should Have | 5 | S2 | • User memory (explicit "remember that...") stored separately • Memory recalled in context for future responses • User can view/delete stored memories • Memory distinct from profile data |
| US-204 | As a user, I want to create a personalized workout plan through chat so that I have a routine to follow | Must Have | 8 | S2 | • Plan generated based on profile (goals, equipment, schedule, fitness level) • Plan includes warm-up, main workout, cool-down • Exercises match available equipment • Plan stored as structured data (not just text) • User can name and save the plan |
| US-205 | As a user, I want to modify my workout for today through chat so that I can adapt to circumstances | Should Have | 5 | S2 | • Can request adjustments (duration, equipment, intensity) • Modified workout still aligns with overall goals • Changes apply only to today (session) unless user specifies permanent • Original plan preserved with version history |
| US-206 | As a user, I want to log my workout completion through chat so that tracking feels natural | Should Have | 3 | S2 | • Can report sets, reps, weight via conversation • AI confirms logged data and provides encouragement • Data stored in workout_logs table • Supports "I did 3 sets of 10 bench press at 60kg" natural language |

**Epic Total**: 32 SP

---

## Epic 3: Safety Gateway
**Epic Owner**: Meera (Backend) + Vikram (QA)
**Business Value**: Non-negotiable — responsible AI, portfolio differentiator

| ID | User Story | Priority | SP | Sprint | Acceptance Criteria |
|----|-----------|----------|-----|--------|---------------------|
| US-301 | As the system, I want to classify user inputs for safety before LLM processing so that harmful/medical advice is prevented | Must Have | 5 | S1 | • Rule-based detection of medical keywords and patterns • Toxicity scoring (Detoxify library) • Classification: SAFE / MEDICAL / HARMFUL / OUT_OF_SCOPE • Processing latency < 200ms (p95) • All decisions audit-logged |
| US-302 | As a user who asks about medical conditions, I want to receive a clear disclaimer and professional referral so that I'm not harmed by incorrect advice | Must Have | 3 | S1 | • Medical queries receive standard disclaimer text • Response includes "consult a healthcare professional" • Educational information still provided where safe • Response logged with safety_category = MEDICAL |
| US-303 | As the system, I want to validate LLM outputs before delivery so that generated content meets safety standards | Must Have | 3 | S1 | • Post-processing safety scan on all LLM responses • Check for unintended medical advice in generated text • Verify exercise recommendations match user profile constraints • Flag and filter contraindicated exercises |
| US-304 | As an administrator, I want to review safety audit logs so that I can monitor and improve the safety system | Could Have | 2 | S2 | • Safety decisions logged with timestamp, input hash, category, confidence • Logs queryable by category and date range • False positive/negative tracking enabled • Basic dashboard or log export |

**Epic Total**: 13 SP

---

## Epic 4: Plan Generation & Management
**Epic Owner**: Meera (Backend) + Ravi (Tech Lead)
**Business Value**: High — structured output demonstrates AI + engineering skills

| ID | User Story | Priority | SP | Sprint | Acceptance Criteria |
|----|-----------|----------|-----|--------|---------------------|
| US-401 | As a user, I want to browse curated workout plan templates so that I can start with proven routines | Must Have | 3 | S2 | • Template library with 5-10 curated plans • Plans categorized by goal, difficulty, equipment • Template details viewable before selection • Templates stored as `is_template=true` plans |
| US-402 | As a user, I want a personalized plan generated from my profile so that it fits my specific needs | Must Have | 5 | S2 | • Plan generated using profile data (goal, equipment, days_per_week, session_duration) • Plan includes weekly structure with day-by-day exercises • Each exercise includes sets, reps, rest periods • Plan stored with version 1 in plan_versions |
| US-403 | As a user, I want to view my active plan in a structured format so that I know what to do each day | Must Have | 3 | S2 | • Plan displayed as day-by-day breakdown • Each day shows exercises with details (sets, reps, weight, rest) • Current day highlighted • Plan navigable by day/week |
| US-404 | As a user, I want plan modifications to be versioned so that I can see what changed and rollback if needed | Should Have | 3 | S2 | • Each modification creates new plan_version record • Version history accessible with change_reason • Can compare versions (diff view) • Can rollback to previous version |

**Epic Total**: 14 SP

---

## Epic 5: Progress Tracking & Body Composition
**Epic Owner**: Meera (Backend) + Zara (Frontend)
**Business Value**: Medium-High — demonstrates data visualization and time-series handling

| ID | User Story | Priority | SP | Sprint | Acceptance Criteria |
|----|-----------|----------|-----|--------|---------------------|
| US-501 | As a user, I want to record body measurements so that I can track physical changes over time | Must Have | 3 | S2 | • Can record weight, waist, neck, hip measurements • Measurements stored with date • Validation prevents unrealistic values (database constraints) • Confirmation after successful log |
| US-502 | As a user, I want to calculate my body composition estimate so that I understand my current state | Must Have | 3 | S2 | • Uses Navy method formula (height, weight, waist, neck, hip, age, sex) • Clear disclaimer: "Estimate only, not clinical measurement" • Result stored in body_measurements table (body_fat_estimate, fat_mass_kg, lean_mass_kg, bmi) • Historical estimates viewable |
| US-503 | As a user, I want to view my progress trends so that I can see improvement over time | Should Have | 5 | S2 | • Weight chart shows trend over time (line chart) • Body fat % trend visible • Workout frequency bar chart (per week/month) • Can filter by time period (1w, 1m, 3m, 6m, all) |
| US-504 | As a user, I want to see workout statistics so that I understand my training patterns | Could Have | 3 | S2 | • Total workouts per week/month • Exercise distribution by muscle group/movement pattern • Volume trends (sets × reps × weight over time) • Completion rate percentage |

**Epic Total**: 14 SP

---

## Epic 6: Knowledge Base & RAG
**Epic Owner**: Ravi (Tech Lead) + Meera (Backend)
**Business Value**: High — demonstrates RAG architecture and responsible sourcing

| ID | User Story | Priority | SP | Sprint | Acceptance Criteria |
|----|-----------|----------|-----|--------|---------------------|
| US-601 | As the system, I want to ingest and embed fitness knowledge documents so that the AI coach has authoritative information | Must Have | 5 | S1 | • Ingestion pipeline: document → chunks → embeddings → pgvector • Chunking strategy: 512 tokens with 50-token overlap • Embedding model: BGE-small-en-v1.5 (384 dimensions) • Source provenance metadata stored (evidence_tier, source_type) • Content hash for change detection |
| US-602 | As the system, I want to perform hybrid search (vector + lexical) so that retrieval is accurate | Must Have | 5 | S1 | • Vector similarity search via pgvector (cosine distance) • Lexical search via PostgreSQL full-text search (ts_rank) • Combined scoring (Reciprocal Rank Fusion or weighted sum) • Metadata filtering before vector search • Top-k results returned with relevance scores |
| US-603 | As a user, I want to see sources for AI responses so that I can trust the information | Must Have | 2 | S1 | • Responses include source citations (title, author, URL where available) • Evidence tier indicator (Tier 1 = government/org, Tier 4 = curated educational) • "Based on" attribution clearly formatted • Sources linked in response |

**Epic Total**: 12 SP

---

## Epic 7: Frontend Shell & Navigation
**Epic Owner**: Zara (Frontend)
**Business Value**: Foundation — no UX without frontend shell

| ID | User Story | Priority | SP | Sprint | Acceptance Criteria |
|----|-----------|----------|-----|--------|---------------------|
| US-701 | As a user, I want a mobile-first PWA interface so that I can use the app on my phone at the gym | Must Have | 5 | S1 | • Responsive layout works on 375px+ screens • PWA manifest.json configured (name, icons, theme, display: standalone) • Service worker caches static assets • "Add to Home Screen" prompt works on Chrome/Safari • Bottom navigation for primary sections |
| US-702 | As a user, I want clear navigation between app sections so that I can find features easily | Must Have | 3 | S1 | • Bottom nav: Dashboard, Coach, Plans, Progress, Profile • Active section highlighted • Smooth transitions between pages • React Router with proper route guards (auth required) |
| US-703 | As a user, I want the app to be accessible so that it works with assistive technologies | Must Have | 3 | S1 | • WCAG 2.1 AA compliance for all core flows • Color contrast ≥ 4.5:1 normal text, ≥ 3:1 large text • Keyboard navigation for all interactive elements • ARIA labels on all icons and interactive components • Focus management with visible indicators |

**Epic Total**: 11 SP

---

## Backlog Summary

| Epic | Must Have SP | Should Have SP | Could Have SP | Total SP |
|------|-------------|---------------|---------------|----------|
| 1. Auth & Users | 9 | 8 | 0 | 17 |
| 2. AI Coach | 19 | 13 | 0 | 32 |
| 3. Safety Gateway | 11 | 0 | 2 | 13 |
| 4. Plan Management | 11 | 3 | 0 | 14 |
| 5. Progress & Body Comp | 6 | 5 | 3 | 14 |
| 6. Knowledge & RAG | 12 | 0 | 0 | 12 |
| 7. Frontend Shell | 11 | 0 | 0 | 11 |
| **TOTAL** | **79** | **29** | **5** | **113** |

### Sprint Allocation

| Sprint | Stories | Total SP | Goal |
|--------|---------|----------|------|
| Sprint 1 | US-101, US-102, US-104, US-105, US-201, US-202, US-301, US-302, US-303, US-601, US-602, US-603, US-701, US-702, US-703 | ~57 SP | Authenticated users can have safe, personalized fitness conversations with source-cited RAG |
| Sprint 2 | US-103, US-106, US-203, US-204, US-205, US-206, US-304, US-401, US-402, US-403, US-404, US-501, US-502, US-503, US-504 | ~56 SP | Users can create, modify, and track workout plans with progress visualization |

---

## Won't Have (This Release)
- Wearable device integration (Apple Health, Google Fit)
- Proactive coaching / notifications
- Native mobile apps (iOS/Android)
- Advanced ML-based recommendations
- Social features / community
- Multi-language support
- Personalized meal planning (guidance only in MVP)
- Admin panel (use DB tools + logs for MVP)

---

## Backlog Grooming Notes
- **Next grooming**: Before Sprint 1 starts
- **Grooming cadence**: Every 3 days (mid-sprint + end of sprint)
- **WIP Limit**: 3 stories in-progress per developer
- **Spike budget**: 10% of sprint capacity reserved for technical spikes
