# FitnessRAG Database Design and API Specification
# Created by Meera (Backend Engineer)

## Database Design

### Design Philosophy
- **Normalization**: Balance between normalization for data integrity and denormalization for performance where appropriate
- **Data Integrity**: Use constraints, foreign keys, and data types to enforce correctness at the database level
- **Scalability**: Design with future growth in mind (indexing, partitioning readiness)
- **Security**: UUIDs for primary keys to prevent enumeration, sensitive data handling
- **Auditability**: Track changes where important for compliance and debugging
- **Flexibility**: Use JSONB for semi-structured data that may evolve

### Core Database Schema

#### Extension Enablement
```sql
-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgvector";
CREATE EXTENSION IF NOT EXISTS "btree_gin";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
```

#### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    hashed_password VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMPTZ WITH TIME ZONE DEFAULT NOW(),
    last_login_at TIMESTAMPTZ WITH TIME ZONE,
    -- OAuth fields
    google_id VARCHAR(255) UNIQUE,
    apple_id VARCHAR(255) UNIQUE,
    -- Password reset
    reset_token_hash VARCHAR(255),
    reset_token_expires_at TIMESTAMPTZ WITH TIME ZONE,
    -- Account security
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMPTZ WITH TIME ZONE,
    CONSTRAINT chk_oauth_ids CHECK (
        (google_id IS NULL AND apple_id IS NULL) OR 
        (google_id IS NOT NULL) OR 
        (apple_id IS NOT NULL)
    )
);

-- Indexes for users
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_google_id ON users(google_id) WHERE google_id IS NOT NULL;
CREATE INDEX idx_users_apple_id ON users(apple_id) WHERE apple_id IS NOT NULL;
CREATE INDEX idx_users_active ON users(is_active) WHERE is_active = true;
```

#### Profiles Table
```sql
CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    age_range VARCHAR(20) CHECK (age_range ~* '^\d{2}-\d{2}$|^18-\d{2}$|^65$'),
    sex VARCHAR(10) CHECK (sex IN ('male', 'female', 'other', 'prefer_not_to_say')),
    height_cm DECIMAL(5,2) CHECK (height_cm > 0 AND height_cm < 300),
    weight_kg DECIMAL(5,2) CHECK (weight_kg > 0 AND weight_kg < 500),
    fitness_level VARCHAR(20) CHECK (fitness_level IN ('beginner', 'intermediate', 'advanced')),
    primary_goal VARCHAR(50) CHECK (primary_goal IN (
        'weight_loss', 'muscle_gain', 'strength', 'endurance', 
        'general_fitness', 'flexibility', 'sport_specific', 'maintenance'
    )),
    dietary_preference VARCHAR(50) CHECK (dietary_preference IN (
        'omnivore', 'vegetarian', 'vegan', 'pescatarian', 'keto', 
        'paleo', 'mediterranean', 'dash', 'gluten_free', 'dairy_free', 'other'
    )),
    allergies TEXT[], -- Array of allergy strings
    available_equipment TEXT[], -- e.g., ['dumbbells', 'resistance_bands', 'yoga_mat']
    workout_location VARCHAR(20) CHECK (workout_location IN ('home', 'gym', 'outdoors', 'mixed')),
    days_per_week INTEGER CHECK (days_per_week >= 0 AND days_per_week <= 7),
    session_duration_min INTEGER CHECK (session_duration_min >= 0 AND session_duration_min <= 180),
    food_dislikes TEXT[],
    experience_level VARCHAR(20) CHECK (experience_level IN ('none', 'beginner', 'intermediate', 'advanced')),
    created_at TIMESTAMPTZ WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMPTZ WITH TIME ZONE DEFAULT NOW(),
    -- Soft delete for GDPR/compliance
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMPTZ WITH TIME ZONE
);

-- Indexes for profiles
CREATE INDEX idx_profiles_user_id ON profiles(user_id);
CREATE INDEX idx_profiles_active ON profiles(is_deleted) WHERE is_deleted = false;
CREATE INDEX idx_profiles_goal ON profiles(primary_goal);
CREATE INDEX idx_profiles_fitness_level ON profiles(fitness_level);
```

#### Plans Table
```sql
CREATE TABLE plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    goal VARCHAR(50) CHECK (goal IN (
        'weight_loss', 'muscle_gain', 'strength', 'endurance', 
        'general_fitness', 'flexibility', 'sport_specific', 'maintenance'
    )),
    duration_weeks INTEGER CHECK (duration_weeks > 0 AND duration_weeks <= 52),
    is_active BOOLEAN DEFAULT TRUE,
    is_template BOOLEAN DEFAULT FALSE,
    template_id UUID REFERENCES plans(id) ON DELETE SET NULL, -- Reference to template plan
    created_at TIMESTAMPTZ WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMPTZ WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for plans
CREATE INDEX idx_plans_user_id ON plans(user_id);
CREATE INDEX idx_plans_active ON plans(is_active) WHERE is_active = true;
CREATE INDEX idx_plans_template ON plans(is_template) WHERE is_template = true;
CREATE INDEX idx_plans_goal ON plans(goal);
```

#### Plan Versions Table (Audit Trail)
```sql
CREATE TABLE plan_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id UUID NOT NULL REFERENCES plans(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    plan_data JSONB NOT NULL, -- Structured plan representation
    changed_by UUID REFERENCES users(id),
    change_reason TEXT,
    created_at TIMESTAMPTZ WITH TIME ZONE DEFAULT NOW(),
    -- Ensure version numbers are sequential per plan
    CONSTRAINT uq_plan_version UNIQUE (plan_id, version_number)
);

-- Indexes for plan_versions
CREATE INDEX idx_plan_versions_plan_id ON plan_versions(plan_id);
CREATE INDEX idx_plan_versions_version ON plan_versions(version_number);
CREATE INDEX idx_plan_versions_changed_by ON plan_versions(changed_by);
```

#### Exercises Table (Standard Library)
```sql
CREATE TABLE exercises (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    primary_muscle_groups TEXT[] NOT NULL,
    secondary_muscle_groups TEXT[],
    equipment_required TEXT[] NOT NULL, -- e.g., ['bodyweight', 'dumbbell', 'barbell']
    movement_pattern VARCHAR(50) CHECK (movement_pattern IN (
        'squat', 'hinge', 'lunge', 'push', 'pull', 'rotation', 
        'core', 'carry', 'jump', 'throw', 'walk', 'run'
    )),
    difficulty_level VARCHAR(20) CHECK (difficulty_level IN ('beginner', 'intermediate', 'advanced')),
    exercise_type VARCHAR(50) CHECK (exercise_type IN (
        'strength', 'cardio', 'flexibility', 'balance', 'plyometrics'
    )),
    contraindications TEXT[], -- e.g., ['knee_pain', 'back_injury', 'shoulder_issue']
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMPTZ WITH TIME ZONE DEFAULT NOW(),
    -- Metadata for exercise variations
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Indexes for exercises
CREATE INDEX idx_exercises_name ON exercises(name);
CREATE INDEX idx_exercises_active ON exercises(is_active) WHERE is_active = true;
CREATE INDEX idx_exercises_type ON exercises(exercise_type);
CREATE INDEX idx_exercises_muscle ON exercises USING GIN (primary_muscle_groups);
CREATE INDEX idx_exercises_equipment ON exercises USING GIN (equipment_required);
CREATE INDEX idx_exercises_difficulty ON exercises(difficulty_level);
```

#### Workouts Table
```sql
CREATE TABLE workouts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id UUID REFERENCES plans(id) ON DELETE SET NULL, -- NULL if standalone workout
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    scheduled_for DATE NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMPTZ WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMPTZ WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for workouts
CREATE INDEX idx_workouts_user_id ON workouts(user_id);
CREATE INDEX idx_workouts_plan_id ON workouts(plan_id);
CREATE INDEX idx_workouts_scheduled_for ON workouts(scheduled_for);
CREATE INDEX idx_workouts_completed ON workouts(completed);
CREATE INDEX idx_workouts_date_range ON workouts(scheduled_for) WHERE completed = false;
```

#### Workout Logs Table (Detailed Performance)
```sql
CREATE TABLE workout_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workout_id UUID NOT NULL REFERENCES workouts(id) ON DELETE CASCADE,
    exercise_name VARCHAR(255) NOT NULL,
    sets_completed INTEGER NOT NULL CHECK (sets_completed > 0),
    reps_per_set INTEGER[] NOT NULL, -- Array matching sets_completed
    weight_used DECIMAL(6,2), -- in kg, NULL for bodyweight exercises
    duration_sec INTEGER, -- Total duration in seconds
    rpe INTEGER CHECK (rpe >= 1 AND rpe <= 10), -- Rate of Perceived Exertion
    energy_level INTEGER CHECK (energy_level >= 1 AND energy_level <= 5),
    soreness_level INTEGER CHECK (soreness_level >= 1 AND soreness_level <= 5),
    enjoyment_level INTEGER CHECK (enjoyment_level >= 1 AND enjoyment_level <= 5),
    free_text_feedback TEXT,
    completed_at TIMESTAMPTZ WITH TIME ZONE DEFAULT NOW(),
    -- Validation: weight_used required if equipment requires weight
    CONSTRAINT chk_weight_requirement CHECK (
        (weight_used IS NOT NULL) OR 
        (SELECT array_to_string(equipment_required, ',') FROM exercises WHERE name = exercise_name LIMIT 1) !~* '(dumbbell|barbell|kettlebell|weight)'
    )
);

-- Indexes for workout_logs
CREATE INDEX idx_workout_logs_workout_id ON workout_logs(workout_id);
CREATE INDEX idx_workout_logs_exercise_name ON workout_logs(exercise_name);
CREATE INDEX idx_workout_logs_completed_at ON workout_logs(completed_at);
```

#### Body Measurements Table
```sql
CREATE TABLE body_measurements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    measurement_date DATE NOT NULL,
    weight_kg DECIMAL(5,2) CHECK (weight_kg > 0 AND weight_kg < 500),
    waist_cm DECIMAL(5,2) CHECK (waist_cm > 0 AND waist_cm < 300),
    neck_cm DECIMAL(5,2) CHECK (neck_cm > 0 AND neck_cm < 200),
    hip_cm DECIMAL(5,2) CHECK (hip_cm > 0 AND hip_cm < 300),
    body_fat_estimate DECIMAL(5,2) CHECK (body_fat_estimate >= 0 AND body_fat_estimate <= 80),
    fat_mass_kg DECIMAL(5,2) CHECK (fat_mass_kg >= 0),
    lean_mass_kg DECIMAL(5,2) CHECK (lean_mass_kg >= 0),
    bmi DECIMAL(4,2) CHECK (bmi > 0 AND bmi < 100),
    notes TEXT,
    created_at TIMESTAMPTZ WITH TIME ZONE DEFAULT NOW(),
    -- Ensure at least one measurement is provided
    CONSTRAINT chk_measurements_provided CHECK (
        weight_kg IS NOT NULL OR 
        waist_cm IS NOT NULL OR 
        neck_cm IS NOT NULL OR 
        hip_cm IS NOT NULL
    )
);

-- Indexes for body_measurements
CREATE INDEX idx_body_measurements_user_id ON body_measurements(user_id);
CREATE INDEX idx_body_measurements_date ON body_measurements(measurement_date);
CREATE INDEX idx_body_measurements_user_date ON body_measurements(user_id, measurement_date);
```

#### Knowledge Base Tables (for RAG)
```sql
CREATE TABLE knowledge_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    author TEXT,
    publisher VARCHAR(255),
    publication_date DATE,
    url TEXT,
    source_type VARCHAR(50) CHECK (source_type IN (
        'guideline', 'research_article', 'review', 'meta_analysis', 
        'educational', 'book', 'website'
    )),
    evidence_tier INTEGER CHECK (evidence_tier >= 1 AND evidence_tier <= 4), -- 1 = highest
    retrieved_at TIMESTAMPTZ WITH TIME ZONE DEFAULT NOW(),
    version VARCHAR(50),
    content_hash VARCHAR(64), -- SHA-256 for change detection
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMPTZ WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE knowledge_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID NOT NULL REFERENCES knowledge_sources(id) ON DELETE CASCADE,
    title VARCHAR(500),
    content TEXT NOT NULL,
    language VARCHAR(10) DEFAULT 'en',
    chunk_count INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE knowledge_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES knowledge_documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    token_count INTEGER,
    embedding VECTOR(384), -- Dimension matches embedding model
    metadata JSONB DEFAULT '{}'::jsonb, -- Topic, section, etc.
    created_at TIMESTAMPTZ WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for knowledge base
CREATE INDEX idx_knowledge_sources_active ON knowledge_sources(is_active) WHERE is_active = true;
CREATE INDEX idx_knowledge_sources_tier ON knowledge_sources(evidence_tier);
CREATE INDEX idx_knowledge_documents_source ON knowledge_documents(source_id);
CREATE INDEX idx_knowledge_chunks_document ON knowledge_chunks(document_id);
-- Vector similarity index (using ivfflat initially)
CREATE INDEX idx_knowledge_chunks_embedding ON knowledge_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
-- Full-text search index
CREATE INDEX idx_knowledge_chunks_content_fts ON knowledge_chunks USING gin (to_tsvector('english', content));
```

### API Specification

#### Authentication Endpoints
**POST /api/v1/auth/register**
- Description: Register a new user account
- Request Body:
  ```json
  {
    "email": "user@example.com",
    "password": "securePassword123!",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```
- Response (201):
  ```json
  {
    "id": "uuid",
    "email": "user@example.com",
    "is_active": true,
    "is_verified": false,
    "created_at": "2024-01-01T00:00:00Z"
  }
  ```
- Errors:
  - 400: Validation error (invalid email, weak password, etc.)
  - 409: Email already registered

**POST /api/v1/auth/login**
- Description: Login with email and password
- Request Body:
  ```json
  {
    "email": "user@example.com",
    "password": "securePassword123!"
  }
  ```
- Response (200):
  ```json
  {
    "access_token": "jwt_token",
    "refresh_token": "refresh_token",
    "token_type": "bearer",
    "expires_in": 900, -- 15 minutes
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "is_active": true
    }
  }
  ```
- Errors:
  - 401: Invalid credentials
  - 403: Account locked or disabled

**POST /api/v1/auth/refresh**
- Description: Refresh access token using refresh token
- Request Body:
  ```json
  {
    "refresh_token": "refresh_token"
  }
  ```
- Response (200):
  ```json
  {
    "access_token": "new_jwt_token",
    "token_type": "bearer",
    "expires_in": 900
  }
  ```

**POST /api/v1/auth/logout**
- Description: Logout (invalidate refresh token)
- Requires: Authorization: Bearer <access_token>
- Request Body:
  ```json
  {
    "refresh_token": "refresh_token"
  }
  ```
- Response (200):
  ```json
  {
    "message": "Successfully logged out"
  }
  ```

#### User Profile Endpoints
**GET /api/v1/users/me/profile**
- Description: Get current user's profile
- Requires: Authorization: Bearer <access_token>
- Response (200):
  ```json
  {
    "id": "uuid",
    "user_id": "uuid",
    "age_range": "25-34",
    "sex": "male",
    "height_cm": 175.0,
    "weight_kg": 70.5,
    "fitness_level": "intermediate",
    "primary_goal": "muscle_gain",
    "dietary_preference": "omnivore",
    "allergies": ["peanuts"],
    "available_equipment": ["dumbbells", "resistance_bands"],
    "workout_location": "home",
    "days_per_week": 4,
    "session_duration_min": 45,
    "food_dislikes": ["cilantro"],
    "experience_level": "beginner",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
  ```

**PUT /api/v1/users/me/profile**
- Description: Update current user's profile
- Requires: Authorization: Bearer <access_token>
- Request Body: Partial profile object (same as GET response structure)
- Response (200): Updated profile object

#### Plans Endpoints
**GET /api/v1/plans**
- Description: Get user's plans (with filtering options)
- Requires: Authorization: Bearer <access_token>
- Query Parameters:
  - `active`: boolean (default: true)
  - `template`: boolean (default: false)
  - `goal`: string filter
  - `limit`: integer (default: 20)
  - `offset`: integer (default: 0)
- Response (200):
  ```json
  {
    "plans": [
      {
        "id": "uuid",
        "name": "Beginner Home Workout",
        "description": "Full body workout using dumbbells",
        "goal": "muscle_gain",
        "duration_weeks": 4,
        "is_active": true,
        "is_template": false,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
      }
    ],
    "total": 1,
    "limit": 20,
    "offset": 0
  }
  ```

**POST /api/v1/plans**
- Description: Create a new plan
- Requires: Authorization: Bearer <access_token>
- Request Body:
  ```json
  {
    "name": "Beginner Home Workout",
    "description": "Full body workout using dumbbells",
    "goal": "muscle_gain",
    "duration_weeks": 4,
    "is_active": true,
    "is_template": false
  }
  ```
- Response (201): Created plan object

**GET /api/v1/plans/{plan_id}**
- Description: Get a specific plan
- Requires: Authorization: Bearer <access_token>
- Response (200): Plan object with nested plan_data (if available)

**PUT /api/v1/plans/{plan_id}**
- Description: Update a plan
- Requires: Authorization: Bearer <access_token>
- Request Body: Partial plan object
- Response (200): Updated plan object

**DELETE /api/v1/plans/{plan_id}**
- Description: Delete a plan (soft delete)
- Requires: Authorization: Bearer <access_token>
- Response (204): No Content

**POST /api/v1/plans/{plan_id}/versions**
- Description: Create a new version of a plan (for modifications)
- Requires: Authorization: Bearer <access_token>
- Request Body:
  ```json
  {
    "change_reason": "User requested easier workout due to soreness"
  }
  ```
- Response (201): Created plan version object

**GET /api/v1/plans/{plan_id}/versions**
- Description: Get version history for a plan
- Requires: Authorization: Bearer <access_token>
- Response (200): Array of plan version objects

#### Workout Endpoints
**GET /api/v1/workouts**
- Description: Get user's workouts (with filtering)
- Requires: Authorization: Bearer <access_token>
- Query Parameters:
  - `start_date`: date (inclusive)
  - `end_date`: date (inclusive)
  - `completed`: boolean
  - `limit`: integer (default: 20)
  - `offset`: integer (default: 0)
- Response (200): Paginated list of workout objects

**POST /api/v1/workouts**
- Description: Schedule a workout
- Requires: Authorization: Bearer <access_token>
- Request Body:
  ```json
  {
    "plan_id": "uuid", -- Optional if creating standalone workout
    "scheduled_for": "2024-01-15",
    "notes": "Feeling energetic today"
  }
  ```
- Response (201): Created workout object

**GET /api/v1/workouts/{workout_id}**
- Description: Get a specific workout
- Requires: Authorization: Bearer <access_token>
- Response (200): Workout object with nested workout_logs

**PUT /api/v1/workouts/{workout_id}**
- Description: Update a workout
- Requires: Authorization: Bearer <access_token>
- Request Body: Partial workout object
- Response (200): Updated workout object

**POST /api/v1/workouts/{workout_id}/logs**
- Description: Log workout performance
- Requires: Authorization: Bearer <access_token>
- Request Body:
  ```json
  {
    "exercise_name": "Dumbbell Bench Press",
    "sets_completed": 3,
    "reps_per_set": [10, 8, 6],
    "weight_used": 22.5,
    "duration_sec": 300,
    "rpe": 8,
    "energy_level": 4,
    "soreness_level": 2,
    "enjoyment_level": 4,
    "free_text_feedback": "Felt strong on the last set"
  }
  ```
- Response (201): Created workout log object

#### Progress Tracking Endpoints
**GET /api/v1/progress/measurements**
- Description: Get user's body measurements
- Requires: Authorization: Bearer <access_token>
- Query Parameters:
  - `start_date`: date (inclusive)
  - `end_date`: date (inclusive)
  - `limit`: integer (default: 20)
  - `offset`: integer (default: 0)
- Response (200): Paginated list of measurement objects

**POST /api/v1/progress/measurements**
- Description: Record a new body measurement
- Requires: Authorization: Bearer <access_token>
- Request Body:
  ```json
  {
    "measurement_date": "2024-01-15",
    "weight_kg": 70.0,
    "waist_cm": 80.0,
    "neck_cm": 38.0,
    "hip_cm": 95.0
  }
  ```
- Response (201): Created measurement object (includes calculated fields like body_fat_estimate, bmi, etc.)

**GET /api/v1/progress/summary**
- Description: Get progress summary statistics
- Requires: Authorization: Bearer <access_token>
- Response (200):
  ```json
  {
    "weight": {
      "current": 70.0,
      "change_4w": -2.5,
      "change_12w": -5.0,
      "trend": "decreasing"
    },
    "workouts": {
      "total_this_month": 12,
      "avg_per_week": 3.0,
      "completion_rate": 0.85
    },
    "body_fat": {
      "current": 18.5,
      "change_4w": -1.2,
      "trend": "decreasing"
    }
  }
  ```

#### Exercise Library Endpoints
**GET /api/v1/exercises**
- Description: Search and filter exercises
- Requires: Authorization: Bearer <access_token>
- Query Parameters:
  - `search`: text search in name/description
  - `muscle_group`: string filter (matches primary or secondary)
  - `equipment`: string filter
  - `difficulty`: string filter
  - `exercise_type`: string filter
  - `limit`: integer (default: 20)
  - `offset`: integer (default: 0)
- Response (200): Paginated list of exercise objects

**GET /api/v1/exercises/{exercise_id}**
- Description: Get a specific exercise
- Requires: Authorization: Bearer <access_token>
- Response (200): Exercise object with full details

#### Chat / AI Coach Endpoints
**POST /api/v1/chat/message**
- Description: Send a message to the AI coach
- Requires: Authorization: Bearer <access_token>
- Request Body:
  ```json
  {
    "message": "What's a good workout for building muscle?",
    "conversation_id": "uuid" -- Optional, if continuing existing conversation
  }
  ```
- Response (200):
  ```json
  {
    "id": "uuid",
    "conversation_id": "uuid",
    "message": "What's a good workout for building muscle?",
    "response": "Based on your profile and fitness goals, I'd recommend...",
    "sources": [ -- Optional, if RAG was used
      {
        "id": "uuid",
        "title": "ACSM Guidelines for Resistance Training",
        "url": "https://www.acsm.org/read-research",
        "snippet": "For muscle growth, aim for 8-12 reps..."
      }
    ],
    "created_at": "2024-01-01T00:00:00Z"
  }
  ```
- Errors:
  - 400: Validation error
  - 429: Rate limit exceeded
  - 503: AI service unavailable

**GET /api/v1/chat/conversations**
- Description: Get user's chat conversations
- Requires: Authorization: Bearer <access_token>
- Query Parameters:
  - `limit`: integer (default: 20)
  - `offset`: integer (default: 0)
- Response (200): Paginated list of conversation objects

**GET /api/v1/chat/conversations/{conversation_id}/messages**
- Description: Get messages in a conversation
- Requires: Authorization: Bearer <access_token>
- Query Parameters:
  - `limit`: integer (default: 50)
  - `offset`: integer (default: 0)
- Response (200): Paginated list of message objects

#### Health Check Endpoints
**GET /health/live**
- Description: Liveness probe (is the application running?)
- Response (200):
  ```json
  {
    "status": "alive",
    "timestamp": "2024-01-01T00:00:00Z"
  }
  ```

**GET /health/ready**
- Description: Readiness probe (is the application ready to serve traffic?)
- Response (200):
  ```json
  {
    "status": "ready",
    "checks": {
      "database": "connected",
      "llm_service": "available",
      "cache": "connected"
    },
    "timestamp": "2024-01-01T00:00:00Z"
  }
  ```
- Errors:
  - 503: Service unavailable (if any critical check fails)

**GET /metrics**
- Description: Prometheus metrics endpoint
- Response (200): Prometheus format text/plain

### Data Validation Rules

#### Constraints Implemented at Database Level
1. **Email Format**: RFC 5322 compliant regex pattern
2. **Age Range**: Format validation (##-##) and range limits (18-65+)
3. **Physical Measurements**: Plausible ranges for height, weight, circumferences
4. **Enumerated Values**: CHECK constraints for fields with limited valid values
5. **Array Contents**: Application-level validation for array elements (equipment, allergies)
6. **JSON Structure**: Application-level validation for JSONB fields (plan_data, metadata)
7. **Referential Integrity**: Foreign keys with appropriate ON DELETE behaviors
8. **Uniqueness**: Unique constraints where appropriate (email, exercise name, etc.)
9. **Soft Delete Pattern**: is_deleted flag with filtered indexes for performance
10. **Temporal Constraints**: Date ranges, future/past validation where applicable

#### Application-Level Validation (Pydantic Models)
1. **Password Strength**: Minimum length, complexity requirements
2. **Exercise Validation**: 
   - Weight requirements based on equipment
   - Rep/set count consistency
   - Plausible duration ranges
3. **Plan Validation**:
   - Exercise availability based on user equipment
   - Intensity matching fitness level
   - Progressive overload limits (max 10% weekly increase)
   - Exercise substitution validity
4. **Measurement Validation**:
   - Logical relationships between measurements (e.g., waist < hip for females)
   - Plausible body fat ranges based on age/sex
   - Consistency between different measurement methods
5. **Chat Validation**:
   - Message length limits
   - Profanity filtering
   - Medical content detection
   - Harmful content screening

### Indexing Strategy

#### Primary Access Patterns
1. **User-centric queries**: Most queries filtered by user_id
2. **Time-series data**: Measurements, workouts logged over time
3. **Lookup by name/code**: Email, exercise name, plan name
4. **Status filtering**: Active/incomplete items
5. **Enumeration filtering**: Goal, difficulty level, etc.
6. **Vector similarity**: Knowledge chunk retrieval

#### Specific Index Recommendations
- **users**: email (unique), google_id/apple_id (sparse), is_active (filtered)
- **profiles**: user_id (FK), is_deleted (filtered), primary_goal, fitness_level
- **plans**: user_id, is_active (filtered), is_template (filtered), goal
- **plan_versions**: plan_id (FK), version_number (unique combo)
- **exercises**: name (unique), is_active (filtered), exercise_type, muscle_groups (GIN), equipment (GIN)
- **workouts**: user_id, plan_id (FK), scheduled_for, completed (filtered)
- **workout_logs**: workout_id (FK), exercise_name, completed_at
- **body_measurements**: user_id, measurement_date, user_id+measurement_date (composite)
- **knowledge_sources**: is_active (filtered), evidence_tier
- **knowledge_documents**: source_id (FK)
- **knowledge_chunks**: document_id (FK), embedding (ivfflat), content_fts (GIN)

#### Index Maintenance
- Regular monitoring of index usage and bloat
- Consider partitioning for large tables (body_measurements, workout_logs) by date
- Update statistics regularly for query planner effectiveness
- Review and adjust IVFFlat lists parameter based on data volume
- Consider migrating to HNSW for knowledge_chunks if performance demands

### Migration Strategy

#### Using Alembic
- All schema changes go through Alembic migrations
- Migration files stored in `app/migrations/`
- Naming convention: `xxxxxx_description.py`
- Both schema and data migrations supported
- Downgrade paths provided where practical
- Testing on production-like data before deployment

#### Migration Workflow
1. Developer makes changes to SQLAlchemy models
2. Runs `alembic revision --autogenerate -m "description"`
3. Reviews generated migration script
4. Edits if necessary (especially for data migrations, complex changes)
5. Runs migration against local development database
6. Tests application functionality
7. Runs migration against staging copy of production data
8. Deploys to production with monitoring

#### Data Migration Considerations
- Backfilling new columns with sensible defaults
- Handling enum value changes or additions
- Migrating JSONB structure changes
- Managing foreign key additions to existing tables
- Considering downtime vs. complex migration strategies
- Planning for rollback scenarios

### Performance Considerations

#### Query Optimization
1. **EXPLAIN ANALYZE**: Regular use to understand query plans
2. **Index Selection**: Ensure queries use appropriate indexes
3. **Join Ordering**: Let PostgreSQL optimizer work, use hints sparingly
4. **Limiting Results**: Use LIMIT/OFFSET or keyset pagination for large sets
5. **Specific vs General**: Select only needed columns
6. **Connection Pooling**: Size appropriately for expected concurrency
7. **Prepared Statements**: Leverage for repeated similar queries
8. **Statement Timeouts**: Prevent runaway queries from consuming resources

#### Caching Strategy
- **Application Level**: Cache frequently accessed, infrequently changing data
  - User profiles (short TTL)
  - Exercise library (longer TTL)
  - Plan templates (longer TTL)
- **Database Level**: 
  - Proper indexing reduces need for application caching
  - Consider materialized views for complex aggregations
- **Cache Invalidation**: 
  - Time-based (TTL)
  - Event-based (clear on update)
  - Write-through/write-behind patterns

#### Archiving and Purging
- **Old Conversations**: Consider archiving after 1 year
- **Inactive Users**: Soft delete, then purge after GDPR-required period
- **Analytics Tables**: Separate schema for aggregated data
- **Log Tables**: Rotate and archive based on size/age

### Security Considerations

#### Data Protection
1. **Encryption at Rest**: 
   - Rely on managed service encryption (Supabase) or filesystem encryption
   - Consider field-level encryption for highly sensitive PII
2. **Encryption in Transit**: 
   - TLS 1.3 enforced everywhere
   - HTTPS for all API endpoints
3. **Secrets Management**:
   - Database credentials in environment/vault
   - API keys in secret management systems
   - Never hardcode secrets
4. **Access Control**:
   - Principle of least privilege for database users
   - Separate roles for application, migrations, reporting
   - Row-level security (RLS) considered for future multi-tenancy
5. **Audit Logging**:
   - Track sensitive data access (GDPR/HIPAA considerations)
   - Log security-relevant events (login attempts, permission changes)
   - Maintain immutable audit trails where required

#### Input Validation and Sanitization
1. **SQL Injection Prevention**: 
   - Use parameterized queries/ORM exclusively
   - Never concatenate user input into SQL strings
2. **Input Validation**:
   - Validate all inputs at API boundary
   - Use whitelists where possible
   - Reject known bad patterns
3. **Output Encoding**:
   - HTML encode when outputting to web contexts
   - JSON encode for API responses
   - Context-appropriate encoding for other outputs
4. **Error Handling**:
   - Don't leak stack traces or system details in errors
   - Log detailed errors internally, return generic messages to users
   - Distinguish between client errors (4xx) and server errors (5xx)

### Backup and Recovery

#### Backup Strategy
1. **Primary**: Supabase built-in automated backups
   - Verify frequency and retention period
   - Test restore process regularly
2. **Secondary**: 
   - Manual logical backups (pg_dump) monthly
   - Store encrypted in offsite location
   - Test quarterly
3. **Point-in-Time Recovery**: 
   - Enable WAL archiving if managing PostgreSQL directly
   - Verify recovery procedures
4. **Consistency**: 
   - Ensure backups are application-consistent where possible
   - Consider stopping writes briefly for logical backups if needed

#### Recovery Procedures
1. **Database Failure**:
   - Restore from latest backup
   - Apply WAL logs if using PITR
   - Validate data integrity
   - Notify stakeholders
2. **Application Failure**:
   - Redeploy from known good container image
   - Validate health checks
   - Restore configuration if needed
3. **Complete Site Failure**:
   - Restore infrastructure from IaC
   - Restore database from backup
   - Redeploy application
   - Validate end-to-end functionality
4. **Regular Testing**:
   - Quarterly restore drills
   - Document recovery time objectives (RTO)
   - Document recovery point objectives (RPO)
   - Update procedures based on test results

### Monitoring and Observability

#### Database Metrics to Monitor
1. **Connection Pool Usage**: Active/idle/waiting connections
2. **Query Performance**: 
   - Slow queries (>1s threshold)
   - Query execution times
   - Rows returned/scanned
3. **Index Usage**: 
   - Hit ratios
   - Unused indexes for removal consideration
   - Index bloat
4. **Locking and Conflicts**:
   - Deadlocks
   - Lock wait times
   - Transaction rollbacks
5. **Replication Lag**: If using read replicas
6. **Storage Usage**:
   - Table and index sizes
   - Growth rates
   - Available space

#### Application Metrics to Monitor
1. **API Performance**:
   - Request rates, error rates, latency
   - Endpoint-specific breakdown
   - Status code distribution
2. **Business Metrics**:
   - Active users, new registrations
   - Feature usage (chat messages, plans created, etc.)
   - Conversion funnels
3. **System Health**:
   - Memory usage, CPU utilization
   - Disk I/O, network throughput
   - Garbage collection stats (JVM if applicable)
4. **External Dependencies**:
   - LLM service latency and error rates
   - Knowledge base freshness
   - Third-party API availability

#### Logging Strategy
1. **Structured Logging**: JSON format with standard fields
   - timestamp, level, logger, message
   - trace_id, span_id for distributed tracing
   - user_id, request_id for correlation
   - event_type, outcome for security/audit
2. **Log Levels**:
   - DEBUG: Development/troubleshooting
   - INFO: Normal operational events
   - WARN: Potentially problematic situations
   - ERROR: Error conditions requiring attention
   - FATAL: Severe errors causing application termination
3. **Sampling**: Consider sampling for high-volume debug logs
4. **Retention**: 
   - Operational logs: 7-30 days
   - Audit/security logs: 1-7 years (per requirements)
   - Debug logs: 1-3 days
5. **Centralization**: Forward logs to centralized system for analysis

## Conclusion

This database design and API specification provides a solid foundation for the FitnessRAG platform. It implements industry best practices for:

1. **Data Integrity**: Constraints, foreign keys, and data types enforce correctness
2. **Scalability**: Proper indexing, partitioning readiness, and connection pooling
3. **Security**: Defense in depth with encryption, access control, and validation
4. **Auditability**: Tracking changes where important for compliance
5. **Flexibility**: JSONB for evolving schema needs, versioned plans
6. **Performance**: Strategic indexing, query optimization guidelines
7. **Maintainability**: Clear naming conventions, documentation, and migration strategy

The design balances normalization for data integrity with selective denormalization for performance where appropriate. It supports the core features outlined in the PRD while providing a foundation for future enhancements.

By following this specification, the development team can implement a robust, secure, and scalable data layer that supports the application's functionality while demonstrating professional engineering practices.