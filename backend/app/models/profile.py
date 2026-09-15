from sqlalchemy import Column, String, Text, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Profile(BaseModel):
    __tablename__ = "profiles"

    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    # Basic info
    full_name = Column(String(255), nullable=True)
    age_range = Column(String(50), nullable=True)  # e.g., "25-34"
    sex = Column(String(20), nullable=True)  # male, female, other
    height_cm = Column(Integer, nullable=True)
    weight_kg = Column(Integer, nullable=True)
    fitness_level = Column(String(50), nullable=True)  # beginner, intermediate, advanced
    primary_goal = Column(String(100), nullable=True)  # weight_loss, muscle_gain, etc.
    # Preferences
    dietary_preference = Column(String(100), nullable=True)  # vegetarian, vegan, omnivore, etc.
    allergies = Column(Text, nullable=True)
    available_equipment = Column(Text, nullable=True)  # JSON or comma-separated
    workout_location = Column(String(50), nullable=True)  # home, gym, outdoors
    days_per_week = Column(Integer, nullable=True)
    session_duration_min = Column(Integer, nullable=True)
    food_preferences = Column(Text, nullable=True)
    food_dislikes = Column(Text, nullable=True)
    experience_exercises = Column(Text, nullable=True)

    # Relationship
    user = relationship("User", back_populates="profile")