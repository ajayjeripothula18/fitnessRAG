# FitnessRAG Development Setup and CI/CD Guide
# Created by Ravi (Tech Lead)

## Overview
This guide provides instructions for setting up the development environment, coding standards, and CI/CD pipelines for the FitnessRAG project. It consolidates research on Python backend templates, Docker multi-stage builds, CI/CD pipelines, and frontend frameworks.

## Development Environment Setup

### Prerequisites
- **Python**: 3.11+ (pyenv or official installer recommended)
- **Node.js**: 18+ (for frontend development)
- **Docker**: 20.10+ (for containerized development)
- **PostgreSQL**: 14+ (can use Docker or local installation)
- **Git**: 2.30+
- **Optional**: 
  - Ollama (for local LLM development)
  - Redis (for caching, optional in MVP)
  - Make or Just (for task running)

### Repository Setup
```bash
# Clone repository
git clone <repository-url>
cd fitnessrag

# Copy example environment files
cp .env.example .env
cp frontend/.env.example frontend/.env

# Initialize git hooks (if using)
pre-commit install
```

### Backend Setup (Python/FastAPI)

#### Option 1: Local Development (Recommended for MVP)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or .\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Includes testing, linting tools

# Install pre-commit hooks
pre-commit install

# Set up environment variables
# Edit .env file with appropriate values
# See .env.example for reference

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Option 2: Containerized Development
```bash
# Build development image
docker-compose -f docker-compose.dev.yml build

# Start services
docker-compose -f docker-compose.dev.yml up

# Services will be available at:
# - API: http://localhost:8000
# - Frontend: http://localhost:3000 (if using separate frontend service)
# - Database: localhost:5432
```

#### Option 3: Fully Containerized with Docker Compose
```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app:cached
      - ./logs:/app/logs
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/fitnessrag
      - OLLAMA_HOST=host.docker.internal:11434
    depends_on:
      - db
      - ollama
  
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - ./frontend/src:/app/src:cached
    environment:
      - VITE_API_URL=http://localhost:8000/api/v1
    depends_on:
      - backend
  
  db:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=fitnessrag
      - POSTGRES_PASSWORD=securepassword123
      - POSTGRES_DB=fitnessrag
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0:11434
  
volumes:
  postgres_data:
  ollama_data:
```

### Frontend Setup (React/Vite)

#### Local Development
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Application will be available at http://localhost:5173
```

#### Containerized Development
```bash
# From project root
docker-compose -f docker-compose.dev.yml up frontend
```

### Environment Configuration
Copy `.env.example` to `.env` and adjust values:

#### Backend (.env)
```
# Application
APP_NAME=FitnessRAG
ENVIRONMENT=development
DEBUG=true

# Database
DATABASE_URL=postgresql://fitnessrag:securepassword123@localhost:5432/fitnessrag

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Ollama (Local LLM)
OLLAMA_HOST=http://localhost:11434
OLLAMA_DEFAULT_MODEL=llama3:8b

# External APIs (if using)
# HUGGINGFACE_API_KEY=your_hf_key_here

# Email (for notifications)
# SMTP_HOST=smtp.example.com
# SMTP_PORT=587
# SMTP_USER=your_user
# SMTP_PASSWORD=your_password

# Feature Flags
ENABLE_METRICS=true
ENABLE_HEALTH_CHECKS=true
```

#### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME=FitnessRAG
```

### Code Quality Tools

#### Backend Python Tools
- **Formatting**: black, isort
- **Linting**: flake8, pylint, ruff
- **Type Checking**: mypy
- **Testing**: pytest, pytest-asyncio, hypothesis
- **Security**: bandit, safety, pip-audit
- **Pre-commit**: Configured to run checks on commit

#### Frontend JavaScript Tools
- **Formatting**: Prettier
- **Linting**: ESLint with React plugin
- **Type Checking**: TypeScript (if using) or JSDoc checks
- **Testing**: Jest, React Testing Library
- **Security**: npm audit, snyk
- **Pre-commit**: Configured to run checks on commit

### Database Management

#### Migrations with Alembic
```bash
# Create new migration
alembic revision --autogenerate -m "description of change"

# Review generated migration
# Edit if necessary (especially for data migrations)

# Apply migration
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# Show migration history
alembic history

# Show current revision
alembic current
```

#### Database Seeding
Seed scripts are located in `app/seeds/`:
```bash
# Run all seeders
python -m app.seeds.run_all

# Run specific seeder
python -m app.seeds.exercise_library
```

### Testing Strategy

#### Running Tests
```bash
# Backend tests
pytest
pytest -v  # Verbose
pytest --cov=app  # With coverage
pytest -m "not slow"  # Exclude slow tests

# Frontend tests
cd frontend
npm test
npm run test:coverage

# End-to-end tests (if using Cypress/Playwright)
# From project root
npm run test:e2e  # In frontend package
```

#### Test Organization
```
tests/
├── unit/                 # Unit tests
│   ├── test_auth_service.py
│   ├── test_plan_service.py
│   └── ...
├── integration/          # Integration tests
│   ├── test_auth_api.py
│   ├── test_chat_workflow.py
│   └── ...
├── e2e/                  # End-to-end tests (frontend)
│   └── ...
└── conftest.py          # Shared pytest fixtures
```

### Docker Images

#### Building Images
```bash
# Backend image
docker build -t fitnessrag/backend:latest .

# Frontend image
cd frontend
docker build -t fitnessrag/frontend:latest .
```

#### Multi-stage Dockerfile Examples

**Backend Dockerfile**
```dockerfile
# Builder stage
FROM python:3.11-slim AS builder
WORKDIR /app
ENVIRONMENT=builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt
COPY requirements-dev.txt .
RUN pip install --user -r requirements-dev.txt
COPY . .
RUN pytest  # Fail build if tests fail

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
ENVIRONMENT=production
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health/live || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile**
```dockerfile
# Builder stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### CI/CD Pipeline (GitHub Actions)

#### Workflow Structure
```
.github/
└── workflows/
    ├── ci.yml              # Continuous Integration
    ├── cd-staging.yml      # Continuous Deployment to Staging
    └── cd-production.yml   # Continuous Deployment to Production
```

#### CI Workflow (ci.yml)
```yaml
name: Continuous Integration

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build-test-and-scan:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11]
        node-version: [18.x]
    
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_USER: fitnessrag
          POSTGRES_PASSWORD: ${{ secrets.POSTGRES_PASSWORD }}
          POSTGRES_DB: fitnessrag_test
        ports: [5432:5432]
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
        cd frontend && npm ci
    
    - name: Setup environment
      run: |
        cp .env.example .env
        echo "DATABASE_URL=postgresql://fitnessrag:${{ secrets.POSTGRES_PASSWORD }}@localhost:5432/fitnessrag_test" >> .env
        cd frontend && cp .env.example .env
    
    - name: Run backend tests
      run: |
        alembic upgrade head
        pytest --cov=app --cov-report=xml
    
    - name: Run frontend tests
      run: |
        cd frontend
        npm test -- --coverage
    
    - name: Security scanning
      run: |
        # Python dependencies
        safety check --full-report
        bandit -r app/ -f json -o bandit-report.json
        # Node.js dependencies
        cd frontend && npm audit --json > audit-report.json
    
    - name: Docker build and scan
      run: |
        # Build backend image
        docker build -t fitnessrag/backend:${{ github.sha }} .
        # Scan image
        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --format json --output trivy-backend.json fitnessrag/backend:${{ github.sha }}
        # Build frontend image
        cd frontend && docker build -t fitnessrag/frontend:${{ github.sha }} .
        # Scan frontend image
        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --format json --output trivy-frontend.json fitnessrag/frontend:${{ github.sha }}
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: test-reports
        path: |
          coverage.xml
          coverage-frontend/
          bandit-report.json
          trivy-*.json
          audit-report.json
    
    - name: Comment on PR
      if: github.event_name == 'pull_request'
      uses: thollander/actions-comment-pull-request@v2
      with:
        message: |
          ## CI Results
          - Tests: ${{ job.status }}
          - Coverage: ${{ steps.test_coverage.outputs.coverage }}%
          - Security: Scanned
          - Docker Images: Built and scanned
```

#### CD Staging Workflow (cd-staging.yml)
```yaml
name: Deploy to Staging

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    needs: [build]  # Assume build job in separate workflow or combine
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up cloud credentials
      # Example for Render.com
      - uses: johnbeynon/render-deploy-action@v1
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          api-key: ${{ secrets.RENDER_API_KEY }}
    
    - name: Wait for deployment
      run: |
        # Implement polling or webhook verification
        sleep 30
    
    - name: Run post-deployment checks
      run: |
        # Verify health endpoints
        curl -f https://staging.fitnessrag.com/health/live
        curl -f https://staging.fitnessrag.com/health/ready
    
    - name: Notify team
      # Use Slack, email, etc.
```

#### CD Production Workflow (cd-production.yml)
Similar to staging but with:
- Manual approval environment
- Tag-based triggering (e.g., v1.0.0)
- Additional validation steps
- Blue/green or canary deployment strategy

### Development Workflow Guidelines

#### Branching Strategy
- **main**: Production-ready code only
- **develop**: Integration branch for features
- **feature/***: Feature branches from develop
- **bugfix/***: Bug fix branches from develop
- **release/***: Release preparation branches
- **hotfix/***: Emergency fixes from main

#### Commit Message Format
Use Conventional Commits:
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```
Types: feat, fix, docs, style, refactor, perf, test, chore, ci

Example:
```
feat(auth): add Google OAuth2 login

- Implement Google sign-in flow
- Add OAuth2 configuration
- Update user model for OAuth fields
- Add corresponding unit tests

Fixes: #123
```

#### Pull Request Process
1. Create feature branch from develop
2. Develop with frequent commits
3. Run local tests: `pytest` and `npm test`
4. Ensure pre-commit passes
5. Push branch and open PR against develop
6. Require at least one approval
7. Squash and merge after CI passes
8. Delete feature branch

#### Release Process
1. From develop, create release/vX.Y.Z branch
2. Update version in package files (pyproject.toml, frontend/package.json)
3. Generate changelog
4. QA testing on release branch
5. Merge into main and develop
6. Tag main with vX.Y.Z
7. Trigger production deployment

### Troubleshooting

#### Common Backend Issues
- **Database connection failures**: 
  - Check DATABASE_URL in .env
  - Verify PostgreSQL is running
  - Check network/firewall settings
  
- **LLM connection errors**:
  - Verify OLLAMA_HOST is correct
  - Ensure Ollama service is running
  - Check model availability with `ollama list`
  
- **Migration failures**:
  - Check migration script for syntax errors
  - Verify database user has permissions
  - Consider manual intervention for complex migrations

#### Common Frontend Issues
- **Dependency resolution**:
  - Delete node_modules and package-lock.json, then reinstall
  - Check for conflicting versions
  
- **Build failures**:
  - Check console for specific error messages
  - Verify compatibility of dependencies
  
- **Runtime errors**:
  - Use browser devtools for debugging
  - Check network tab for failed API requests

#### Docker Issues
- **Port conflicts**: 
  - Check what's using the port with `lsof -i :port`
  - Change port in docker-compose or application config
  
- **Volume permissions**:
  - Ensure proper ownership of mounted volumes
  - Consider using named volumes vs bind mounts
  
- **Image build failures**:
  - Check Dockerfile syntax
  - Verify base image availability
  - Look for missing dependencies

### Performance Tips for Development

#### Backend
- Use `uvicorn` with `--reload` during development
- Enable SQL query logging in debug mode
- Use connection pooling effectively
- Cache frequently accessed static data

#### Frontend
- Leverage Vite's fast HMR
- Use React DevTools for performance profiling
- Implement code splitting for lazy loading
- Optimize images and assets

#### Database
- Use EXPLAIN ANALYZE for query optimization
- Monitor connection pool usage
- Consider read replicas for scaling reads
- Archive old data periodically

### Security Practices for Development

#### Secrets Management
- Never commit secrets to git
- Use environment variables or secret managers
- Use tools like git-secrets to prevent accidental commits
- Rotate secrets regularly

#### Dependency Security
- Run `safety check` regularly
- Use `dependabot` for automatic updates
- Review security advisories for critical dependencies
- Consider using a software bill of materials (SBOM)

#### Code Security
- Follow principle of least privilege
- Validate and sanitize all inputs
- Use parameterized queries to prevent SQL injection
- Implement proper error handling (don't leak stack traces)

### Resources and References

#### Backend
- FastAPI Documentation: https://fastapi.tiangolo.com/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- Alembic Documentation: https://alembic.sqlalchemy.org/
- Pydantic Documentation: https://docs.pydantic.dev/
- LangChain Documentation: https://python.langchain.com/
- LangGraph Documentation: https://langchain-ai.github.io/langgraph/

#### Frontend
- React Documentation: https://react.dev/
- Vite Documentation: https://vitejs.dev/
- Tailwind CSS Documentation: https://tailwindcss.com/
- Chakra UI Documentation: https://chakra-ui.com/
- React Query Documentation: https://tanstack.com/query/latest

#### DevOps
- Docker Documentation: https://docs.docker.com/
- GitHub Actions Documentation: https://docs.github.com/en/actions
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Prometheus Documentation: https://prometheus.io/docs/introduction/overview/
- Sentry Documentation: https://docs.sentry.io/

## Conclusion

This guide provides a comprehensive foundation for developing, testing, and deploying the FitnessRAG platform. By following these practices, the team can ensure consistency, quality, and security throughout the development lifecycle while maintaining the ability to deliver value rapidly within the constraints of a portfolio MVP.

The emphasis on automation (CI/CD), containerization, and observability creates a professional development environment that demonstrates senior-level engineering practices while remaining accessible for a small team working within timeline and budget constraints.