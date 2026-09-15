from pydantic import BaseModel, Field
from typing import Optional
from pydantic.config import ConfigDict


class ProfileBase(BaseModel):
    full_name: Optional[str] = None
    age_range: Optional[str] = None
    sex: Optional[str] = None
    height_cm: Optional[int] = None
    weight_kg: Optional[int] = None
    fitness_level: Optional[str] = None
    primary_goal: Optional[str] = None
    dietary_preference: Optional[str] = None
    allergies: Optional[str] = None
    available_equipment: Optional[str] = None
    workout_location: Optional[str] = None
    days_per_week: Optional[int] = None
    session_duration_min: Optional[int] = None
    food_preferences: Optional[str] = None
    food_dislikes: Optional[str] = None
    experience_exercises: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ProfileCreate(ProfileBase):
    model_config = ConfigDict(from_attributes=True)


class ProfileUpdate(ProfileBase):
    model_config = ConfigDict(from_attributes=True)


class ProfileResponse(ProfileBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)