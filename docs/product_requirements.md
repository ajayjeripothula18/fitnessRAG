# FitnessRAG Product Requirements Document (PRD)
# Created by Priya (CPO)

## Vision
An AI-powered Fitness & Nutrition Guidance Platform for general adults seeking non-clinical guidance on exercise, fitness, nutrition, and healthy lifestyle planning.

## Target Users
- General adults (18-65) seeking non-clinical fitness and nutrition guidance
- Primary use case: Founder's personal use and demonstration to friends/family
- Tech-savviness: Variable - must be user-friendly and easy to operate, should be able to use it on mobile and tablet devices, should be able to use it on mobile and tablet devices

## Core Features (MVP - P0)

### 1. Authentication & Profile Management
- Email/password signup and login
- Google sign-in (OAuth2)
- Profile management with fitness/nutrition personalization fields:
  * Age range, sex, height, weight
  * Fitness level, primary goal (lose weight, gain muscle, improve stamina, etc)
  * Fitness background (beginner, intermediate, advanced)
  * Fitness frequency (how many days a week)
  * Fitness equipment (gym, home, bodyweight, etc)
  * Dietary preferences, allergies
  * Available equipment, workout location
  * Schedule constraints, food dislikes

### 2. Conversational AI Coach (Primary Interface)
- Chat-based interaction as main user interaction
- Safety gateway to prevent medical advice, harmful content
- Context-aware responses using:
  * User profile
  * Conversation history (short-term)
  * User memory (explicit preferences)
  * Active plan and progress data
  * Retrieved knowledge from RAG
- Ability to:
  * Answer fitness/nutrition questions
  * Create workout plans
  * Modify existing plans
  * Log workouts and progress
  * Calculate body composition estimates
  * Manage user memory ("remember that...")

### 3. Plan Generation & Management
- Curated workout plan templates
- Personalized plan generation based on user profile
- Plan modification through conversation (temporary/session changes)
- Persistent plan changes requiring explicit approval
- Plan versioning for auditability and rollback

### 4. Progress Tracking
- Manual logging of:
  * Workout completion (sets, reps, weight)
  * Workout streak
  * Body measurements (weight, waist, neck, hip)
  * Subjective feedback (RPE, energy, soreness, enjoyment)
  * Estimated body fat % (via calculator)
- Progress visualization over time

### 5. Body Composition Calculator
- Deterministic estimator using anthropometric measurements
- Inputs: height, weight, age, sex, waist, neck, hip (where applicable)
- Clear disclaimer: estimate only, not clinical measurement
- Historical tracking for trend analysis

### 6. Knowledge & Source Attribution
- RAG-based responses with source citations
- Knowledge hierarchy: gov/orgs → professional orgs → peer-reviewed → curated educational
- Source provenance metadata for transparency

### 7. Safety Gateway
- Pre-processing safety classification
- Detection of medical advice requests, harmful content
- Appropriate responses: disclaimer, redirection, educational response
- Audit logging of safety decisions

## Non-Featured (P1/P2 - Future)
- Wearable device integration (Apple Health, Google Fit)
- Proactive coaching/notifications
- Native mobile apps (iOS/Android)
- Advanced analytics and recommendations
- Social features and community
- Expanded knowledge base and languages

## User Stories (Prioritized)

### Authentication Epic
1. As a new user, I want to sign up with email/password so that I can create an account.
2. As a user, I want to log in with my credentials so that I can access my personalized data.
3. As a user, I want to sign in with Google so that I can quickly create/access my account.
4. As a user, I want to view and edit my profile so that I can keep my information current.

### Conversational Coach Epic
5. As a user, I want to ask fitness/nutrition questions so that I can get reliable guidance.
6. As a user, I want to create a personalized workout plan so that I have a routine to follow.
7. As a user, I want to modify my workout for today so that I can adapt to changing circumstances.
8. As a user, I want to log my workout completion so that I can track my progress.
9. As a user, I want to calculate my body composition estimate so that I can track physical changes.

### Progress Tracking Epic
10. As a user, I want to record body measurements so that I can track physical changes over time.
11. As a user, I want to view my progress trends so that I can see how I'm improving.
12. As a user, I want to see workout statistics so that I understand my training patterns.

## Acceptance Criteria Template
For each user story, acceptance criteria will follow:
- Given [precondition]
- When [action]
- Then [observable outcome]

## MVP Scope Boundaries
**In Scope:**
- Conversational AI coach with safety controls
- User profile management and authentication
- Basic workout plan generation and modification
- Manual progress tracking and logging
- Body composition estimation calculator
- Source-attributed Q&A responses
- Mobile-first PWA interface

**Out of Scope for MVP:**
- Medical/clinical advice or diagnosis
- Personalized meal planning (guidance only)
- Wearable/device integration
- Proactive notifications
- Native mobile apps
- Multi-language support
- Advanced machine learning recommendations