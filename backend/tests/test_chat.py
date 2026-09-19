import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock


async def _get_auth_headers(client: AsyncClient, email: str = "chatuser@example.com"):
    # Attempt to register first; if it exists we ignore the 400 error.
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "mypassword123"},
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "mypassword123"},
    )
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_chat_message_success(client: AsyncClient):
    headers = await _get_auth_headers(client)

    with patch("app.api.v1.chat.get_graph") as mock_get_graph:
        from unittest.mock import AsyncMock

        mock_graph = MagicMock()
        mock_graph.ainvoke = AsyncMock(
            return_value={
                "response": "Here is a safe response.",
                "citations": [
                    {
                        "index": 1,
                        "title": "Test Doc",
                        "url": "http://test",
                        "page": None,
                    }
                ],
                "safety_tier": "safe",
            }
        )
        mock_get_graph.return_value = mock_graph

        response = await client.post(
            "/api/v1/chat/message",
            json={"message": "How do I start lifting?", "history": []},
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "Here is a safe response."
        assert len(data["citations"]) == 1
        assert data["citations"][0]["title"] == "Test Doc"
        assert "conversation_id" in data


@pytest.mark.asyncio
async def test_chat_message_history(client: AsyncClient):
    headers = await _get_auth_headers(client, "user2@example.com")

    with patch("app.api.v1.chat.get_graph") as mock_get_graph:
        from unittest.mock import AsyncMock

        mock_graph = MagicMock()
        mock_graph.ainvoke = AsyncMock(
            return_value={
                "response": "Here is a safe response.",
                "citations": [],
                "safety_tier": "safe",
            }
        )
        mock_get_graph.return_value = mock_graph

        # Turn 1
        resp1 = await client.post(
            "/api/v1/chat/message",
            json={"message": "First message", "history": []},
            headers=headers,
        )
        assert resp1.status_code == 200
        conv_id = resp1.json()["conversation_id"]

        # Turn 2
        resp2 = await client.post(
            "/api/v1/chat/message",
            json={
                "message": "Second message",
                "conversation_id": conv_id,
                "history": [{"role": "user", "content": "First message"}],
            },
            headers=headers,
        )
        assert resp2.status_code == 200
        assert resp2.json()["conversation_id"] == conv_id

        # Get history
        hist_resp = await client.get(f"/api/v1/chat/history/{conv_id}", headers=headers)
        assert hist_resp.status_code == 200
        hist_data = hist_resp.json()
        assert hist_data["conversation_id"] == conv_id
        assert len(hist_data["messages"]) == 4  # user1, ai1, user2, ai2


@pytest.mark.asyncio
async def test_chat_graph_failure(client: AsyncClient):
    headers = await _get_auth_headers(client, "user3@example.com")

    with patch("app.api.v1.chat.get_graph") as mock_get_graph:
        from unittest.mock import AsyncMock

        mock_graph = MagicMock()
        mock_graph.ainvoke = AsyncMock(
            side_effect=Exception("Ollama connection refused")
        )
        mock_get_graph.return_value = mock_graph

        response = await client.post(
            "/api/v1/chat/message",
            json={"message": "Fail me", "history": []},
            headers=headers,
        )

        assert response.status_code == 503
        assert "temporarily unavailable" in response.json()["detail"]
