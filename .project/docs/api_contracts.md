# FitnessRAG — API Contracts
## Created by Meera (Senior Backend Engineer) & Ravi (Tech Lead)
## Last Updated: 2026-08-31

> **Base URL**: `http://localhost:8000/api/v1`
> **Format**: JSON (application/json)
> **Auth**: Bearer JWT token (unless marked as Public)
> **API Documentation**: Auto-generated at `/docs` (Swagger) and `/redoc` (ReDoc) via FastAPI

---

## 1. Authentication Endpoints

### POST `/auth/register` — Public
Create a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecureP@ss1",
  "full_name": "Ajay Kumar"
}
```

**Validation Rules:**
- `email`: Valid RFC 5322 format, unique (case-insensitive)
- `password`: Min 8 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char
- `full_name`: 2-100 chars, no special characters except spaces, hyphens, apostrophes

**Response: 201 Created**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "full_name": "Ajay Kumar",
  "is_verified": false,
  "created_at": "2026-09-01T10:30:00Z"
}
```

**Error Responses:**
| Status | Code | Message |
|--------|------|---------|
| 400 | `VALIDATION_ERROR` | Validation details in `errors` array |
| 409 | `EMAIL_EXISTS` | An account with this email already exists |
| 429 | `RATE_LIMITED` | Too many registration attempts |

---

### POST `/auth/login` — Public
Authenticate and receive JWT tokens.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecureP@ss1"
}
```

**Response: 200 OK**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 900,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "Ajay Kumar",
    "has_profile": true
  }
}
```

**Error Responses:**
| Status | Code | Message |
|--------|------|---------|
| 401 | `INVALID_CREDENTIALS` | Invalid email or password |
| 403 | `ACCOUNT_LOCKED` | Account locked due to too many failed attempts. Try again after {locked_until} |
| 429 | `RATE_LIMITED` | Too many login attempts |

---

### POST `/auth/refresh` — Public (with refresh token)
Refresh an expired access token.

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response: 200 OK**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 900
}
```

---

### POST `/auth/logout` — Authenticated
Invalidate the current refresh token.

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response: 200 OK**
```json
{
  "message": "Successfully logged out"
}
```

---

### POST `/auth/password-reset/request` — Public
Request a password reset email.

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response: 200 OK** (always returns 200, even if email doesn't exist — prevents enumeration)
```json
{
  "message": "If this email is registered, a reset link has been sent"
}
```

---

### POST `/auth/password-reset/confirm` — Public
Reset password with token.

**Request:**
```json
{
  "token": "abc123def456...",
  "new_password": "NewSecureP@ss2"
}
```

**Response: 200 OK**
```json
{
  "message": "Password reset successfully"
}
```

---

## 2. User Profile Endpoints

### GET `/profile` — Authenticated
Get the current user's profile.

**Response: 200 OK**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "full_name": "Ajay Kumar",
  "age_range": "25-34",
  "sex": "male",
  "height_cm": 175.0,
  "weight_kg": 78.5,
  "fitness_goal": "muscle_gain",
  "fitness_level": "intermediate",
  "available_equipment": ["dumbbells", "barbell", "pull_up_bar", "bench"],
  "workout_days_per_week": 4,
  "session_duration_minutes": 60,
  "dietary_preference": "vegetarian",
  "allergies": ["lactose"],
  "medical_conditions": [],
  "profile_completed": true,
  "updated_at": "2026-09-01T10:30:00Z"
}
```

---

### PUT `/profile` — Authenticated
Update profile fields. Partial updates supported.

**Request:**
```json
{
  "fitness_goal": "fat_loss",
  "workout_days_per_week": 5,
  "weight_kg": 77.0
}
```

**Validation:**
- `age_range`: enum `["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]`
- `sex`: enum `["male", "female", "other", "prefer_not_to_say"]`
- `height_cm`: 100.0 - 250.0
- `weight_kg`: 30.0 - 300.0
- `fitness_goal`: enum `["weight_loss", "fat_loss", "muscle_gain", "endurance", "flexibility", "general_fitness", "strength"]`
- `fitness_level`: enum `["beginner", "intermediate", "advanced"]`
- `available_equipment`: array of strings from allowed equipment list
- `workout_days_per_week`: 1 - 7
- `session_duration_minutes`: 15 - 180
- `dietary_preference`: enum `["none", "vegetarian", "vegan", "keto", "paleo", "mediterranean"]`

**Response: 200 OK** — Returns updated profile (same schema as GET)

---

## 3. Chat / Conversation Endpoints

### POST `/chat/conversations` — Authenticated
Create a new conversation thread.

**Request:**
```json
{
  "title": "Beginner workout help"
}
```

**Response: 201 Created**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "title": "Beginner workout help",
  "created_at": "2026-09-01T10:30:00Z",
  "message_count": 0
}
```

---

### GET `/chat/conversations` — Authenticated
List user's conversations (paginated, most recent first).

**Query Parameters:**
- `page` (int, default: 1)
- `page_size` (int, default: 20, max: 50)

**Response: 200 OK**
```json
{
  "conversations": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "title": "Beginner workout help",
      "last_message_preview": "What's a good routine for...",
      "message_count": 12,
      "created_at": "2026-09-01T10:30:00Z",
      "updated_at": "2026-09-01T11:45:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 5,
    "total_pages": 1
  }
}
```

---

### POST `/chat/conversations/{conversation_id}/messages` — Authenticated
Send a message and receive AI response (streaming via SSE).

**Request:**
```json
{
  "content": "What's a good beginner push workout?",
  "context": {
    "active_plan_id": null
  }
}
```

**Response: 200 OK** (Server-Sent Events stream)
```
event: message_start
data: {"message_id": "770e8400-e29b-41d4-a716-446655440002", "role": "assistant"}

event: safety_check
data: {"category": "SAFE", "action": "PROCESS"}

event: content_delta
data: {"delta": "A great beginner push workout"}

event: content_delta
data: {"delta": " includes three key movements:"}

event: sources
data: {"sources": [{"title": "ACE Fitness Guide", "evidence_tier": 1, "chunk_id": "abc123"}]}

event: message_complete
data: {"message_id": "770e8400-e29b-41d4-a716-446655440002", "usage": {"prompt_tokens": 1200, "completion_tokens": 450}}
```

**Non-streaming fallback** (if `Accept: application/json`):
```json
{
  "message_id": "770e8400-e29b-41d4-a716-446655440002",
  "role": "assistant",
  "content": "A great beginner push workout includes three key movements...",
  "safety": {
    "category": "SAFE",
    "action": "PROCESS"
  },
  "sources": [
    {
      "title": "ACE Fitness Guide",
      "evidence_tier": 1,
      "url": null,
      "chunk_id": "abc123"
    }
  ],
  "created_at": "2026-09-01T10:31:00Z"
}
```

---

### GET `/chat/conversations/{conversation_id}/messages` — Authenticated
Get conversation history (paginated).

**Query Parameters:**
- `page` (int, default: 1)
- `page_size` (int, default: 50, max: 100)
- `order` (string, "asc" | "desc", default: "asc")

**Response: 200 OK**
```json
{
  "messages": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "role": "user",
      "content": "What's a good beginner push workout?",
      "created_at": "2026-09-01T10:30:00Z"
    },
    {
      "id": "770e8400-e29b-41d4-a716-446655440003",
      "role": "assistant",
      "content": "A great beginner push workout...",
      "sources": [...],
      "safety": { "category": "SAFE" },
      "created_at": "2026-09-01T10:31:00Z"
    }
  ],
  "pagination": { "page": 1, "page_size": 50, "total": 12 }
}
```

---

## 4. Plan Endpoints

### POST `/plans/generate` — Authenticated
Generate a personalized workout plan via AI.

**Request:**
```json
{
  "name": "My Push/Pull/Legs Plan",
  "preferences": {
    "split_type": "push_pull_legs",
    "days_per_week": 4,
    "session_duration_minutes": 60,
    "focus_areas": ["chest", "shoulders"],
    "exclude_exercises": ["barbell row"]
  }
}
```

**Response: 202 Accepted** (AI generation is async)
```json
{
  "plan_id": "880e8400-e29b-41d4-a716-446655440004",
  "status": "generating",
  "estimated_seconds": 15,
  "poll_url": "/api/v1/plans/880e8400-e29b-41d4-a716-446655440004"
}
```

---

### GET `/plans/{plan_id}` — Authenticated
Get a specific plan with full details.

**Response: 200 OK**
```json
{
  "id": "880e8400-e29b-41d4-a716-446655440004",
  "name": "My Push/Pull/Legs Plan",
  "status": "active",
  "is_template": false,
  "current_version": 1,
  "plan_data": {
    "overview": "4-day push/pull/legs split for intermediate lifters",
    "days": [
      {
        "day_number": 1,
        "name": "Push Day",
        "focus": ["chest", "shoulders", "triceps"],
        "exercises": [
          {
            "name": "Barbell Bench Press",
            "sets": 4,
            "reps": "8-10",
            "rest_seconds": 90,
            "notes": "Focus on controlled eccentric",
            "muscle_groups": ["chest", "triceps", "anterior deltoid"]
          },
          {
            "name": "Overhead Dumbbell Press",
            "sets": 3,
            "reps": "10-12",
            "rest_seconds": 60,
            "notes": null,
            "muscle_groups": ["shoulders", "triceps"]
          }
        ],
        "warmup": "5 min light cardio + shoulder circles + arm swings",
        "cooldown": "5 min chest/shoulder stretches"
      }
    ],
    "weekly_schedule": {
      "monday": "Push Day",
      "tuesday": "Pull Day",
      "wednesday": "Rest",
      "thursday": "Legs Day",
      "friday": "Upper Body",
      "saturday": "Rest",
      "sunday": "Rest"
    },
    "progression": "Add 2.5kg when you can complete all sets at the top of the rep range for 2 consecutive sessions"
  },
  "created_at": "2026-09-01T10:30:00Z",
  "updated_at": "2026-09-01T10:30:00Z"
}
```

---

### GET `/plans` — Authenticated
List user's plans + available templates.

**Query Parameters:**
- `type`: "my_plans" | "templates" | "all" (default: "my_plans")
- `status`: "active" | "archived" | "all" (default: "active")

**Response: 200 OK**
```json
{
  "plans": [
    {
      "id": "880e8400-...",
      "name": "My PPL Plan",
      "status": "active",
      "is_template": false,
      "days_per_week": 4,
      "current_version": 2,
      "created_at": "2026-09-01T10:30:00Z"
    }
  ],
  "pagination": { "page": 1, "page_size": 20, "total": 3 }
}
```

---

### PUT `/plans/{plan_id}` — Authenticated
Update a plan (creates new version).

**Request:**
```json
{
  "name": "Updated PPL Plan",
  "plan_data": { "...updated plan structure..." },
  "change_reason": "Swapped barbell row for cable row due to lower back discomfort"
}
```

**Response: 200 OK** — Returns updated plan with incremented `current_version`

---

### GET `/plans/{plan_id}/versions` — Authenticated
Get version history for a plan.

**Response: 200 OK**
```json
{
  "versions": [
    { "version": 2, "change_reason": "Swapped barbell row for cable row", "created_at": "..." },
    { "version": 1, "change_reason": "Initial generation", "created_at": "..." }
  ]
}
```

---

## 5. Progress Tracking Endpoints

### POST `/tracking/body-measurements` — Authenticated
Log a body measurement.

**Request:**
```json
{
  "date": "2026-09-01",
  "weight_kg": 78.5,
  "waist_cm": 84.0,
  "neck_cm": 38.0,
  "hip_cm": 96.0,
  "notes": "Measured in the morning, fasted"
}
```

**Validation:**
- `weight_kg`: 30.0 - 300.0
- `waist_cm`: 40.0 - 200.0
- `neck_cm`: 20.0 - 60.0
- `hip_cm`: 50.0 - 200.0
- `date`: Cannot be in the future; max 1 entry per day

**Response: 201 Created**
```json
{
  "id": "990e8400-...",
  "date": "2026-09-01",
  "weight_kg": 78.5,
  "waist_cm": 84.0,
  "neck_cm": 38.0,
  "hip_cm": 96.0,
  "body_fat_estimate": 18.5,
  "fat_mass_kg": 14.5,
  "lean_mass_kg": 64.0,
  "bmi": 25.6,
  "notes": "Measured in the morning, fasted",
  "created_at": "2026-09-01T10:30:00Z"
}
```

---

### GET `/tracking/body-measurements` — Authenticated
Get measurement history.

**Query Parameters:**
- `from_date` (ISO 8601, optional)
- `to_date` (ISO 8601, optional)
- `page`, `page_size`

**Response: 200 OK**
```json
{
  "measurements": [...],
  "trends": {
    "weight_change_kg": -2.5,
    "body_fat_change_pct": -1.2,
    "period_days": 30
  },
  "pagination": { ... }
}
```

---

### POST `/tracking/workouts` — Authenticated
Log a workout session.

**Request:**
```json
{
  "plan_id": "880e8400-...",
  "plan_day_number": 1,
  "date": "2026-09-01",
  "duration_minutes": 55,
  "exercises": [
    {
      "name": "Barbell Bench Press",
      "sets": [
        { "reps": 10, "weight_kg": 60, "completed": true },
        { "reps": 8, "weight_kg": 65, "completed": true },
        { "reps": 7, "weight_kg": 65, "completed": true },
        { "reps": 6, "weight_kg": 65, "completed": false }
      ]
    }
  ],
  "notes": "Felt strong on bench, struggled on last set",
  "perceived_effort": 7,
  "mood": "good"
}
```

**Response: 201 Created** — Returns the logged workout with computed volume stats.

---

### GET `/tracking/workouts` — Authenticated
Get workout history.

**Query Parameters:**
- `from_date`, `to_date`, `plan_id`, `page`, `page_size`

---

### GET `/tracking/stats` — Authenticated
Get aggregated statistics.

**Query Parameters:**
- `period`: "1w" | "1m" | "3m" | "6m" | "all" (default: "1m")

**Response: 200 OK**
```json
{
  "period": "1m",
  "workouts": {
    "total": 16,
    "completion_rate": 0.80,
    "avg_duration_minutes": 52,
    "by_week": [4, 4, 5, 3]
  },
  "volume": {
    "total_sets": 240,
    "total_reps": 2400,
    "total_weight_kg": 48000,
    "by_muscle_group": {
      "chest": { "sets": 48, "volume_kg": 12000 },
      "back": { "sets": 40, "volume_kg": 10000 }
    }
  },
  "body_composition": {
    "weight_start": 80.0,
    "weight_current": 78.5,
    "weight_change": -1.5,
    "body_fat_start": 20.0,
    "body_fat_current": 18.5,
    "body_fat_change": -1.5
  }
}
```

---

## 6. System Endpoints

### GET `/health` — Public
Health check endpoint.

**Response: 200 OK**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-09-01T10:30:00Z",
  "services": {
    "database": "healthy",
    "vector_store": "healthy",
    "llm": "healthy",
    "safety_gateway": "healthy"
  }
}
```

---

## 7. Common Response Patterns

### Error Response Format
All errors follow a consistent structure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format",
        "value": "not-an-email"
      }
    ],
    "request_id": "req_abc123def456"
  }
}
```

### Standard Error Codes

| HTTP Status | Code | Description |
|------------|------|-------------|
| 400 | `VALIDATION_ERROR` | Request body failed validation |
| 401 | `UNAUTHORIZED` | Missing or invalid authentication |
| 403 | `FORBIDDEN` | Authenticated but not authorized |
| 404 | `NOT_FOUND` | Resource not found |
| 409 | `CONFLICT` | Resource already exists |
| 422 | `UNPROCESSABLE` | Valid JSON but semantically incorrect |
| 429 | `RATE_LIMITED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Server error (generic) |
| 503 | `SERVICE_UNAVAILABLE` | Downstream service (LLM, DB) unavailable |

### Pagination
All list endpoints use offset-based pagination:
```json
{
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 150,
    "total_pages": 8,
    "has_next": true,
    "has_previous": false
  }
}
```

### Rate Limiting Headers
All responses include:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1693576200
```

**Rate Limits:**
| Endpoint Type | Limit |
|--------------|-------|
| Auth (register, login, reset) | 5 req/min per IP |
| Chat (send message) | 30 req/min per user |
| General API | 100 req/min per user |
| Health check | Unlimited |
