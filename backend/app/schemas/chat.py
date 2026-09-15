"""Pydantic schemas for the Chat API (Ravi – Checkpoint 4)."""
from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class ConversationTurn(BaseModel):
    """A single turn in the conversation history."""

    role: str = Field(..., pattern="^(user|assistant)$")
    content: str = Field(..., min_length=1, max_length=8192)


class ChatRequest(BaseModel):
    """Request body for POST /api/v1/chat/message."""

    message: str = Field(..., min_length=1, max_length=4096, description="User's fitness question.")
    conversation_id: Optional[int] = Field(None, description="Existing conversation ID for multi-turn chat.")
    history: list[ConversationTurn] = Field(
        default_factory=list,
        max_length=20,  # Limit history depth to control context window
        description="Recent conversation turns for multi-turn context.",
    )


class CitationSchema(BaseModel):
    """A source citation linked in the AI response."""

    index: int
    title: str
    url: str
    page: Optional[int] = None


class ChatResponse(BaseModel):
    """Response body for POST /api/v1/chat/message."""

    conversation_id: int
    message_id: int
    response: str
    citations: list[CitationSchema]
    safety_tier: str = Field(..., description="'safe' | 'medical' | 'dangerous'")
