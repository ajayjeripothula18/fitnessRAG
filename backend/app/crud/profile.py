from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.profile import Profile


async def get_profile_by_user_id(session: AsyncSession, user_id: int) -> Profile | None:
    result = await session.execute(select(Profile).where(Profile.user_id == user_id))
    return result.scalar_one_or_none()


async def update_profile(
    session: AsyncSession, user_id: int, profile_in: dict
) -> Profile | None:
    profile = await get_profile_by_user_id(session, user_id)
    if not profile:
        return None
    for field, value in profile_in.items():
        if hasattr(profile, field) and value is not None:
            setattr(profile, field, value)
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile
