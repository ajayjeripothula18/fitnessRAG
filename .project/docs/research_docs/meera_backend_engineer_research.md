# Meera (Backend Engineer) Research Findings

## Database Schema Design Patterns

### Core Tables for Fitness Application

#### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_login_at TIMESTAMPTZ,
    -- OAuth fields
    google_id VARCHAR(255) UNIQUE,
    apple_id VARCHAR(255) UNIQUE
);
```

#### Profiles Table
```sql
CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    age_range VARCHAR(20), -- e.g., '25-34', '35-44'
    sex VARCHAR(10), -- 'male', 'female', 'other'
    height_cm DECIMAL(5,2),
    weight_kg DECIMAL(5,2),
    fitness_level VARCHAR(20), -- 'beginner', 'intermediate', 'advanced'
    primary_goal VARCHAR(50), -- 'weight_loss', 'muscle_gain', etc.
    dietary_preference VARCHAR(50),
    allergies TEXT[], -- Array of allergies
    available_equipment TEXT[], -- Array of equipment
    workout_location VARCHAR(20), -- 'home', 'gym', 'outdoors'
    days_per_week INTEGER,
    session_duration_min INTEGER,
    food_dislikes TEXT[],
    experience_level VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### Plans Table
```sql
CREATE TABLE plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255),
    description TEXT,
    goal VARCHAR(50),
    duration_weeks INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    is_template BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### Plan Versions Table (for audit/history)
```sql
CREATE TABLE plan_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id UUID REFERENCES plans(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    plan_data JSONB NOT NULL, -- Structured plan data
    changed_by UUID REFERENCES users(id),
    change_reason TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### Workouts Table
```sql
CREATE TABLE workouts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id UUID REFERENCES plans(id) ON DELETE SET NULL,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    scheduled_for DATE,
    completed BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### Workout Logs Table
```sql
CREATE TABLE workout_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workout_id UUID REFERENCES workouts(id) ON DELETE CASCADE,
    exercise_name VARCHAR(255),
    sets_completed INTEGER,
    reps_per_set INTEGER[],
    weight_used DECIMAL(6,2), -- in kg or lbs
    duration_sec INTEGER,
    rpe INTEGER, -- Rate of Perceived Exertion 1-10
    energy_level INTEGER, -- 1-5 scale
    soreness_level INTEGER, -- 1-5 scale
    enjoyment_level INTEGER, -- 1-5 scale
    free_text_feedback TEXT,
    completed_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### Body Measurements Table
```sql
CREATE TABLE body_measurements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    measurement_date DATE NOT NULL,
    weight_kg DECIMAL(5,2),
    waist_cm DECIMAL(5,2),
    neck_cm DECIMAL(5,2),
    hip_cm DECIMAL(5,2),
    body_fat_estimate DECIMAL(5,2),
    fat_mass_kg DECIMAL(5,2),
    lean_mass_kg DECIMAL(5,2),
    bmi DECIMAL(4,2),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### Exercise Library Table
```sql
CREATE TABLE exercises (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    primary_muscle_groups TEXT[],
    secondary_muscle_groups TEXT[],
    equipment_required TEXT[], -- e.g., ['dumbbell', 'barbell']
    movement_pattern VARCHAR(50), -- 'squat', 'hinge', 'push', 'pull', etc.
    difficulty_level VARCHAR(20), -- 'beginner', 'intermediate', 'advanced'
    exercise_type VARCHAR(50), -- 'strength', 'cardio', 'flexibility', etc.
    contraindications TEXT[], -- e.g., ['knee_injury', 'back_pain']
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### Knowledge Tables (for RAG)
```sql
CREATE TABLE knowledge_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500),
    author TEXT,
    publisher VARCHAR(255),
    publication_date DATE,
    url TEXT,
    source_type VARCHAR(50), -- 'guideline', 'research', 'educational'
    evidence_tier INTEGER, -- 1=highest, 4=lowest
    retrieved_at TIMESTAMPTZ DEFAULT NOW(),
    version VARCHAR(50),
    content_hash VARCHAR(64)
);

CREATE TABLE knowledge_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID REFERENCES knowledge_sources(id) ON DELETE CASCADE,
    title VARCHAR(500),
    content TEXT,
    chunk_index INTEGER,
    token_count INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE knowledge_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES knowledge_documents(id) ON DELETE CASCADE,
    content TEXT,
    embedding VECTOR(384), -- or 768 depending on model
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Indexing Strategy
- Primary keys: UUID with default gen_random_uuid()
- Foreign keys: Indexed automatically in PostgreSQL
- Frequently queried columns: Add indexes (email, user_id, scheduled_for, measurement_date)
- Full-text search: GIN indexes on tsvector columns for exercise search
- Vector similarity: IVFFlat or HNSW indexes on embedding columns
- Composite indexes: For common query patterns (e.g., user_id + date ranges)

### Relationships and Constraints
- Use CASCADE deletes appropriately (user deletion removes profile, plans, etc.)
- Use SET NULL for optional relationships (workout plan reference)
- Add CHECK constraints for validated fields (age ranges, percentages, etc.)
- Use EXCLUDE constraints where appropriate (prevent overlapping date ranges)

## API Versioning and Authentication Best Practices

### API Versioning Strategies
#### URI Versioning (Recommended for MVP)
```
/api/v1/auth/login
/api/v1/users/profile
/api/v1/plans
```
- Pros: Simple, visible, cache-friendly
- Cons: Can lead to version proliferation
- Implementation: Use FastAPI APIRouter with prefix

#### Header Versioning
- Accept-Version: application/vnd.fitness.v1+json
- More RESTful but less visible
- Requires custom middleware

#### Query Parameter Versioning
- ?version=1.0
- Least preferred due to caching issues

### Authentication Implementation

#### OAuth2 with JWT (Recommended)
1. **Login Endpoint**: POST /api/v1/auth/login
   - Accepts email/password
   - Returns access_token (JWT) and refresh_token
   - Access token short-lived (15-30 min)
   - Refresh token longer-lived (7-30 days)

2. **Token Structure**:
   ```json
   {
     "sub": "user_uuid",
     "email": "user@example.com",
     "role": "user",
     "exp": 1234567890,
     "iat": 1234567890,
     "type": "access"
   }
   ```

3. **Security Considerations**:
   - Use HS256 for simplicity in MVP, consider RS256 for production
   - Store refresh tokens hashed in database (like passwords)
   - Implement token blacklisting for logout
   - Use secure, HTTP-only cookies for tokens if applicable
   - Implement rate limiting on auth endpoints
   - Use OAuth2PasswordBearer with FastAPI

#### Alternative: Session-Based Auth
- Simpler to implement initially
- Uses server-side sessions (Redis-backed)
- Less suitable for mobile/native clients
- Good for web-only MVP

#### Social Authentication (Google/Apple)
- Use `python-social-auth` or `authlib`
- Implement proper OAuth2 flow
- Link social accounts to existing email accounts
- Handle account merging appropriately

### Security Patterns for APIs
- Input validation with Pydantic models
- Output serialization to prevent over-exposure
- Rate limiting per IP/user (use slowapi or similar)
- Request size limits
- Timeout middleware
- Security headers (CSP, HSTS, X-Frame-Options, etc.)
- CORS configuration (restrict origins in production)
- SQL injection prevention (use ORM/parameterized queries)
- Logging without sensitive data
- Environment-based configuration (dev/staging/prod)

## Safety Pattern Libraries for Content Filtering

### Input Validation and Sanitization
- **Pydantic**: Built-in validation for FastAPI
- **Validators**: Custom validators for specific rules
- **Bleach**: HTML sanitization if accepting rich text
- **regex**: For pattern matching (use carefully)
- **phonenumbers**: For phone validation if needed

### Content Safety and Toxicity Detection
- **Perspective API** (Google): Toxicity, severe toxicity, etc.
  - Free tier available, requires API key
  - Good for detecting harmful language
- **Detoxify**: Python library for toxicity detection
  - Can run locally, multiple models available
  - Good for self-hosted solution
- **Hugging Face Transformers**: For custom classifiers
  - Models like `unitary/toxic-bert`
  - Can be run locally with appropriate resources

### Medical Content Detection
- **MedCAT**: Medical concept annotation tool
  - Can detect medical entities in text
  - Requires setup but effective for medical content
- **Clink**: Medical abbreviation expander
- **Custom NER**: Train or use existing models for medical PII

### Fitness-Specific Safety Rules
- **Exercise Contraindication Checking**: 
  - Cross-reference user profile with exercise restrictions
  - Example: Users with knee issues shouldn't get deep squats
- **Intensity Validation**: 
  - Check if proposed workout intensity matches fitness level
  - Use HR zones or RPE guidelines
- **Progressive Overload Limits**: 
  - Don't allow >10% weekly increase in volume/intensity
  - Based on ACSM guidelines
- **Pain vs. Discomfort Differentiation**:
  - Distinguish between muscle soreness and joint pain
  - Pain should trigger safety review/restriction

### Implementation Approach
1. **Pre-processing Layer**:
   - Input sanitization (basic)
   - Length limits
   - Character set validation

2. **Safety Classification**:
   - Rule-based checks first (fast, deterministic)
   - ML-based checks for nuanced cases
   - Medical content detection
   - Toxicity/harmful content detection

3. **Decision Engine**:
   - SAFE: Allow normal processing
   - MEDICAL_CONSULTATION_REQUIRED: Provide disclaimer + suggest professional
   - HARMFUL_CONTENT: Block and provide educational response
   - OUT_OF_SCOPE: Politely redirect to fitness/nutrition topics

4. **Post-processing Validation**:
   - Validate generated content against safety rules
   - Check for unintended medical advice
   - Ensure exercise recommendations match user profile
   - Verify nutritional guidance is general, not prescriptive

### Libraries and Tools
- **scispaCy**: For scientific/medical NLP
- **spaCy**: General NLP with customizable pipelines
- **NLTK**: Classic NLP library
- **scikit-learn**: For custom ML models if needed
- **firebase-admin**: For Google's safety APIs if using Firebase
- **azure-content-moderator**: If using Azure services

## Data Migration Strategies

### Migration Tool: Alembic (Recommended with SQLAlchemy)
- Integrates well with FastAPI + SQLAlchemy
- Supports autogenerate feature
- Handles both schema and data migrations
- Provides downgrade capability

### Migration Workflow
1. **Development**:
   - Modify SQLAlchemy models
   - Run `alembic revision --autogenerate -m "description"`
   - Review generated migration script
   - Apply with `alembic upgrade head`
   - Test locally

2. **Production**:
   - Test migration on staging copy of production DB
   - Schedule during low-usage period
   - Backup before migration
   - Run migration with monitoring
   - Validate post-migration
   - Have rollback plan ready

### Types of Migrations
#### Schema Changes
- Adding tables/columns
- Modifying column types
- Adding constraints/indexes
- Renaming (requires careful handling)

#### Data Changes
- Backfilling new columns
- Data cleanup/transformation
- Reference data updates
- Migration from legacy systems

### Best Practices
1. **Backward Compatibility**:
   - Add new columns as nullable initially
   - Provide default values where appropriate
   - Deprecate old fields before removing
   - Use versioned APIs to manage client changes

2. **Testing Migrations**:
   - Test on copy of production data
   - Measure migration time
   - Verify data integrity post-migration
   - Test downgrade path if applicable

3. **Zero-Downtime Migrations** (when needed):
   - Add new column, backfill gradually
   - Switch reads to new column
   - Switch writes to new column
   - Remove old column after transition
   - Use feature flags for dark launches

4. **Data Seeding**:
   - Separate seed data from migrations
   - Use seed scripts for reference data (exercise library, etc.)
   - Keep seeds idempotent
   - Separate prod/dev/test seeds

### Handling Specific Scenarios
#### Adding Exercise Library
1. Create exercises table
2. Create seed script with initial exercises
3. Run seed after table creation
4. Consider periodic updates from trusted sources

#### Evolving User Profile Schema
1. Add new profile fields as nullable
2. Provide sensible defaults in application code
3. Consider profile completion percentage
4. Allow users to skip optional fields

#### Plan Schema Evolution
1. Use versioned plans (plan_versions table)
2. Store plan as JSONB for flexibility
3. Migrate existing plans to version 1 on upgrade
4. New plans start at current version

### Monitoring and Validation
- Pre-migration: Record row counts, checksums
- Post-migration: Verify counts, spot-check data
- Use database constraints to validate after migration
- Monitor application logs for errors post-migration
- Have emergency rollback procedure tested

## Key Recommendations for MVP

### Database Design
1. Start with core tables: users, profiles, plans, workouts, measurements
2. Use UUIDs for all primary keys for security and distribution
3. Implement proper indexing from the start (don't wait for performance issues)
4. Use JSONB for flexible data (plan data, user preferences)
5. Implement soft deletes where appropriate (is_deleted flag)
6. Create views for common query patterns
7. Consider partitioning for time-series data (measurements, logs) if growing large
8. Implement database-level constraints for data integrity

### API and Authentication
1. Use JWT-based authentication with access/refresh tokens
2. Implement API versioning from day one (URI versioning)
3. Use Pydantic v2 for request/response validation
4. Implement rate limiting on authentication endpoints
5. Use HTTPS everywhere (even in dev with self-signed certs)
6. Store secrets in environment variables, never in code
7. Implement proper CORS restrictions
8. Add security headers via middleware
9. Structure API responses consistently (success/data/error format)
10. Implement proper HTTP status codes

### Safety Implementation
1. Start with rule-based safety checks (deterministic and fast)
2. Add ML-based toxicity detection as secondary layer
3. Implement medical content detection using rule + NLP approaches
4. Create clear escalation paths for different risk levels
5. Log all safety decisions for audit and improvement
6. Allow user appeals for false positives (important for UX)
7. Regularly update safety patterns based on feedback
8. Consider using Hugging Face models that can run locally for MVP

### Data Management
1. Use Alembic for migrations from the first schema change
2. Keep migrations small and focused
3. Test migrations on production-like data
4. Implement backup strategy (use Supabase built-in or custom)
5. Consider point-in-time recovery needs
6. Archive old data periodically (conversations, logs)
7. Implement data export/delete functionality for GDPR-like compliance
8. Monitor database performance early and often
9. Use connection pooling effectively
10. Consider read replicas if read-heavy workload anticipated