"""
Chat API Router — /api/v1/chat  (Ravi – Checkpoint 4)

Endpoints:
  POST /message   — Send a message, run the LangGraph pipeline, return AI response
  GET  /history   — Retrieve conversation message history for authenticated user
"""
from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from fastapi.concurrency import run_in_threadpool

from app.ai.graph import get_graph
from app.core.dependencies import get_current_user
from app.db.session import get_async_session, get_sync_session
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.auth import UserResponse
from app.schemas.chat import ChatRequest, ChatResponse, CitationSchema

logger = logging.getLogger(__name__)

router = APIRouter()


# ---------------------------------------------------------------------------
# POST /message — Main chat endpoint
# ---------------------------------------------------------------------------


@router.post("/message", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def send_message(
    payload: ChatRequest,
    current_user: UserResponse = Depends(get_current_user),
    async_db: AsyncSession = Depends(get_async_session),
    sync_db: Session = Depends(get_sync_session),
):
    """
    Process a user message through the LangGraph RAG pipeline and return the AI response.

    Steps:
    1. Create or retrieve the Conversation record (async).
    2. Persist the user Message (async).
    3. Invoke the LangGraph agent (synchronous — uses sync_db for retrieval).
    4. Persist the AI reply Message (async).
    5. Return ChatResponse with citations.
    """
    # --- Step 1: Resolve conversation ------------------------------------------
    if payload.conversation_id:
        result = await async_db.execute(
            select(Conversation).where(
                Conversation.id == payload.conversation_id,
                Conversation.user_id == current_user.id,
            )
        )
        conversation = result.scalars().first()
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or does not belong to current user.",
            )
    else:
        conversation = Conversation(user_id=current_user.id, title=payload.message[:80])
        async_db.add(conversation)
        await async_db.flush()  # get conversation.id

    # --- Step 2: Persist user message ------------------------------------------
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=payload.message,
    )
    async_db.add(user_message)
    await async_db.flush()  # get user_message.id

    # --- Step 3: Run LangGraph agent -------------------------------------------
    history = [{"role": t.role, "content": t.content} for t in payload.history]

    try:
        graph = get_graph()
        result = await run_in_threadpool(
            graph.invoke,
            {
                "user_query": payload.message,
                "conversation_history": history,
                "db": sync_db,
                # Initialise remaining state keys
                "safety_tier": "",
                "safety_message": "",
                "retrieved_chunks": [],
                "response": "",
                "citations": [],
                "skip_generation": False,
            },
        )
    except Exception as exc:
        logger.error("LangGraph invocation failed: %s", exc)
        await async_db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is temporarily unavailable. Please try again.",
        ) from exc

    ai_response: str = result.get("response", "")
    citations_raw: list[dict] = result.get("citations", [])
    safety_tier: str = result.get("safety_tier", "safe")

    # --- Step 4: Persist AI response -------------------------------------------
    ai_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=ai_response,
    )
    async_db.add(ai_message)
    await async_db.commit()
    await async_db.refresh(ai_message)

    # --- Step 5: Return --------------------------------------------------------
    return ChatResponse(
        conversation_id=conversation.id,
        message_id=ai_message.id,
        response=ai_response,
        citations=[CitationSchema(**c) for c in citations_raw],
        safety_tier=safety_tier,
    )


# ---------------------------------------------------------------------------
# GET /history — Return recent messages for a conversation
# ---------------------------------------------------------------------------


@router.get("/history/{conversation_id}", status_code=status.HTTP_200_OK)
async def get_history(
    conversation_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
    limit: int = 50,
):
    """
    Return the last `limit` messages for a conversation owned by the current user.
    """
    result = await db.execute(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id,
        )
    )
    conversation = result.scalars().first()
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found."
        )

    msg_result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .limit(limit)
    )
    messages = msg_result.scalars().all()

    return {
        "conversation_id": conversation_id,
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at,
            }
            for m in messages
        ],
    }
