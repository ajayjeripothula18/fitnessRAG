"""LangGraph AI Pipeline — FitnessRAG Agent (Ravi – Checkpoint 4)

StateGraph flow:
  [START]
    │
    ▼
  safety_check          ← 3-tier input classification
    │ safe                   │ unsafe
    ▼                        ▼
  retrieve              [reject / disclaimer node]
    │
    ▼
  generate              ← Ollama LLM with retrieved context + citations
    │
    ▼
  output_safety         ← validate LLM output before returning
    │
    ▼
  [END]
"""
from __future__ import annotations

import logging
import time
from typing import TypedDict, Union

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph

from app.core.config import settings
from app.services.retrieval import RetrievedChunk
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Graph State
# ---------------------------------------------------------------------------


class AgentState(TypedDict):
    """Shared state object that flows through every graph node."""

    # Inputs
    user_query: str
    conversation_history: list[dict]  # [{"role": "user"|"assistant", "content": "..."}]
    db: Session  # SQLAlchemy Session (injected by caller)

    # Safety
    safety_tier: str  # "safe" | "medical" | "dangerous"
    safety_message: str  # pre-formed response for non-safe queries

    # Retrieval
    retrieved_chunks: list[RetrievedChunk]

    # Generation
    response: str
    citations: list[dict]  # [{"title": ..., "url": ..., "page": ...}]

    # Control
    skip_generation: bool  # True when safety blocks the query


# ---------------------------------------------------------------------------
# LLM Client
# ---------------------------------------------------------------------------


def _get_llm():
    primary_llm = ChatOllama(
        model=settings.OLLAMA_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=0.7,
        num_predict=1024,
        timeout=settings.OLLAMA_TIMEOUT,
    )

    if settings.OPENAI_API_KEY:
        try:
            from langchain_openai import ChatOpenAI  # type: ignore[import]
            from langchain_core.runnables import RunnableLambda
            import httpx

            fallback_llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                api_key=settings.OPENAI_API_KEY,
                temperature=0.7,
                max_tokens=1024,
            )

            def log_fallback(input_val, config, **kwargs):
                logger.warning("Ollama primary LLM failed. Triggering OpenAI fallback.")
                return fallback_llm.invoke(input_val, config=config, **kwargs)

            # Apply fallback to primary LLM
            return primary_llm.with_fallbacks(
                [RunnableLambda(log_fallback)],
                exceptions_to_handle=(
                    TimeoutError,
                    httpx.TimeoutException,
                    httpx.ConnectError,
                ),
            )
        except ImportError:
            logger.warning(
                "langchain_openai not installed. Cannot configure OpenAI fallback."
            )

    return primary_llm


# ---------------------------------------------------------------------------
# Node: Safety Check
# ---------------------------------------------------------------------------
_DANGEROUS_KEYWORDS = {
    "suicide",
    "self-harm",
    "overdose",
    "anorexia",
    "bulimia",
    "steroid injection",
    "doping",
    "drug abuse",
}
_MEDICAL_KEYWORDS = {
    "diagnose",
    "diagnosis",
    "prescription",
    "medication",
    "surgery",
    "disease",
    "disorder",
    "chronic",
    "cancer",
    "diabetes",
    "heart attack",
    "blood pressure medication",
    "clinical trial",
}


def node_safety_check(state: AgentState) -> AgentState:
    """Classify the user query into safety tier."""
    query_lower = state["user_query"].lower()

    if any(kw in query_lower for kw in _DANGEROUS_KEYWORDS):
        logger.warning("Dangerous query blocked: %.80s", state["user_query"])
        return {
            **state,
            "safety_tier": "dangerous",
            "safety_message": (
                "I'm not able to assist with that request. "
                "If you're struggling, please contact a qualified medical professional "
                "or a crisis helpline immediately."
            ),
            "skip_generation": True,
        }

    if any(kw in query_lower for kw in _MEDICAL_KEYWORDS):
        logger.info("Medical query — adding disclaimer.")
        return {
            **state,
            "safety_tier": "medical",
            "safety_message": (
                "⚠️ I can provide general fitness information, but this touches on a "
                "medical topic. Please consult a qualified healthcare professional for "
                "personalised medical advice."
            ),
            "skip_generation": False,
        }

    return {
        **state,
        "safety_tier": "safe",
        "safety_message": "",
        "skip_generation": False,
    }


# ---------------------------------------------------------------------------
# Node: Retrieve
# ---------------------------------------------------------------------------


def node_retrieve(state: AgentState) -> AgentState:
    """Hybrid retrieval: vector + BM25 + RRF fusion."""
    if state.get("skip_generation"):
        return {**state, "retrieved_chunks": []}

    from app.services.retrieval import retrieve

    try:
        chunks = retrieve(state["user_query"], state["db"])
    except Exception as exc:
        logger.error("Retrieval failed: %s", exc)
        chunks = []

    return {**state, "retrieved_chunks": chunks}


# ---------------------------------------------------------------------------
# Node: Generate
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """\
You are FitnessCoach AI, a knowledgeable and encouraging fitness assistant.
Your role is to provide accurate, science-backed fitness advice based ONLY on
the reference material provided below.

Guidelines:
- Be concise, motivating, and evidence-based.
- Cite your sources using [Source N] notation when referencing context.
- If the context does not contain enough information, say so honestly.
- Do NOT provide medical diagnoses or prescriptions.
- Always encourage the user to consult a professional for medical concerns.

Reference material:
{context}
"""


def node_generate(state: AgentState) -> AgentState:
    """Generate a response using the LLM with retrieved context."""
    if state.get("skip_generation"):
        return {**state, "response": state["safety_message"], "citations": []}

    chunks = state["retrieved_chunks"]
    citations: list[dict] = []

    if chunks:
        context_parts = []
        for i, chunk in enumerate(chunks, start=1):
            context_parts.append(f"[Source {i}] {chunk.source_title}\n{chunk.content}")
            citations.append(
                {
                    "index": i,
                    "title": chunk.source_title,
                    "url": chunk.source_url,
                    "page": chunk.page_number,
                }
            )
        context = "\n\n---\n\n".join(context_parts)
    else:
        context = "No reference material available."

    messages: list[Union[HumanMessage, SystemMessage]] = [
        SystemMessage(content=_SYSTEM_PROMPT.format(context=context))
    ]
    for turn in state.get("conversation_history", []):
        if turn["role"] == "user":
            messages.append(HumanMessage(content=turn["content"]))
    messages.append(HumanMessage(content=state["user_query"]))

    try:
        start_time = time.time()
        llm = _get_llm()
        result = llm.invoke(messages)
        latency = time.time() - start_time
        response_text: str = result.content

        # Log usage if available
        usage = getattr(result, "usage_metadata", None) or result.response_metadata.get(
            "token_usage", "unknown"
        )
        logger.info("LLM generation succeeded in %.2fs. Usage: %s", latency, usage)
    except Exception as exc:
        logger.error("LLM generation failed: %s", exc)
        response_text = (
            "I'm having trouble connecting right now. Please try again in a moment."
        )

    if state.get("safety_tier") == "medical" and state.get("safety_message"):
        response_text = state["safety_message"] + "\n\n" + response_text

    return {**state, "response": response_text, "citations": citations}


# ---------------------------------------------------------------------------
# Node: Output Safety
# ---------------------------------------------------------------------------


def node_output_safety(state: AgentState) -> AgentState:
    """Lightweight output guard — redact if dangerous keywords appear in response."""
    response = state.get("response", "")
    for kw in _DANGEROUS_KEYWORDS:
        if kw in response.lower():
            logger.warning("Output safety: dangerous keyword in response — redacting.")
            return {
                **state,
                "response": "I'm not able to provide that information. Please consult a qualified professional.",
                "citations": [],
            }
    return state


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------


def route_after_safety(state: AgentState) -> str:
    return "output_safety" if state.get("safety_tier") == "dangerous" else "retrieve"


# ---------------------------------------------------------------------------
# Build the graph
# ---------------------------------------------------------------------------


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("safety_check", node_safety_check)
    graph.add_node("retrieve", node_retrieve)
    graph.add_node("generate", node_generate)
    graph.add_node("output_safety", node_output_safety)

    graph.add_edge(START, "safety_check")
    graph.add_conditional_edges(
        "safety_check",
        route_after_safety,
        {"retrieve": "retrieve", "output_safety": "output_safety"},
    )
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", "output_safety")
    graph.add_edge("output_safety", END)

    return graph.compile()


# Singleton — compile once at import time
_compiled_graph = None


def get_graph():
    """Return the compiled LangGraph agent (singleton)."""
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph
