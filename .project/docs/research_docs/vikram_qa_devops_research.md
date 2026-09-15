# Vikram (QA/DevOps) Research Findings

## Testing Strategies for AI-Powered Applications

### Testing Pyramid for Fitness RAG Application
1. **Unit Tests** (Foundation):
   - Test individual functions and methods
   - Mock external dependencies (LLM, vector store, APIs)
   - Focus on business logic: calculators, validation rules, safety checks
   - Target: 70-80% coverage of core logic

2. **Integration Tests** (Middle Layer):
   - Test API endpoints with real database
   - Test service layer interactions
   - Test LangGraph workflows with mocked LLM/vector store
   - Test authentication and authorization flows
   - Target: 20-30% of tests

3. **End-to-End Tests** (Top):
   - Critical user journeys (login → ask question → get response)
   - Test UI interactions with real backend (Cypress or Playwright)
   - Test mobile-specific gestures and interactions
   - Target: 5-10% of tests

### Specific Testing Areas

#### LLM and AI Component Testing
- **Prompt Testing**: Test various prompts for consistency and safety
- **Output Validation**: Verify LLM outputs conform to expected formats
- **Hallucination Detection**: Test for factual accuracy against knowledge base
- **Bias Testing**: Check for unintended biases in recommendations
- **Safety Testing**: Attempt to elicit harmful or medical advice
- **Consistency**: Similar prompts should yield similar advice levels

#### RAG System Testing
- **Retrieval Relevance**: Test that retrieved documents are actually relevant
- **Precision/Recall**: Measure retrieval quality with test queries
- **Source Attribution**: Verify that sources are correctly attributed
- **Hybrid Search**: Test both vector and lexical components
- **Reranking Effectiveness**: Check that reranking improves results
- **Metadata Filtering**: Test that filters correctly narrow results

#### Safety Gateway Testing
- **Positive Testing**: Valid fitness/nutrition questions should pass
- **Negative Testing**: 
  - Medical advice requests should be blocked/redirected
  - Toxic/harmful content should be detected
  - Personal health data requests should be handled appropriately
  - Extremely dangerous exercise requests should be flagged
- **Edge Cases**: Ambiguous queries, misspellings, slang
- **Over-blocking**: Ensure legitimate questions aren't incorrectly blocked

#### Plan Generation and Validation Testing
- **Structural Validation**: Generated plans should have correct structure
- **Constraint Satisfaction**: Plans should respect user profile constraints
- **Exercise Validity**: All exercises should exist in exercise library
- **Equipment Matching**: Plans should only use available equipment
- **Intensity Appropriateness**: Workout intensity should match fitness level
- **Progression Logic**: Plans should show appropriate progression over time
- **Modification Testing**: Plan modifications should be valid and tracked

#### Progress Tracking Testing
- **Data Integrity**: Measurements should be stored correctly
- **Time-Series Queries**: Efficient querying of historical data
- **Calculation Accuracy**: Body fat estimates should match reference calculations
- **Trend Analysis**: Progress trends should be correctly calculated
- **Goal Tracking**: Goal achievement should be detected correctly

### Testing Tools and Frameworks

#### Backend Testing (Python)
- **pytest**: Primary testing framework
- **pytest-asyncio**: For async function testing
- **httpx.AsyncClient**: For testing FastAPI endpoints
- **factory_boy or model_bakery**: For test data generation
- **responses or requests-mock**: For mocking external HTTP calls
- **pytest-mock**: For mocking dependencies
- **hypothesis**: For property-based testing
- **tox**: For testing across Python versions

#### Frontend Testing (JavaScript/TypeScript)
- **Jest**: Unit testing for React components
- **React Testing Library**: For testing user interactions
- **Cypress or Playwright**: For end-to-end testing
- **jest-dom**: For custom Jest matchers
- **user-event**: For simulating user actions
- **msw (Mock Service Worker)**: For mocking API calls

#### Mobile/PWA Specific Testing
- **Lighthouse**: For performance, accessibility, PWA compliance
- **Web Vitals Measurement**: For real-user monitoring
- **Touch Event Testing**: For mobile-specific interactions
- **Offline Functionality**: Testing service worker caching
- **Installability Testing**: PWA install prompts and behavior

### AI-Specific Testing Considerations

#### Non-Determinism Handling
- **Seed Control**: Use fixed seeds for reproducible testing where possible
- **Statistical Testing**: For non-deterministic outputs, test distributions
- **Golden Master Testing**: Approve known good outputs as baseline
- **Similarity Metrics**: Use semantic similarity for response comparison
- **Threshold-Based**: Accept outputs within certain quality thresholds

#### Hallucination and Grounding Testing
- **Knowledge Base Grounding**: Verify responses are supported by retrieved docs
- **Fact-Checking**: Compare claims against trusted sources
- **Uncertainty Quantification**: Test model's ability to express uncertainty
- **Attribution Verification**: Check that cited sources actually support claims

#### Safety and Ethical Testing
- **Adversarial Testing**: Attempt to jailbreak or manipulate the system
- **Bias Probes**: Test for demographic or other biases
- **Privacy Testing**: Ensure no leakage of personal data in responses
- **Consent Testing**: Verify proper handling of sensitive topics

## Security Scanning Tools for Python Dependencies

### Dependency Vulnerability Scanning
- **safety**: Checks Python packages against known vulnerabilities
  - Integrates well with CI/CD
  - Can ignore specific CVEs if necessary
  - Open source and actively maintained
  
- **pip-audit**: Official PyPA tool for auditing Python environments
  - Uses PyPI vulnerability database
  - Can be used as pre-commit hook
  
- **dependabot**: GitHub-native dependency updates and security alerts
  - Automatic PRs for vulnerable dependencies
  - Configurable update frequency
  
- **snyk**: Comprehensive security platform
  - Scans dependencies, containers, code, IaC
  - Free tier available for open source/small teams
  - Provides detailed fix recommendations
  
- **azure-security-python**: Microsoft's security scanner for Python
  - Good integration with Azure DevOps
  - Less known but effective

### Container Image Scanning
- **trivy**: Comprehensive vulnerability scanner for containers
  - Scans OS packages and application dependencies
  - Fast and easy to use in CI
  - Open source
  
- **grype**: Anchore's vulnerability scanner
  - Similar to trivy with good database
  - Supports various output formats
  
- **clair**: Container vulnerability scanning service
  - More complex setup but good for Kubernetes
  
- **docker scan**: Docker's built-in scanning (uses Snyk backend)

### Static Application Security Testing (SAST)
- **bandit**: Python-specific security linter
  - Finds common security issues in Python code
  - Integrates with pytest and CI/CD
  - Configurable rule sets
  
- **semgrep**: Multi-language pattern matching for security
  - Can write custom rules
  - Excellent for finding specific patterns
  - Fast and customizable
  
- **flake8-security**: Security-focused flake8 plugin
  - Simple integration if already using flake8
  
- **pylint-security**: Security checker for pylint
  - Good if already using pylint

### Dynamic Application Security Testing (DAST)
- **OWASP ZAP**: Popular open-source DAST tool
  - Can be automated in CI/CD
  - Good for finding runtime vulnerabilities
  - Has excellent community support
  
- **Nikto**: Web server scanner
  - Good for finding outdated software and misconfigurations
  - Less effective for complex app logic
  
- **Burp Suite**: Professional DAST tool (free community edition)
  - Excellent for manual testing
  - Can be automated to some extent

### Secrets Detection
- **git-secrets**: Prevents committing secrets to git
  - AWS-focused but configurable
  - Works as pre-commit hook
  
- **detect-secrets**: GitHub's secrets detection framework
  - Can scan repos for existing secrets
  - Supports various secret types
  
- **truffleHog**: Finds secrets in git history
  - Can detect high-entropy strings
  - Good for auditing existing repos

### Security Testing in CI/CD
1. **Pre-commit**: 
   - Run bandit, semgrep, safety on staged changes
   - Prevent obvious security issues early
   
2. **Pull Request**:
   - Run dependency scanning (safety, pip-audit)
   - Run container scanning if building images
   - Run SAST tools
   - Comment on PR with results
   
3. **Main Branch**:
   - Run full security scan on merge
   - Fail build on critical/severe vulnerabilities
   - Allow low/medium with tickets for tracking
   
4. **Scheduled**:
   - Weekly dependency scans for new vulnerabilities
   - Monthly container rescans
   - Quarterly penetration tests (if resources allow)

## Logging and Monitoring Solutions for Free Tiers

### Structured Logging
- **structlog**: Excellent for structured logging in Python
  - JSON output by default
  - Contextual logging (bind user/request IDs)
  - Processors for timestamping, level filtering, etc.
  
- **loguru**: Simpler alternative to structlog
  - Easy setup, good defaults
  - Automatic serialization, rotation, etc.
  - Less configurable than structlog but very usable
  
- **Standard logging + jsonlogger**: 
  - Use Python's standard logging with JSON formatter
  - More verbose but familiar to many developers

### Log Management and Analysis (Free Tiers)
- **Elastic Cloud (Free Tier)**:
  - Limited but usable for small applications
  - Requires managing Elasticsearch cluster
  
- **Graylog (Free/Open Source)**:
  - Self-hosted option
  - Good web interface for searching and dashboards
  
- **Loki + Grafana (Grafana Cloud Free Tier)**:
  - Loki for log aggregation
  - Grafana for visualization
  - Free tier has limits but good for development
  
- **Papertrail (Free Tier)**:
  - Simple log management
  - Limited retention but good for development
  
- **LogDNA (Free Tier)**:
  - Good UI, limited retention
  - Easy setup

### Metrics Collection and Monitoring
- **Prometheus (Self-hosted)**:
  - Industry standard for metrics
  - Requires setting up and maintaining server
  - Excellent query language (PromQL)
  
- **Grafana Cloud (Free Tier)**:
  - Hosted Prometheus and Grafana
  - Good limits for small applications
  - Easy setup
  
- **InfluxDB + Grafana**:
  - Time-series database with good visualization
  - Free tier available
  
- **AWS CloudWatch (Free Tier)**:
  - If using AWS services
  - Good integration with other AWS tools

### Distributed Tracing (Free Options)
- **Jaeger**:
  - Open source distributed tracing
  - Good UI for trace visualization
  - Requires setting up agent/collector
  
- **Zipkin**:
  - Another open source tracing option
  - Simpler than Jaeger in some ways
  
- **AWS X-Ray (Free Tier)**:
  - If using AWS
  - Good for serverless applications

### Health Checks and Uptime Monitoring
- **Kubernetes Liveness/Readiness Probes**:
  - If deploying to Kubernetes (even managed)
  
- **Docker HEALTHCHECK**:
  - Built-in Docker health checking
  
- **Custom Health Endpoints**:
  - /health/live, /health/ready in application
  - Check database, external services, etc.
  
- **UptimeRobot (Free Tier)**:
  - Monitor HTTP endpoints
  - Alert via email, Slack, etc.
  - 50 monitors free, 5-minute intervals
  
- **Better Uptime (Free Tier)**:
  - Similar to UptimeRobot
  - More features in free tier

### Alerting and Notification
- **Alertmanager** (with Prometheus):
  - Powerful alerting system
  - Requires Prometheus setup
  
- **Grafana Alerting**:
  - Built into Grafana
  - Works with Grafana Cloud free tier
  
- **IFTTT/Webhooks**:
  - Simple webhook-based alerting
  - Can connect to Slack, email, SMS, etc.
  
- **GitHub Actions**:
  - Can use workflow runs for monitoring/alerting
  - Limited but free for public/private repos

### Error Tracking and Exception Monitoring
- **Sentry (Free Tier)**:
  - Excellent for error tracking
  - Performance monitoring included
  - Generous free tier (5,000 events/month)
  - Supports Python, JavaScript, mobile
  
- **Rollbar (Free Tier)**:
  - Similar to Sentry
  - Good error grouping and tracking
  
- **Bugsnag (Free Tier)**:
  - Another error tracking option
  - Good mobile support

## Backup and Disaster Recovery Strategies

### Database Backup Strategies (PostgreSQL)

#### Logical Backups (pg_dump/pg_dumpall)
- **Pros**: Portable, human-readable, point-in-time
- **Cons**: Slower for large DBs, doesn't capture WAL
- **Frequency**: Daily for small/medium DBs
- **Retention**: Keep daily for week, weekly for month, monthly for year
- **Verification**: Regularly restore to test backup integrity
- **Compression**: Use gzip or similar to save space
- **Encryption**: Encrypt backups before offsite storage

#### Physical Base Backups (pg_basebackup)
- **Pros**: Faster for large DBs, captures exact state
- **Cons**: Larger files, requires WAL for PITR
- **Frequency**: Weekly base backup + continuous WAL archiving
- **Point-in-Time Recovery**: Combine base backup with WAL logs
- **Storage**: Need to store both base backups and WAL archives

#### Cloud-Native Backup Solutions
- **Supabase Built-in Backups**:
  - Automatic daily backups
  - Point-in-time recovery available
  - Retention depends on plan
  
- **Managed PostgreSQL Services**:
  - Most offer automated backups
  - Check RPO/RTO capabilities
  
- **Custom S3-based Backups**:
  - Upload pg_dump output to S3-compatible storage
  - Use lifecycle policies for automatic deletion
  - Consider Wasabi, Backblaze B2, or MinIO for S3-compatible

### Backup Testing and Validation
1. **Restore Testing**:
   - Regularly test restoring from backups
   - Test both logical and physical backups if using both
   - Validate data integrity after restore
   
2. **Recovery Time Objective (RTO)**:
   - Measure how long restore takes
   - Aim for RTO that meets business needs
   
3. **Recovery Point Objective (RPO)**:
   - Determine maximum acceptable data loss
   - Backup frequency should meet RPO
   
4. **Backup Verification**:
   - Check backup file integrity (checksums)
   - Test backup readability
   - Validate backup contains expected data

### Application and Configuration Backups
- **Infrastructure as Code**:
  - Store Terraform/CloudFormation in git
  - Treat as source of truth
  
- **Application Code**:
  - Already in git repository
  - Ensure proper branching and tagging
  
- **Configuration Files**:
  - Store in git or separate config repo
  - Use tools like Vault or AWS Secrets Manager for secrets
  
- **Container Images**:
  - Push to registry (Docker Hub, GitHub Packages, etc.)
  - Use immutable tags for reproducibility
  
- **Database Schema**:
  - Use Alembic migrations as source of truth
  - Consider exporting schema as backup

### Disaster Recovery Planning
1. **Risk Assessment**:
   - Identify potential failure points (DB, app, network, etc.)
   - Assess likelihood and impact
   
2. **Recovery Strategies**:
   - Database: Restore from backup + apply WAL
   - Application: Redeploy from container image
   - Infrastructure: Recreate from IaC
   - Data: Merge any lost data if possible
   
3. **Communication Plan**:
   - Stakeholder notification procedures
   - Status update frequency during outage
   - Post-mortem process
   
4. **Documentation**:
   - Runbooks for common recovery scenarios
   - Contact information for key personnel
   - Architecture diagrams and dependencies
   
5. **Testing**:
   - Regular disaster recovery drills
   - Test different failure scenarios
   - Update plans based on test results

### Specific Recommendations for $0/Month MVP
1. **Database**: Use Supabase free tier with their built-in backups
   - Verify backup frequency and retention
   - Consider manual exports as additional safety
   
2. **Application**: 
   - Container images stored in GitHub Packages (free for public repos)
   - or Docker Hub (free tier limits apply)
   - Source code in git (GitHub/GitLab/Bitbucket free tiers)
   
3. **Backups**:
   - Manual monthly pg_dump to personal storage (local drive, encrypted cloud)
   - Consider using rclone or similar for automated backups to free cloud storage
   - Test restore process quarterly
   
4. **Monitoring**:
   - Use UptimeRobot for basic availability monitoring
   - Use Sentry free tier for error tracking
   - Use GitHub Actions for simple CI/CD with security scanning
   
5. **Logging**:
   - Application logs to stdout/stderr (captured by platform)
   - Consider simple log rotation if self-hosted
   - Use structured logging for easier parsing if needed later

## Key Recommendations for MVP

### Testing Strategy
1. Start with unit tests for core business logic (calculators, validation, safety)
2. Add integration tests for API endpoints and critical workflows
3. Implement end-to-end tests for primary user journeys
4. Use pytest for backend, Jest/React Testing Library for frontend
5. Add Cypress or Playwright for E2E testing as complexity grows
6. Implement property-based testing for edge cases with hypothesis
7. Set up coverage reporting and aim for 80%+ on core logic
8. Test safety gateway extensively with both positive and negative cases
9. Mock external dependencies (LLM, vector store) in most tests
10. Include performance tests for critical paths as needed

### Security Scanning
1. Use safety for dependency scanning in CI/CD
2. Implement bandit for Python SAST
3. Use semgrep for custom security patterns
4. Scan container images with trivy in CI/CD
5. Use dependabot for automatic dependency updates
6. Add secret detection to pre-commit hooks
7. Schedule monthly full security scans
8. Track and remediate vulnerabilities promptly
9. Consider OWASP ZAP for periodic DAST testing
10. Implement security headers and CORS properly

### Logging and Monitoring
1. Use structlog for structured JSON logging
2. Implement health check endpoints (/health/live, /health/ready)
3. Use UptimeRobot (free tier) for basic uptime monitoring
4. Use Sentry (free tier) for error tracking and performance monitoring
5. Implement request logging with timing and status codes
6. Log safety decisions for audit and improvement
7. Monitor database connection pool usage
8. Set up alerts for error rate spikes or latency increases
9. Keep logs for minimum 30 days for debugging
10. Implement log rotation if self-hosting to prevent disk filling

### Backup and Disaster Recovery
1. Leverage Supabase built-in backups for primary DB protection
2. Schedule manual monthly logical backups as secondary protection
3. Store backups encrypted and offsite (personal cloud storage)
4. Test restore process quarterly to ensure viability
5. Document recovery procedures in team wiki
6. Implement soft deletes for critical user data where possible
7. Consider point-in-time recovery needs for compliance
8. Monitor backup success/failure and alert on failures
9. Keep critical secrets (API keys, etc.) out of backups or encrypt them
10. Plan for geographic redundancy if using multiple services

### DevOps and CI/CD
1. Set up GitHub Actions CI pipeline early
2. Implement dependency scanning in CI
3. Run tests on every push/pull request
4. Build and test Docker images in CI
5. Use Docker Compose for local development
6. Implement feature flags for risky changes
7. Use environment-specific configuration (dev/staging/prod)
8. Implement blue-green deployment strategy even on free tiers
9. Monitor deployment success and rollback capability
10. Keep infrastructure as code (even if simple bash scripts initially)

### Observability and Debugging
1. Implement correlation IDs for request tracing
2. Add timing middleware to measure request duration
3. Log slow requests (>1s) for performance investigation
4. Monitor external API call performance and error rates
5. Track user satisfaction metrics if possible (simple thumbs up/down)
6. Implement feature usage tracking for product decisions
7. Monitor error rates by endpoint and error type
8. Track database query performance and slow queries
9. Implement health checks for all external dependencies
10. Regularly review logs and metrics for improvement opportunities