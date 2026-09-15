# Priya (CPO) Research Findings

## FastAPI Best Practices

### Project Structure
- **Modular Structure**: Use `app/` containing `api/`, `core/`, `models/`, `schemas/`, `services/`, `utils/`
- **API Versioning**: `app/api/v1/` for versioned endpoints with clear separation
- **Dependency Injection**: Leverage FastAPI's built-in DI for database connections, services, and repositories
- **Configuration Management**: Use pydantic-settings for environment-based configuration
- **Separation of Concerns**: Routes handle HTTP, services handle business logic, models handle data

### Async Support and Performance
- **Async/Await**: Use async/await for I/O operations (database calls, HTTP requests) to improve concurrency
- **Database Drivers**: Use asyncpg for PostgreSQL to fully leverage async capabilities
- **External API Calls**: Use httpx.AsyncClient for non-blocking HTTP requests
- **Background Tasks**: Use FastAPI's BackgroundTasks for non-critical async operations
- **WebSocket Support**: Consider for real-time features if needed later

### Validation and Serialization
- **Pydantic v2**: Use for request/response models with proper field validation and serialization
- **Field Validation**: Use validators for complex validation logic (age ranges, etc.)
- **Custom Types**: Create custom types for domain-specific values (UUIDs, enums, etc.)
- **Exclusion Rules**: Use `response_model_exclude` to prevent sensitive data exposure
- **Examples**: Include examples in schema for better documentation

### Security Implementation
- **Authentication**: Use `fastapi.security` for OAuth2, API keys implementation
- **Rate Limiting**: Implement with `slowapi` or similar to prevent abuse
- **Input Validation**: Validate and sanitize all inputs to prevent injection attacks
- **CSRF Protection**: Implement for state-changing operations if using cookies
- **Security Headers**: Use middleware to add CSP, HSTS, X-Frame-Options, etc.
- **Secrets Management**: Use environment variables, never hardcode secrets
- **CORS**: Configure properly based on deployment environment

### Documentation and Testing
- **Auto-generated Docs**: Leverage OpenAPI/Swagger UI for testing and documentation
- **Custom Documentation**: Add descriptions, examples, and response codes
- **Testing Strategy**: Use `httpx.AsyncClient` for integration tests
- **Test Organization**: Separate unit, integration, and end-to-end tests
- **Fixtures**: Use pytest fixtures for database setup/teardown
- **Mocking**: Mock external services (LLM, vector store) in tests

### Deployment Considerations
- **ASGI Server**: Use `uvicorn` with appropriate worker count
- **Process Manager**: Consider `gunicorn` with uvicorn workers for production
- **Health Checks**: Implement liveness and readiness endpoints
- **Graceful Shutdown**: Handle SIGTERM properly for zero-downtime deployments
- **Logging**: Use structured logging (JSON format) for better observability
- **Exception Handling**: Custom exception handlers for consistent error responses

## LangGraph Patterns for Stateful Conversational Workflows

### State Design and Management
- **TypedDict State**: Use TypedDict for graph state with clear typing (messages, user_profile, active_plan, etc.)
- **Immutability**: Treat state updates as immutable where possible for predictability
- **State Size**: Keep state minimal and serializable to avoid performance issues
- **Pydantic Models**: Consider using Pydantic models for state validation and serialization
- **State Persistence**: Design state to be easily checkpointed and restored

### Node Architecture
- **Pure Functions**: Design nodes as pure functions that take state and return updated state
- **Single Responsibility**: Each node should have one clear purpose
- **Error Handling**: Nodes should handle their own errors or return error states
- **Logging**: Add appropriate logging within nodes for debugging
- **Testing**: Make nodes easily unit-testable with mock state

### Workflow Control Flow
- **Conditional Edges**: Use functions to determine routing based on state (safety check, RAG need, tool use)
- **Entry/Exit Points**: Clear definition of workflow start and end conditions
- **Subgraphs**: Use subgraphs for complex workflows (plan creation, modification, progress tracking)
- **Loops**: Implement controlled loops where needed (with proper exit conditions)
- **Interrupts**: Use `interrupt()` for actions requiring user approval (plan modifications)

### Persistence and Checkpointing
- **Checkpointer Selection**: 
  - Development: MemorySaver (simple, in-memory)
  - Production: PostgresSaver (persistent, scalable)
- **TTL Implementation**: Implement time-to-live for old conversation states
- **Storage Optimization**: Only persist necessary state components
- **Recovery**: Design for graceful recovery from checkpoint failures

### Advanced Features
- **Streaming Responses**: Implement streaming for LLM responses to improve UX
- **Human-in-the-Loop**: Use breakpoints and interrupts for user approval steps
- **Error Recovery**: Implement retry mechanisms and fallback nodes
- **Observability**: Add tracing and metrics collection within the graph
- **Dynamic Workflows**: Consider ability to modify workflow at runtime if needed

### Testing Strategies
- **Unit Testing**: Test individual nodes with various input states
- **Integration Testing**: Test complete workflows with mock external dependencies
- **Property-Based Testing**: Use hypothesis for edge case discovery
- **Mocking Strategy**: Mock LLM, vector store, and external services
- **State Snapshot Testing**: Consider snapshot testing for complex state changes

## pgvector Optimization Techniques

### Index Selection and Configuration
- **IVFFlat (Inverted File Index with Flat encoding)**:
  - Good balance of speed and accuracy for medium datasets
  - Tunable via `lists` parameter (number of centroids)
  - Faster build times than HNSW
  - Suitable for development and moderate production loads
  
- **HNSW (Hierarchical Navigable Small World)**:
  - Highest accuracy with reasonable query speed
  - Slower build times but excellent query performance
  - Good for production when accuracy is paramount
  - Tunable via `m` (connections per layer) and `ef_construction` parameters

- **Experimental**: Consider experimenting with both to determine optimal choice

### Index Maintenance and Monitoring
- **Regular Rebuilding**: Schedule index rebuilding during low-usage periods
- **Monitor Metrics**: Track query latency, recall rates, and index size
- **Concurrent Rebuilding**: Use `CONCURRENTLY` option to avoid downtime
- **Index Bloat**: Monitor and address index bloat over time
- **Statistics**: Keep PostgreSQL statistics updated for query planner

### Query Optimization Strategies
- **Appropriate Parameters**:
  - IVFFlat: Set `lists` ≈ sqrt(row_count) as starting point, tune based on performance
  - HNSW: Tune `ef_search` at query time for speed/accuracy tradeoff
  
- **Query Planning**: Use `EXPLAIN ANALYZE` to understand query execution
- **Work Memory**: Adjust `work_mem` setting for complex queries
- **Parallel Queries**: Enable and tune parallel query settings if beneficial

### Hybrid Search Implementation
- **Score Normalization**: Normalize vector and lexical scores to same scale before combining
- **Weighting Strategy**: Experiment with different weights (e.g., 0.7 vector, 0.3 lexical)
- **Rank Fusion**: Consider Reciprocal Rank Fusion (RRF) or similar techniques
- **PostgreSQL FTS**: Use `ts_rank` or `ts_rank_cd` for lexical scoring
- **Metadata Filtering**: Apply metadata filters BEFORE vector search to reduce search space

### Memory and Resource Management
- **Memory Monitoring**: Track memory usage of indexes and queries
- **Work_mem Settings**: Configure appropriately for complex operations
- **Maintenance Work_mem**: Set higher for index building operations
- **Temp File Limit**: Monitor temporary file usage during queries
- **Partitioning**: Consider partitioning large knowledge bases by topic or date

### Connection and Transaction Management
- **Connection Pooling**: Use effective connection pooling (SQLAlchemy pooling)
- **Transaction Size**: Keep transactions short to avoid lock contention
- **Read Replicas**: Consider for read-heavy workloads (if using managed PostgreSQL)
- **Prepared Statements**: Leverage for repeated similar queries
- **Statement Timeout**: Implement to prevent runaway queries

## Ollama LLM Performance Characteristics

### Model Selection Framework
- **Task-Specific Selection**:
  - Chat/QA: Llama 3 8B, Mistral 7B, Phi-3 medium
  - Structured Output: Models with strong JSON/function calling (Llama 3, Nemotron)
  - Embeddings: BGE-small-en-v1.5, Snowflake-arctic-embed-m, E5-large
  
- **Benchmarking**: Test models on representative fitness/nutrition queries
- **Latency vs Quality**: Measure time-to-first-token and overall response quality
- **Context Window**: Consider required context length for conversations

### Hardware and Resource Optimization
- **VRAM Requirements**: 
  - 8B model: ~4-6GB VRAM for Q4 quantization
  - 70B model: ~28-40GB VRAM (likely prohibitive for free tier)
  
- **RAM Overhead**: Allow 1.5x model size for context processing and overhead
- **CPU Optimization**: Ensure AVX2/AVX512 support for better CPU performance
- **Disk I/O**: Use SSD for faster model loading and swapping
- **GPU Utilization**: Monitor and optimize GPU memory usage if available

### Quantization Strategies
- **Quantization Levels**:
  - Q2_K: Smallest, lowest quality
  - Q3_K_M: Good balance for very constrained environments
  - Q4_K_M: Recommended default for good quality/speed
  - Q5_K_M: Better quality, higher resource usage
  - Q6_K: High quality, significant resource usage
  - F16: Near original quality, large size
  
- **Dynamic Quantization**: Consider if supported by Ollama/runtime
- **Mixed Precision**: Explore if beneficial for specific model architectures

### Concurrency and Scaling Approaches
- **Ollama Concurrency**: Native handling via queuing system
- **Multiple Instances**: Run multiple Ollama instances behind load balancer
- **Model Caching**: Ollama caches models; ensure sufficient RAM for hot models
- **Request Batching**: Implement where applicable for similar requests
- **Queue Monitoring**: Monitor queue depth and processing times

### Fallback and Resilience Patterns
- **Graceful Degradation**: Design to fallback to smaller models if needed
- **Circuit Breaker**: Implement to prevent cascading failures
- **Response Caching**: Cache frequent, non-personalized responses
- **Rate Limiting**: Implement per-user/IP rate limiting for LLM calls
- **Usage Monitoring**: Track token usage, latency, and error rates
- **Alerting**: Set up alerts for performance degradation or high error rates

### API Compatibility and Integration
- **OpenAI Compatibility**: Leverage Ollama's OpenAI-compatible API for easy switching
- **Streaming Support**: Implement streaming responses for better perceived performance
- **Function Calling**: Utilize Ollama's function calling capabilities for tool use
- **JSON Mode**: Use structured output modes when available for reliable parsing
- **Timeouts**: Implement appropriate timeouts for LLM calls
- **Retry Logic**: Add exponential backoff for transient failures

### Development and Testing Considerations
- **Local Development**: Design to work entirely with local Ollama for zero API cost
- **Model Switching**: Make model choice configurable via environment variables
- **Prompts Engineering**: Develop and test prompts specifically for selected models
- **Output Validation**: Validate and sanitize LLM outputs before use
- **Cost Tracking**: Even with local models, track resource usage for optimization
- **Continuous Evaluation**: Regularly re-evaluate model choices as new options emerge

## Key Recommendations for MVP Implementation

### FastAPI Implementation
1. Start with modular structure from day one (don't refactor later)
2. Implement environment-based configuration using pydantic-settings
3. Use asyncpg for PostgreSQL connectivity to enable true async
4. Set up structured logging with JSON format from the beginning
5. Implement health check endpoints (liveness, readiness)
6. Use dependency injection for database, services, and external clients
7. Add middleware for request logging, timing, and error handling
8. Configure CORS properly based on deployment environment
9. Implement rate limiting on authentication and sensitive endpoints
10. Use Pydantic v2 models with comprehensive validation

### LangGraph Implementation
1. Define clear state schema using TypedDict or Pydantic models
2. Implement nodes as pure, testable functions
3. Use conditional edges for workflow routing based on state
4. Implement persistence with PostgresSaver for production readiness
5. Add logging and error handling within each node
6. Design for human-in-the-loop where user approval is needed
7. Implement streaming responses for better UX with LLMs
8. Write unit tests for individual nodes early
9. Create integration tests for complete workflows
10. Consider subgraphs for complex workflows (plan creation, modification)

### Database and Vector Search
1. Choose IVFFlat index initially for development simplicity
2. Implement proper indexing on frequently queried columns
3. Design schema with UUIDs for security and distribution
4. Use JSONB for flexible data storage (plan data, preferences)
5. Implement hybrid search early but start with vector-only for simplicity
6. Add metadata filtering capability to reduce search space
7. Monitor query performance and adjust index parameters as needed
8. Consider connection pooling configuration for expected load
9. Implement basic full-text search capabilities alongside vector search
10. Plan for index maintenance and monitoring from the start

### LLM Integration Strategy
1. Start with Llama 3 8B via Ollama for local development
2. Implement abstraction layer for easy provider switching
3. Design for local-first operation with optional cloud fallback
4. Implement response caching for non-personalized queries
5. Add usage monitoring and alerting for resource tracking
6. Implement structured output (JSON mode) for reliable parsing
7. Add timeout and retry mechanisms for LLM calls
8. Consider implementing request batching for similar queries
9. Design prompts specifically for selected model capabilities
10. Implement output validation and sanitization before use