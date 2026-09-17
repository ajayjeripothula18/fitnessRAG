# ADR-002: AI Architecture — LangGraph + Safety-First Design
## Created by Arjun (CTO)
## Status: Accepted
## Date: 2026-08-31

---

## Context

FitnessRAG requires an AI system that can:
1. Answer fitness/nutrition questions using a curated knowledge base (RAG)
2. Generate personalized workout plans based on user profiles
3. Maintain multi-turn conversation context
4. Route different intents (chat, plan generation, workout logging)
5. Enforce safety guardrails at every step (medical/harmful content filtering)
6. Support streaming responses for good UX

We need an architecture that handles these requirements while being maintainable, testable, and extensible.

## Decision

### LangGraph as AI Orchestration Layer

We will use **LangGraph** for stateful, graph-based AI workflow orchestration rather than simple chain-based LangChain pipelines.

### Conversation Graph Design

```
                    ┌───────────────┐
                    │   User Input  │
                    └───────┬───────┘
                            │
                    ┌───────▼───────┐
                    │    Safety     │
                    │   Pre-Check   │ ◄── DETERMINISTIC (no LLM)
                    └───────┬───────┘
                            │
                  ┌─────────┼──────────┐
                  ▼         ▼          ▼
              BLOCKED    MEDICAL     SAFE
              (return)   (flag +     (continue)
                         continue)
                            │
                    ┌───────▼───────┐
                    │    Intent     │
                    │    Router     │ ◄── LLM-powered classification
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │  Chat    │  │  Plan    │  │  Track   │
        │  Agent   │  │  Agent   │  │  Agent   │
        └────┬─────┘  └────┬─────┘  └────┬─────┘
             │              │              │
        ┌────▼─────┐  ┌────▼─────┐  ┌────▼─────┐
        │  RAG     │  │  Plan    │  │  Log     │
        │  Retrieve│  │  Generate│  │  Parser  │
        └────┬─────┘  └────┬─────┘  └────┬─────┘
             │              │              │
             └──────────────┼──────────────┘
                            │
                    ┌───────▼───────┐
                    │    Safety     │
                    │  Post-Check   │ ◄── DETERMINISTIC (no LLM)
                    └───────┬───────┘
                            │
                    ┌───────▼───────┐
                    │   Response    │
                    │   Formatter   │
                    └───────┬───────┘
                            │
                    ┌───────▼───────┐
                    │  Stream to    │
                    │  Client (SSE) │
                    └───────────────┘
```

### Graph State Schema

```python
from typing import TypedDict, Literal, Annotated
from langgraph.graph import add_messages

class ConversationState(TypedDict):
    # Core conversation state
    messages: Annotated[list, add_messages]
    user_id: str
    conversation_id: str
    
    # User context
    user_profile: dict  # Loaded from DB at conversation start
    active_plan: dict | None
    
    # Safety state
    safety_classification: Literal["SAFE", "MEDICAL", "HARMFUL", "OUT_OF_SCOPE"] | None
    safety_triggered_rules: list[str]
    safety_disclaimer: str | None
    
    # Intent routing
    detected_intent: Literal["chat", "plan_generate", "plan_modify", "workout_log", "memory_store"] | None
    
    # RAG state
    retrieved_documents: list[dict]
    source_citations: list[dict]
    
    # Plan generation state
    plan_preferences: dict | None
    generated_plan: dict | None
    
    # Tracking state
    parsed_workout_log: dict | None
    
    # Response
    final_response: str
    response_metadata: dict
```

### Safety-First Design Principle

The safety gateway is implemented as a **deterministic pre-processing step** (no LLM involved) that runs BEFORE any AI processing:

1. **Input Safety Check**: Rule-based keyword/pattern matching + Detoxify toxicity scoring
2. **All decisions are logged** to `safety_audit_logs` for review
3. **Output Safety Check**: Post-LLM scan for unintended medical advice or dangerous recommendations
4. **Exercise Contraindication Check**: Cross-reference recommended exercises against user profile

Key design choice: **Safety checks are NOT LLM-powered.** This ensures:
- Deterministic, reproducible behavior
- No hallucination in safety decisions
- Sub-200ms classification latency
- Testable with exact expected outputs

### Provider-Agnostic LLM Interface

```python
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, messages: list, **kwargs) -> AsyncIterator[str]:
        """Stream tokens from the LLM."""
        pass
    
    @abstractmethod
    async def generate_structured(self, messages: list, schema: type) -> dict:
        """Generate structured output matching a Pydantic schema."""
        pass

class OllamaProvider(LLMProvider):
    """Local Ollama inference — $0 cost."""
    pass

class OpenAIProvider(LLMProvider):
    """OpenAI API — for production/paid deployment."""
    pass

class AnthropicProvider(LLMProvider):
    """Anthropic API — alternative provider."""
    pass
```

Configuration via environment variable:
```
LLM_PROVIDER=ollama  # or "openai", "anthropic"
LLM_MODEL=llama3:8b  # or "gpt-4o-mini", "claude-3-haiku"
```

## Alternatives Considered

### Simple LangChain Chains (Rejected)
- **Pro**: Simpler to set up initially
- **Con**: No built-in state management for multi-turn conversations
- **Con**: Difficult to add conditional routing (intent → different processing paths)
- **Con**: No graph-level checkpointing or state persistence

### Custom Agent Framework (Rejected)
- **Pro**: Full control, no dependency
- **Con**: Significant development time to build state management, routing, persistence
- **Con**: Misses the portfolio value of demonstrating LangGraph expertise

### AutoGen / CrewAI (Rejected)
- **Pro**: Multi-agent capabilities
- **Con**: Overkill for our use case — we need routing, not autonomous agents
- **Con**: Less control over the exact conversation flow
- **Con**: Higher LLM token usage (agents talking to each other)

### LLM-Powered Safety (Rejected)
- **Pro**: More nuanced understanding of context
- **Con**: Non-deterministic — same input could give different safety decisions
- **Con**: Higher latency (LLM call adds 1-3s)
- **Con**: Higher cost (uses LLM tokens for every safety check)
- **Con**: Untestable — can't assert exact expected outputs

## Consequences

### Positive
- LangGraph provides clear, visual conversation flow (portfolio-impressive)
- Safety-first design demonstrates responsible AI development
- Provider-agnostic interface allows easy switching between free (Ollama) and paid APIs
- Graph state schema is self-documenting and type-safe
- Each graph node is independently testable

### Negative
- LangGraph adds a learning curve for developers unfamiliar with graph-based orchestration
- Graph state can grow large with many conversation turns (mitigated by sliding window)
- Debugging graph execution requires LangSmith or custom logging

### Risks
- **LangGraph API stability**: Relatively new library, API may change → Pin version, abstract behind internal interfaces
- **Local LLM quality**: 8B models may produce lower-quality plans → Validate with structured output schemas (Pydantic), fall back to templates
- **Context window management**: Long conversations may exceed model context → Implement sliding window with summarization

## References
- Technical Design: `/docs/technical_design.md` (Sections 3-5)
- Safety Gateway Spec: `/docs/safety_gateway_spec.md`
- LangGraph Documentation: https://langchain-ai.github.io/langgraph/
