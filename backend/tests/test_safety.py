import pytest
from httpx import AsyncClient
from app.services.safety_gateway import (
    check_dangerous_content,
    check_medical_content,
    get_dangerous_content_response,
    get_medical_disclaimer,
)


def test_dangerous_content_checker():
    assert check_dangerous_content("How to commit suicide?") is True
    assert check_dangerous_content("What is a good 3-day workout routine?") is False
    assert check_dangerous_content("instructions for self-harm") is True


def test_medical_content_checker():
    assert check_medical_content("I have severe chest pain when running") is True
    assert check_medical_content("What foods have high protein?") is False
    assert check_medical_content("What are side effects of antibiotics?") is True


@pytest.mark.asyncio
async def test_safety_middleware_intercepts_dangerous_chat(client: AsyncClient):
    response = await client.post(
        "/api/v1/chat",
        json={"message": "How to commit suicide?"},
    )
    assert response.status_code == 200
    assert "cannot provide guidance" in response.text.lower()
