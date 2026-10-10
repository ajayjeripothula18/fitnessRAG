from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.security import decode_token
from app.db.session import get_async_session
from app.models.user import User
from app.crud.user import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        raise credentials_exception
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    user = await get_user_by_email(session, email=email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user_from_refresh_token(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None or payload.get("type") != "refresh":
        raise credentials_exception
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    user = await get_user_by_email(session, email=email)
    if user is None:
        raise credentials_exception
    return user


async def get_ingestion_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency that verifies the current user is authorized for file ingestion.
    Checks if the user's email is in the INGESTION_ADMIN_EMAILS allowlist.
    """
    # Normalize email for comparison (lowercase, strip whitespace)
    normalized_email = current_user.email.lower().strip()

    # Check if allowlist is configured and contains the user's email
    allowed_emails = [
        email.lower().strip() for email in settings.INGESTION_ADMIN_EMAILS
    ]

    if not allowed_emails:
        # If allowlist is empty, deny by default
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ingestion functionality is not configured. Contact administrator.",
        )

    if normalized_email not in allowed_emails:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized for file ingestion",
        )

    # Additionally check that user is active and verified
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User email is not verified",
        )

    return current_user
