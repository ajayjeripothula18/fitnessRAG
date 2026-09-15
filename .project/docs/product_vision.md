# Product Vision: AI-Powered Fitness & Nutrition Guidance Platform

## Overview
The system is an **AI-powered Fitness & Nutrition Guidance Platform** intended for general adults seeking non-clinical guidance on exercise, fitness, nutrition, and healthy lifestyle planning. The primary user experience is a **conversation-first fitness assistant** with structured fitness features built around it.

This is a portfolio project designed to demonstrate realistic production-style architecture and engineering depth—including RAG, LLM orchestration, backend architecture, data modeling, security, evaluation, observability, and deployment.

## Core Capabilities
- **Conversation-First Assistant**: Users interact naturally with an AI coach that leverages context (profile, active plan, history, RAG) for personalized advice.
- **Fitness & Nutrition Q&A**: Backed by a curated, evidence-based knowledge base (RAG) providing source attribution.
- **Personalized Workout Plans**: Hybrid RAG + LLM + deterministic validation for plan generation, not just an LLM writing text.
- **Predefined/Curated Plans**: Available for users to browse and personalize.
- **Dynamic Plan Modification**: Users can adjust plans interactively (e.g., "I only have 20 minutes today").
- **Progress Tracking**: Manual logging for workouts, weight, measurements, and subjective feedback.
- **Nutrition Guidance**: Macro/food recommendations (not full meal generation).
- **Body Composition Calculators**: Deterministic, anthropometry-based estimations with clear non-clinical disclaimers and historical trend tracking.

## User Experience Architecture
The platform is an application with a conversational AI assistant embedded at its core.

### Dashboard / Menu
- **AI Coach (Primary Interface)**
- Dashboard
- My Plan
- Progress
- Body Composition
- Nutrition
- Exercise/Plan Library
- Profile & Settings

## Platform Scope & Safety Boundaries
The system is intended as a **general wellness product, not a medical/clinical system**.

**In Scope:**
- General fitness and nutrition education.
- General supplement education (no personalized dosing or disease-treatment claims).

**Out of Scope (Blocked by Safety Gateway):**
- Diagnosis of medical conditions.
- Disease-specific treatment plans.
- Medication advice or prescriptions.
- Rehabilitation prescriptions.
- High-risk cases (eating disorders, extreme weight loss, emergency symptoms).

*Safety enforcement runs before normal RAG generation to appropriately handle or escalate unsafe requests.*

## Architectural Tenets
1. **Hybrid Planning Engine**: Curated templates + RAG (for evidence) + deterministic planning/validation + LLM (for reasoning, personalization, and interaction).
2. **Structured Domain Objects**: Generated plans are stored as structured domain objects (e.g., JSON representation of Goal, Schedule, Exercises, Sets/Reps) rather than raw LLM text.
3. **Structured Context**: User profile, preferences, active plan, and progress history are authoritative state stored in a database, distinct from unstructured chat history.
4. **Curated RAG Knowledge**: The RAG corpus is a curated hierarchy (Tier 1: Guidelines -> Tier 2: Peer-reviewed research -> Tier 3: Curated knowledge) providing traceable provenance for answers.
5. **Mobile-First Web/PWA**: The initial client is a mobile-first Progressive Web App (PWA) with backend APIs, keeping the architecture ready for native iOS/Android apps later.

## Development Methodology
- **Agile Methodology**: Incremental implementation and expansion.
- **Focus**: Realistic MVP that demonstrates advanced AI engineering skills without unnecessary enterprise complexity.
