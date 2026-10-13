from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    UniqueConstraint,
    Index,
    Float,
    CheckConstraint,
    text,
)
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class WorkoutPlan(BaseModel):
    __tablename__ = "workout_plans"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    plan_identifier = Column(String(255), nullable=False)
    version = Column(Integer, nullable=False, default=1, server_default=text("1"))
    is_active = Column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    goal = Column(
        String(100), nullable=True
    )  # e.g., weight_loss, muscle_gain, endurance
    change_reason = Column(Text, nullable=True)  # Reason for creating a new version

    # Relationships
    user = relationship("User", back_populates="workout_plans", lazy="selectin")
    plan_days = relationship(
        "PlanDay",
        back_populates="workout_plan",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint(
            "plan_identifier", "version", name="uq_workoutplan_plan_identifier_version"
        ),
        CheckConstraint("version > 0", name="ck_workoutplan_positive_version"),
        Index(
            "ix_workoutplan_user_plan_active",
            "plan_identifier",
            postgresql_where=text("is_active = true"),
            unique=True,
            postgresql_using="btree",
        ),
    )


class PlanDay(BaseModel):
    __tablename__ = "plan_days"

    workout_plan_id = Column(
        Integer, ForeignKey("workout_plans.id", ondelete="CASCADE"), nullable=False
    )
    day_number = Column(
        Integer, nullable=False
    )  # Day number within the plan (1, 2, 3, etc.)
    name = Column(String(100), nullable=False)  # e.g., "Monday", "Day 1", "Rest Day"
    description = Column(Text, nullable=True)
    focus = Column(String(200), nullable=True)  # e.g., "Upper Body", "Cardio", "Legs"
    order_idx = Column(Integer, nullable=False)  # Order of days in the plan

    # Relationships
    workout_plan = relationship(
        "WorkoutPlan", back_populates="plan_days", lazy="selectin"
    )
    plan_exercises = relationship(
        "PlanExercise",
        back_populates="plan_day",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint(
            "workout_plan_id", "day_number", name="uq_planday_workoutplan_day_number"
        ),
        UniqueConstraint(
            "workout_plan_id", "order_idx", name="uq_planday_workoutplan_order_idx"
        ),
        CheckConstraint("day_number > 0", name="ck_planday_positive_day_number"),
        CheckConstraint("order_idx >= 0", name="ck_planday_nonnegative_order_idx"),
    )


class PlanExercise(BaseModel):
    __tablename__ = "plan_exercises"

    plan_day_id = Column(
        Integer, ForeignKey("plan_days.id", ondelete="CASCADE"), nullable=False
    )
    exercise_name = Column(String(255), nullable=False)
    target_sets = Column(Integer, nullable=False)  # Number of sets
    target_reps = Column(String(50), nullable=False)  # e.g., "8-10", "12", "AMRAP"
    target_weight_kg = Column(Float, nullable=True)  # Weight in kilograms
    rest_seconds = Column(Integer, nullable=True)  # Rest time between sets in seconds
    order_idx = Column(Integer, nullable=False)  # Order of exercises within the day
    notes = Column(Text, nullable=True)  # Additional notes

    # Relationships
    plan_day = relationship("PlanDay", back_populates="plan_exercises", lazy="selectin")

    # Constraints
    __table_args__ = (
        UniqueConstraint(
            "plan_day_id", "order_idx", name="uq_planexercise_plan_day_order_idx"
        ),
        CheckConstraint("target_sets > 0", name="ck_planexercise_positive_sets"),
        CheckConstraint("rest_seconds >= 0", name="ck_planexercise_nonnegative_rest"),
    )
