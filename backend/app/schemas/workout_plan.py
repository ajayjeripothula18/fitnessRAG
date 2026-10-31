"""Pydantic schemas for Workout Plan API.

This module defines request/response models for workout plan operations,
including custom validation for exercise repetitions, sets, and plan structure.
"""
from __future__ import annotations

import math
import re
from datetime import datetime
from typing import Optional, List, Sequence

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
    ConfigDict,
)


class PlanExerciseBase(BaseModel):
    """Base schema for a plan exercise."""

    exercise_name: str = Field(..., min_length=1, max_length=255)
    target_sets: int = Field(..., gt=0)
    target_reps: str = Field(..., min_length=1, max_length=50)
    rest_seconds: Optional[int] = Field(default=None, ge=0, le=600)
    target_weight_kg: Optional[float] = Field(default=None, ge=0)

    @field_validator("target_reps")
    @classmethod
    def validate_target_reps(cls, v: str) -> str:
        """Validate target_reps format.

        Accepts:
        - Positive integers: "12", "8"
        - Positive ranges: "8-10", "12-15"
        - "AMRAP" (case-insensitive)

        Rejects:
        - Time formats: "30s", "45sec"
        - Text without numbers: "reps", "to failure"
        - Zero: "0"
        - Negative values: "-5"
        - Inverted ranges: "10-8"
        """
        v = v.strip()

        # Check for AMRAP (case-insensitive)
        if v.upper() == "AMRAP":
            return v

        # Check for range format (e.g., "8-10")
        range_pattern = r"^(\d+)-(\d+)$"
        range_match = re.match(range_pattern, v)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2))
            if start <= 0 or end <= 0:
                raise ValueError("Range values must be positive integers")
            if start > end:
                raise ValueError("Range start must not exceed end (inverted range)")
            return v

        # Check for single positive integer
        if v.isdigit():
            value = int(v)
            if value <= 0:
                raise ValueError("Repetition count must be a positive integer")
            return v

        # Reject time formats (e.g., "30s", "45sec")
        if re.match(r"^\d+\s*(s|sec|min|m)$", v, re.IGNORECASE):
            raise ValueError(
                "Time-based formats (e.g., '30s') are not allowed; use rep counts or ranges"
            )

        # Reject text without numbers
        if not re.search(r"\d", v):
            raise ValueError("Repetition string must contain numeric values or 'AMRAP'")

        # If we get here, it's an invalid format
        raise ValueError(
            "Invalid format; expected positive integer, range (e.g., '8-10'), or 'AMRAP'"
        )

    @field_validator("target_weight_kg")
    @classmethod
    def validate_target_weight_kg(cls, v: Optional[float]) -> Optional[float]:
        """Validate target_weight_kg is non-negative and finite."""
        if v is not None:
            if not math.isfinite(v):
                raise ValueError("Weight must be a finite number")
            if v < 0:
                raise ValueError("Weight must be non-negative")
        return v

    @field_validator("rest_seconds")
    @classmethod
    def validate_rest_seconds(cls, v: Optional[int]) -> Optional[int]:
        """Validate rest_seconds is between 0 and 600."""
        if v is not None:
            if v < 0 or v > 600:
                raise ValueError("Rest seconds must be between 0 and 600")
        return v


class PlanExerciseCreate(PlanExerciseBase):
    """Schema for creating a plan exercise."""

    pass


class PlanExerciseResponse(PlanExerciseBase):
    """Schema for plan exercise response."""

    id: int
    order_idx: int
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PlanDayBase(BaseModel):
    """Base schema for a plan day."""

    day_number: int = Field(..., gt=0)
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    focus: Optional[str] = Field(default=None, max_length=200)
    exercises: Sequence[PlanExerciseBase] = Field(default_factory=list)


class PlanDayCreate(PlanDayBase):
    """Schema for creating a plan day."""

    pass


class PlanDayResponse(PlanDayBase):
    """Schema for plan day response."""

    id: int
    order_idx: int
    exercises: List[PlanExerciseResponse] = Field(
        default_factory=list, validation_alias="plan_exercises"
    )

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class WorkoutPlanCreate(BaseModel):
    """Schema for creating a workout plan."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    goal: Optional[str] = Field(default=None, max_length=100)
    days: List[PlanDayCreate] = Field(..., min_length=1)
    change_reason: Optional[str] = None

    @model_validator(mode="after")
    def validate_unique_day_numbers(self) -> "WorkoutPlanCreate":
        """Ensure day_number is unique across all plan days."""
        day_numbers = [day.day_number for day in self.days]
        if len(day_numbers) != len(set(day_numbers)):
            raise ValueError("Duplicate day_number values are not allowed")
        return self


class WorkoutPlanResponse(BaseModel):
    """Schema for workout plan response."""

    id: int
    plan_identifier: str
    version: int
    is_active: bool
    name: str
    description: Optional[str] = None
    goal: Optional[str] = None
    change_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    days: List[PlanDayResponse] = Field(
        default_factory=list, validation_alias="plan_days"
    )

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PlansListResponse(BaseModel):
    """Schema for paginated workout plans list response."""

    plans: List[WorkoutPlanResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class WorkoutPlanVersionResponse(BaseModel):
    """Schema for a single version in version history."""

    version: int
    is_active: bool
    created_at: datetime
    change_reason: Optional[str] = None


class VersionsHistoryResponse(BaseModel):
    """Schema for workout plan versions history response."""

    plan_identifier: str
    versions: List[WorkoutPlanVersionResponse]

    model_config = ConfigDict(from_attributes=True)
