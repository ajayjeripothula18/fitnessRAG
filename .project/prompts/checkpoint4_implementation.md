# Implementation Prompt: Checkpoint 4 (AI & Knowledge Retrieval)

## Context
Based on the latest team meeting decisions:
1. We are keeping LangGraph but simplifying the retrieval process to just vector search + basic safety check for the MVP. (Hybrid search/RRF will be added in later sprints).
2. We are adding a managed LLM fallback (OpenAI/Anthropic) with timeout/retry logic to our LangGraph/Ollama setup.

## Tasks for Claude Code

### 1. Simplify Retrieval (`backend/app/services/retrieval.py`)
- Remove BM25 and RRF logic (`_bm25_rank`, `_rrf_merge`, and related imports like `rank_bm25`).
- Update the `retrieve` function to only execute `_vector_search`.
- Modify `_vector_search` to return similarity scores alongside `DocumentChunk`s.
- Update the `RetrievedChunk` dataclass to store `vector_score` (similarity score) instead of `rrf_score`.
- Add basic observability logging for retrieval latency (time taken for vector search).

### 2. Add LLM Fallback & Observability (`backend/app/ai/graph.py`)
- Update the `_get_llm()` function to use LangChain's `.with_fallbacks()`:
  - **Primary**: `ChatOllama` with a configurable timeout from settings (e.g., 5 seconds) to trigger fast failovers.
  - **Fallback**: `ChatOpenAI` (e.g., `model="gpt-3.5-turbo"`, `temperature=0.7`).
- **Fallback Trigger Specifics**: Configure the fallback to trigger specifically on `TimeoutError`, `httpx.TimeoutException`, and `httpx.ConnectError` using the `exceptions_to_handle` parameter in `.with_fallbacks()`.
- **Observability Logging**: Add logging for:
  - LLM call latency (duration of primary and/or fallback requests).
  - Token usage statistics.
  - Fallback events (log a warning when a fallback is triggered, including the exception that caused it).
- Ensure `ChatOpenAI` is imported from `langchain_openai`.

### 3. Update Settings (`backend/app/core/config.py`)
- Add `OPENAI_API_KEY` to the application settings. Make it **optional** so the app can run without it if Ollama is available.
- Add an `OLLAMA_TIMEOUT` setting (default `5.0` seconds).
- Add validation logic (e.g., in an `__init__` or validation hook) to ensure at least one LLM provider (Ollama URL or OpenAI API key) is configured.

## Verification & Testing
- Run backend tests to ensure `retrieve` works correctly with only vector search.
- Test the fallback mechanism by deliberately mocking an Ollama failure (e.g., setting a very low timeout or invalid URL) and verifying it gracefully falls back to OpenAI.
- Verify that latency and token usage logs appear during standard conversation queries.
