from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user
from app.crud.profile import get_profile_by_user_id, update_profile
from app.crud.user import get_user_by_id
from app.db.session import get_async_session
from app.models.user import User
from app.schemas.auth import UserResponse
from app.schemas.user import ProfileCreate, ProfileUpdate, ProfileResponse

router = APIRouter()


@router.get("/me/profile", response_model=ProfileResponse)
async def read_own_profile(
    current_user: UserResponse = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Get current user's profile.
    """
    profile = await get_profile_by_user_id(session, user_id=current_user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    return profile


@router.put("/me/profile", response_model=ProfileResponse)
async def update_own_profile(
    profile_in: ProfileUpdate,
    current_user: UserResponse = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Update current user's profile.
    """
    profile = await update_profile(
        session, user_id=current_user.id, profile_in=profile_in.dict(exclude_unset=True)
    )
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    return profile


@router.get("/{user_id}", response_model=UserResponse)
async def read_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Get a specific user by ID (for demo purposes, normally you'd restrict this).
    """
    user = await get_user_by_id(session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
