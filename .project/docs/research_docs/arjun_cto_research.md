# Arjun (CTO) Research Findings

## FastAPI Project Structure and Performance

### Modular Architecture
- Use `app/api/v1/` for versioned endpoints
- Separate concerns: routers, services, models, schemas, utils
- Use dependency injection for database, services, external APIs

### Performance Optimization
- Use `uvicorn` with `--workers` based on CPU cores
- Implement response compression (gzip)
- Use async database drivers (asyncpg for PostgreSQL)
- Cache frequently accessed data (Redis or in-memory for dev)
- Use connection pooling properly

### Security Best Practices
- Use HTTPS in production (even on free tiers via Render/Netlify TLS)
- Implement proper CORS policies
- Use security headers (via middleware)
- Validate and sanitize all inputs
- Use environment variables for secrets (never hardcode)

### Observability
- Structured logging (JSON format)
- Prometheus metrics endpoint
- Health check endpoints
- Distributed tracing consideration (OpenTelemetry)

## LangGraph Patterns

### State Management
- Keep state minimal and serializable
- Use immutable updates where possible
- Consider using Pydantic models for state validation

### Workflow Design
- Clear entry and exit points
- Use subgraphs for complex workflows (plan creation, modification)
- Implement proper error handling with fallback nodes
- Use streaming for LLM responses to improve perceived performance

### Persistence
- Use PostgresSaver for production-ready checkpointing
- Implement proper TTL for old conversations
- Consider archiving strategy for long-term storage

### Testing Strategies
- Unit test individual nodes with mock state
- Integration test complete workflows
- Property-based testing for edge cases
- Mock external dependencies (LLM, vector store)

## pgvector Indexing Strategies

### Index Selection
- Start with IVFFlat for development/testing
- Monitor performance metrics (query time, recall)
- Consider migrating to HNSW for production if needed

### Index Parameters
- IVFFlat: `lists` parameter = rows / 1000 (adjust based on testing)
- HNSW: `m` and `ef_construction` parameters affect build time/query speed

### Maintenance
- Schedule regular index rebuilding during low-usage periods
- Monitor index bloat
- Consider concurrent index rebuilding to avoid downtime

### Hybrid Search Optimization
- Use appropriate weights for vector vs lexical scores
- Experiment with reciprocal rank fusion or weighted sum
- Consider using PostgreSQL's `ts_rank_cd` for better lexical scoring

### Memory Management
- Monitor memory usage of indexes
- Consider partitioning large knowledge bases
- Use appropriate work_mem settings

## Ollama LLM Performance (CTO Perspective)

### Model Selection Criteria
- Latency vs quality trade-off
- Structured output capability (JSON mode)
- Tool/function calling reliability
- Context window size

### Hardware Considerations
- VRAM requirements for GPU inference
- CPU optimization with AVX2/AVX512
- RAM overhead for context processing
- Disk I/O for model loading

### Concurrency and Scaling
- Ollama handles concurrent requests via queuing
- Consider multiple Ollama instances behind load balancer for high concurrency
- Monitor GPU utilization and memory usage

### Optimization Techniques
- Use quantized models (Q4_K_M, Q5_K_M) for speed
- Enable GPU offloading if available
- Consider model caching strategies
- Implement request batching where applicable

### Fallback and Resilience
- Design graceful degradation to smaller models
- Implement circuit breaker pattern for LLM service
- Cache frequent responses where appropriate
- Monitor and alert on performance degradation

## Key Technical Recommendations
1. Start with simple monolith structure, refactor to microservices only if needed
2. Use feature flags for risky changes
3. Implement blue-green deployment strategy for zero-downtime updates
4. Use infrastructure as code (Terraform or similar) even for free tiers
5. Implement chaos engineering principles (simple version)
6. Design for observability from day one (logs, metrics, traces)
7. Plan for data migration early (use Alembic for schema migrations)
8. Implement API versioning from the start
9. Use contract testing for frontend-backend integration
10. Implement chaos monkey style tests for resilience