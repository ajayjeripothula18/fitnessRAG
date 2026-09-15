---
description: Deployment workflow for staging and production releases
---

# Deployment Workflow

**Version**: 1.0  
**Last Updated**: 2026-01-04  
**Purpose**: Systematic, safe deployment to staging and production

---

## When to Use This Workflow

### ✅ Use For:
- Production deployments
- Staging deployments
- Hot fix releases
- Rollbacks

### ❌ This is NOT For:
- Local development
- Running tests (use VALIDATE instead)

---

## Deployment in RRPAI Flow

```
... → VALIDATE (all tests pass) → DEPLOY → Monitor

Deployment sequence:
1. Deploy to Staging
2. Validate on Staging
3. Deploy to Production
4. Validate on Production
5. Monitor
```

**Position**: After successful validation, final SDLC phase

---

## Pre-Deployment Checklist

### ✅ Before ANY Deployment

 ALL must be true:
- [ ] All tests passing (Unit + Integration + E2E)
- [ ] Code reviewed and approved
- [ ] No known blockers or critical bugs
- [ ] Database migrations ready (if any)
- [ ] Environment variables configured
- [ ] Rollback plan defined
- [ ] Deployment window confirmed (if scheduled)

---

## Deployment Environments

### Local Development
- **Purpose**: Development and testing
- **URL**: `http://localhost:8000` or `http://agency.localhost:8000`
- **Database**: Local PostgreSQL
- **Deploy**: `python manage.py runserver`

### Staging
- **Purpose**: Pre-production validation
- **URL**: `https://staging.hypermiles.app`
- **Database**: Staging database (production-like)
- **Deploy**: Via CI/CD or manual

### Production
- **Purpose**: Live application
- **URL**: `https://hypermiles.app` / `https://agency.hypermiles.app`
- **Database**: Production database
- **Deploy**: Via CI/CD (preferred) or careful manual

---

## Deployment Process

### Stage 1: Deploy to Staging

#### Step 1: Prepare for Deployment

```bash
# Ensure on correct branch
git checkout main
git pull origin main

# Verify tests pass
cd app/backend
python manage.py test
```

#### Step 2: Database Migrations (if any)

// turbo
```bash
# Check for pending migrations
python manage.py showmigrations

# If migrations pending:
python manage.py migrate --plan  # Review plan
```

**For staging deployment**:
```bash
# Run migrations on staging
# (method depends on deployment setup)
python manage.py migrate
```

#### Step 3: Deploy to Staging

**Method depends on infrastructure**:

**Option A: Manual Deployment**
```bash
# SSH to staging server
ssh user@staging.hypermiles.app

# Pull latest code
cd /path/to/app
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Restart application
sudo systemctl restart hypermiles
```

**Option B: CI/CD (GitHub Actions, etc.)**
```yaml
# Trigger deployment workflow
# Usually automated on push to main
```

#### Step 4: Validate Staging Deployment

**Smoke tests**:
```bash
# Test health endpoint
curl https://staging.hypermiles.app/health/

# Test API endpoint
curl -X POST https://staging.hypermiles.app/api/agency/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test"}'
```

**Manual validation**:
- [ ] Can log in
- [ ] Core workflows work (book flight, view booking, etc.)
- [ ] No console errors
- [ ] Database queries working
- [ ] No regression in existing features

**If staging validation fails**:
- Investigate logs
- Rollback if critical
- Fix and re-deploy

---

### Stage 2: Deploy to Production

⚠️ **CRITICAL**: Only proceed if staging is fully validated

#### Step 1: Final Pre-Production Checks

- [ ] Staging fully validated (all smoke tests pass)
- [ ] No errors in staging logs
- [ ] Team notified about deployment
- [ ] Backup created (if critical)
- [ ] Rollback plan ready

#### Step 2: Create Deployment Tag

```bash
# Tag the release
git tag -a v1.2.3 -m "Release v1.2.3: Add wallet recharge feature"
git push origin v1.2.3
```

#### Step 3: Deploy to Production

**Follow same steps as staging** but for production:

```bash
# SSH to production server
ssh user@production.hypermiles.app

# Pull latest code
cd /path/to/app
git pull origin main
# OR
git fetch --tags
git checkout v1.2.3

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (with backup first!)
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Restart application
sudo systemctl restart hypermiles
```

#### Step 4: Validate Production Deployment

**Immediate validation** (within 5 minutes):

```bash
# Health check
curl https://hypermiles.app/health/

# API smoke test (use production test account)
curl -X POST https://agency.hypermiles.app/api/agency/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "prod_test", "password": "..."}'
```

**Manual validation**:
- [ ] Can log in
- [ ] Critical flows work
- [ ] No errors in browser console
- [ ] Response times acceptable

#### Step 5: Monitor (First 30 Minutes)

**Watch for**:
-Application logs (errors/exceptions)
- Database performance
- Response times
- User reports/support tickets

**Monitoring commands**:
```bash
# Watch application logs
tail -f /var/log/hypermiles/app.log

# Watch error logs
tail -f /var/log/hypermiles/error.log

# Check system resources
htop
```

---

## Rollback Procedures

### When to Rollback

**Immediate rollback if**:
- Critical functionality broken
- Data integrity issues
- Security vulnerability introduced
- Application crashes/unavailable

**Can wait if**:
- Minor UI issues
- Non-critical feature bugs
- Can be hot-fixed quickly

### How to Rollback

#### Option 1: Revert to Previous Tag (Preferred)

```bash
# SSH to server
ssh user@production.hypermiles.app

# Switch to previous version
cd /path/to/app
git fetch --tags
git checkout v1.2.2  # Previous stable version

# Rollback migrations (if needed)
python manage.py migrate app_name 0042  # Previous migration number

# Restart
sudo systemctl restart hypermiles
```

#### Option 2: Revert Commit

```bash
# Locally, revert the problematic commit
git revert <commit-hash>
git push origin main

# Deploy the revert
# (follow normal deployment process)
```

### Post-Rollback

- [ ] Validate rollback successful
- [ ] Document what went wrong
- [ ] Fix issue in development
- [ ] Re-deploy when ready

---

## Post-Deployment

### Update Documentation

**Update release notes**:
```markdown
# Release v1.2.3 - 2026-01-04

## Features
- Added wallet recharge API endpoint
- Implemented GST calculation for bookings

## Bug Fixes
- Fixed commission calculation for sub-agents

## Database Changes
- Added `wallet_transactions` table
- Added `gst_rate` column to `bookings`

## Deployment Notes
- Run migrations before deployment
- Update environment variable `GST_ENABLED=true`
```

**Location**: `.project/planning/RELEASE_NOTES.md` or `CHANGELOG.md`

### Update Tracking

```markdown
# Update TODO_NOW.md
- [x] Deploy wallet recharge feature

# Update SPRINT_TRACKER
## Deployment Log
| Date | Version | Features | Status |
|------|---------|----------|--------|
| 2026-01-04 | v1.2.3 | Wallet recharge | ✅ Deployed |
```

### Team Communication

**Notify team**:
```markdown
## Deployment Complete ✅

**Version**: v1.2.3
**Environment**: Production
**Deployed**: 2026-01-04 10:30 IST
**Features**: Wallet recharge, GST calculation
**Status**: All validations passed
**Monitoring**: Active for next 30 minutes
```

---

## Database Migration Best Practices

### Before Migration

```bash
# Always check migration plan
python manage.py migrate --plan

# Test on staging first
# Never run on production without staging validation
```

### Critical Migrations

If migration is **destructive** (drops columns, changes types):

1. **Create backup**:
   ```bash
   pg_dump -U postgres hypermiles > backup_$(date +%Y%m%d_%H%M%S).sql
   ```

2. **Test migration on copy of production data**
3. **Schedule maintenance window**
4. **Notify users** if downtime expected

### Migration Rollback

```bash
# Rollback to specific migration
python manage.py migrate app_name 0041

# Rollback all migrations for an app
python manage.py migrate app_name zero
```

---

## Environment Variables

### Checklist

Before deployment, verify:
- [ ] All required env vars set
- [ ] Secrets not in code (use env vars)
- [ ] Different values for staging vs. production

### Common Variables

```bash
# Django settings
DEBUG=False  # MUST be False in production
SECRET_KEY=<strong-random-key>
ALLOWED_HOSTS=hypermiles.app,agency.hypermiles.app

# Database
DATABASE_URL=postgres://user:pass@host:5432/hypermiles

# Redis
REDIS_URL=redis://localhost:6379/0

# External APIs
TBO_API_KEY=<key>
TBO_API_URL=https://api.tbo.com/

# Feature flags
GST_ENABLED=true
```

---

## Deployment Checklist Template

**Copy this for each deployment**:

```markdown
## Deployment Checklist: v1.2.3

### Pre-Deployment
- [ ] All tests passing
- [ ] Code reviewed and merged
- [ ] Migrations created and tested
- [ ] Release notes drafted
- [ ] Team notified

### Staging
- [ ] Deployed to staging
- [ ] Migrations run successfully
- [ ] Smoke tests passed
- [ ] Manual validation complete
- [ ] No errors in logs

### Production
- [ ] Final approval obtained
- [ ] Backup created (if critical migration)
- [ ] Deployed to production
- [ ] Smoke tests passed
- [ ] Manual validation complete
- [ ] Monitoring active

### Post-Deployment
- [ ] No errors in first 30 minutes
- [ ] Release notes published
- [ ] Tracking updated
- [ ] Team notified
```

---

## Quick Commands Reference

### Deployment
```bash
# Check current version/branch
git branch --show-current
git describe --tags

# Update code
git pull origin main

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Restart app (systemd)
sudo systemctl restart hypermiles
sudo systemctl status hypermiles
```

### Monitoring
```bash
# Watch logs
tail -f /var/log/hypermiles/app.log

# Check running processes
ps aux | grep python

# Check system resources
htop

# Check disk space
df -h
```

---

**Last Updated**: 2026-01-04  
**Version**: 1.0  
**Integrated with**: RRPAI v3.1  
**Previous**: `/rrpai/validate`
