"""
Unit tests for the LangGraph AI pipeline (Ravi – Checkpoint 4).

Each node is tested in isolation; graph compilation and routing are also tested.
All external calls (Ollama, DB) are mocked.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from app.ai.graph import (
    AgentState,
    _DANGEROUS_KEYWORDS,
    _MEDICAL_KEYWORDS,
    node_generate,
    node_output_safety,
    node_retrieve,
    node_safety_check,
    route_after_safety,
)


def _base_state(**overrides) -> AgentState:
    """Return a minimal valid AgentState for testing."""
    state: AgentState = {
        "user_query": "How many reps for hypertrophy?",
        "conversation_history": [],
        "db": MagicMock(),
        "safety_tier": "",
        "safety_message": "",
        "retrieved_chunks": [],
        "response": "",
        "citations": [],
        "skip_generation": False,
    }
    state.update(overrides)  # type: ignore[typeddict-item]
    return state


# ---------------------------------------------------------------------------
# node_safety_check
# ---------------------------------------------------------------------------


class TestNodeSafetyCheck:
    def test_safe_query(self):
        state = node_safety_check(
            _base_state(user_query="Best exercises for core strength?")
        )
        assert state["safety_tier"] == "safe"
        assert not state["skip_generation"]

    def test_dangerous_query_is_blocked(self):
        state = node_safety_check(
            _base_state(user_query="How to do a steroid injection?")
        )
        assert state["safety_tier"] == "dangerous"
        assert state["skip_generation"] is True
        assert "crisis helpline" in state["safety_message"]

    def test_medical_query_adds_disclaimer(self):
        state = node_safety_check(
            _base_state(user_query="Can I exercise after heart attack?")
        )
        assert state["safety_tier"] == "medical"
        assert not state["skip_generation"]
        assert "healthcare professional" in state["safety_message"]


# ---------------------------------------------------------------------------
# node_retrieve
# ---------------------------------------------------------------------------


class TestNodeRetrieve:
    def test_skips_when_blocked(self):
        state = _base_state(skip_generation=True)
        result = node_retrieve(state)
        assert result["retrieved_chunks"] == []

    @patch("app.services.retrieval.retrieve")
    def test_calls_retrieve_for_safe_query(self, mock_retrieve):
        mock_retrieve.return_value = [MagicMock()]
        state = _base_state(safety_tier="safe")
        result = node_retrieve(state)
        mock_retrieve.assert_called_once()
        assert len(result["retrieved_chunks"]) == 1

    @patch("app.services.retrieval.retrieve", side_effect=Exception("DB error"))
    def test_returns_empty_on_retrieval_error(self, _):
        state = _base_state(safety_tier="safe")
        result = node_retrieve(state)
        assert result["retrieved_chunks"] == []


# ---------------------------------------------------------------------------
# node_generate
# ---------------------------------------------------------------------------


class TestNodeGenerate:
    def test_returns_safety_message_when_blocked(self):
        state = _base_state(skip_generation=True, safety_message="Blocked.")
        result = node_generate(state)
        assert result["response"] == "Blocked."
        assert result["citations"] == []

    @patch("app.ai.graph._get_llm")
    def test_generates_response_with_chunks(self, mock_llm_factory):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(content="Great answer about fitness!")
        mock_llm_factory.return_value = mock_llm

        chunk = MagicMock()
        chunk.source_title = "Fitness Guide"
        chunk.source_url = "https://example.com"
        chunk.page_number = None
        chunk.content = "Exercise improves health."

        state = _base_state(retrieved_chunks=[chunk], safety_tier="safe")
        result = node_generate(state)

        assert "Great answer about fitness!" in result["response"]
        assert len(result["citations"]) == 1
        assert result["citations"][0]["title"] == "Fitness Guide"

    @patch("app.ai.graph._get_llm")
    def test_prepends_medical_disclaimer(self, mock_llm_factory):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(
            content="Moderate exercise is generally safe."
        )
        mock_llm_factory.return_value = mock_llm

        state = _base_state(
            safety_tier="medical",
            safety_message="⚠️ Consult a professional.",
            skip_generation=False,
        )
        result = node_generate(state)
        assert result["response"].startswith("⚠️ Consult a professional.")

    @patch("app.ai.graph._get_llm")
    def test_graceful_fallback_on_llm_error(self, mock_llm_factory):
        mock_llm_factory.side_effect = Exception("Ollama crashed")
        state = _base_state(retrieved_chunks=[], safety_tier="safe")
        result = node_generate(state)
        assert "trouble connecting" in result["response"]


# ---------------------------------------------------------------------------
# node_output_safety
# ---------------------------------------------------------------------------


class TestNodeOutputSafety:
    def test_passes_clean_response(self):
        state = _base_state(response="Great workout plan for beginners!")
        result = node_output_safety(state)
        assert result["response"] == "Great workout plan for beginners!"

    def test_redacts_dangerous_response(self):
        state = _base_state(response="Here is how to do self-harm safely...")
        result = node_output_safety(state)
        assert "I'm not able to provide" in result["response"]
        assert result["citations"] == []


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------


class TestRouting:
    def test_dangerous_routes_to_output_safety(self):
        state = _base_state(safety_tier="dangerous")
        assert route_after_safety(state) == "output_safety"

    def test_safe_routes_to_retrieve(self):
        state = _base_state(safety_tier="safe")
        assert route_after_safety(state) == "retrieve"

    def test_medical_routes_to_retrieve(self):
        state = _base_state(safety_tier="medical")
        assert route_after_safety(state) == "retrieve"


# ---------------------------------------------------------------------------
# Graph compilation smoke test
# ---------------------------------------------------------------------------


class TestGraphCompilation:
    def test_graph_compiles_without_error(self):
        from app.ai.graph import build_graph

        graph = build_graph()
        assert graph is not None
