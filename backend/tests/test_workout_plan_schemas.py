"""Pure unit tests for workout plan Pydantic schemas.

These tests validate the Pydantic schema validation logic without requiring
a database connection. They can run standalone.
"""
import pytest
from pydantic import ValidationError

from app.schemas.workout_plan import (
    PlanExerciseCreate,
    PlanExerciseResponse,
    PlanDayCreate,
    PlanDayResponse,
    WorkoutPlanCreate,
    WorkoutPlanResponse,
    PlansListResponse,
    WorkoutPlanVersionResponse,
    VersionsHistoryResponse,
)


class TestPlanExerciseCreate:
    """Tests for PlanExerciseCreate schema validation."""

    def test_valid_target_reps_positive_integer(self):
        """target_reps accepts positive integers like '12'."""
        exercise = PlanExerciseCreate(
            exercise_name="Push Up",
            target_sets=3,
            target_reps="12",
        )
        assert exercise.target_reps == "12"

    def test_valid_target_reps_range(self):
        """target_reps accepts positive ranges like '8-10'."""
        exercise = PlanExerciseCreate(
            exercise_name="Squat",
            target_sets=4,
            target_reps="8-10",
        )
        assert exercise.target_reps == "8-10"

    def test_valid_target_reps_amrap_uppercase(self):
        """target_reps accepts 'AMRAP'."""
        exercise = PlanExerciseCreate(
            exercise_name="Pull Up",
            target_sets=3,
            target_reps="AMRAP",
        )
        assert exercise.target_reps == "AMRAP"

    def test_valid_target_reps_amrap_lowercase(self):
        """target_reps accepts 'amrap' (case-insensitive)."""
        exercise = PlanExerciseCreate(
            exercise_name="Pull Up",
            target_sets=3,
            target_reps="amrap",
        )
        assert exercise.target_reps == "amrap"

    def test_invalid_target_reps_time_format(self):
        """target_reps rejects time formats like '30s'."""
        with pytest.raises(ValidationError) as exc_info:
            PlanExerciseCreate(
                exercise_name="Plank",
                target_sets=3,
                target_reps="30s",
            )
        assert "Time-based formats" in str(exc_info.value)

    def test_invalid_target_reps_text_without_numbers(self):
        """target_reps rejects text without numbers like 'reps'."""
        with pytest.raises(ValidationError) as exc_info:
            PlanExerciseCreate(
                exercise_name="Push Up",
                target_sets=3,
                target_reps="reps",
            )
        assert "must contain numeric values or 'AMRAP'" in str(exc_info.value)

    def test_invalid_target_reps_zero(self):
        """target_reps rejects '0'."""
        with pytest.raises(ValidationError) as exc_info:
            PlanExerciseCreate(
                exercise_name="Push Up",
                target_sets=3,
                target_reps="0",
            )
        assert "positive integer" in str(exc_info.value)

    def test_invalid_target_reps_negative(self):
        """target_reps rejects negative values like '-5'."""
        with pytest.raises(ValidationError) as exc_info:
            PlanExerciseCreate(
                exercise_name="Push Up",
                target_sets=3,
                target_reps="-5",
            )
        assert "positive integer" in str(exc_info.value)

    def test_invalid_target_reps_inverted_range(self):
        """target_reps rejects inverted ranges like '10-8'."""
        with pytest.raises(ValidationError) as exc_info:
            PlanExerciseCreate(
                exercise_name="Push Up",
                target_sets=3,
                target_reps="10-8",
            )
        assert "inverted range" in str(exc_info.value)

    def test_valid_target_sets_positive(self):
        """target_sets accepts positive integers."""
        exercise = PlanExerciseCreate(
            exercise_name="Push Up",
            target_sets=3,
            target_reps="10",
        )
        assert exercise.target_sets == 3

    def test_invalid_target_sets_zero(self):
        """target_sets rejects 0."""
        with pytest.raises(ValidationError) as exc_info:
            PlanExerciseCreate(
                exercise_name="Push Up",
                target_sets=0,
                target_reps="10",
            )
        assert "greater than 0" in str(exc_info.value)

    def test_invalid_target_sets_negative(self):
        """target_sets rejects negative values."""
        with pytest.raises(ValidationError) as exc_info:
            PlanExerciseCreate(
                exercise_name="Push Up",
                target_sets=-1,
                target_reps="10",
            )
        assert "greater than 0" in str(exc_info.value)

    def test_valid_rest_seconds_zero(self):
        """rest_seconds accepts 0."""
        exercise = PlanExerciseCreate(
            exercise_name="Push Up",
            target_sets=3,
            target_reps="10",
            rest_seconds=0,
        )
        assert exercise.rest_seconds == 0

    def test_valid_rest_seconds_600(self):
        """rest_seconds accepts 600."""
        exercise = PlanExerciseCreate(
            exercise_name="Push Up",
            target_sets=3,
            target_reps="10",
            rest_seconds=600,
        )
        assert exercise.rest_seconds == 600

    def test_invalid_rest_seconds_601(self):
        """rest_seconds rejects 601."""
        with pytest.raises(ValidationError) as exc_info:
            PlanExerciseCreate(
                exercise_name="Push Up",
                target_sets=3,
                target_reps="10",
                rest_seconds=601,
            )
        assert "less than or equal to 600" in str(exc_info.value) or "le=600" in str(exc_info.value)

    def test_invalid_rest_seconds_negative(self):
        """rest_seconds rejects -1."""
        with pytest.raises(ValidationError) as exc_info:
            PlanExerciseCreate(
                exercise_name="Push Up",
                target_sets=3,
                target_reps="10",
                rest_seconds=-1,
            )
        assert "greater than or equal to 0" in str(exc_info.value) or "ge=0" in str(exc_info.value)

    def test_valid_target_weight_kg_zero(self):
        """target_weight_kg accepts 0.0."""
        exercise = PlanExerciseCreate(
            exercise_name="Push Up",
            target_sets=3,
            target_reps="10",
            target_weight_kg=0.0,
        )
        assert exercise.target_weight_kg == 0.0

    def test_valid_target_weight_kg_none(self):
        """target_weight_kg accepts None."""
        exercise = PlanExerciseCreate(
            exercise_name="Push Up",
            target_sets=3,
            target_reps="10",
            target_weight_kg=None,
        )
        assert exercise.target_weight_kg is None

    def test_invalid_target_weight_kg_negative(self):
        """target_weight_kg rejects negative values."""
        with pytest.raises(ValidationError) as exc_info:
            PlanExerciseCreate(
                exercise_name='Push Up',
                target_sets=3,
                target_reps='10',
                target_weight_kg=-5.0,
            )
        assert 'greater than or equal to 0' in str(exc_info.value) or 'ge=0' in str(exc_info.value)

    def test_invalid_target_weight_kg_nan(self):
        """target_weight_kg rejects NaN (caught by ge=0 validator)."""
        with pytest.raises(ValidationError) as exc_info:
            PlanExerciseCreate(
                exercise_name='Push Up',
                target_sets=3,
                target_reps='10',
                target_weight_kg=float('nan'),
            )
        assert 'greater than or equal to 0' in str(exc_info.value)

    def test_invalid_target_weight_kg_inf(self):
        """target_weight_kg rejects infinity (passes ge=0 but caught by custom validator)."""
        with pytest.raises(ValidationError) as exc_info:
            PlanExerciseCreate(
                exercise_name='Push Up',
                target_sets=3,
                target_reps='10',
                target_weight_kg=float('inf'),
            )
        assert 'finite' in str(exc_info.value).lower()

    def test_invalid_target_weight_kg_negative_inf(self):
        """target_weight_kg rejects negative infinity (caught by ge=0 validator)."""
        with pytest.raises(ValidationError) as exc_info:
            PlanExerciseCreate(
                exercise_name='Push Up',
                target_sets=3,
                target_reps='10',
                target_weight_kg=float('-inf'),
            )
        assert 'greater than or equal to 0' in str(exc_info.value)


class TestPlanDayCreate:
    """Tests for PlanDayCreate schema validation."""

    def test_valid_day_number_positive(self):
        """day_number accepts positive integers."""
        day = PlanDayCreate(
            day_number=1,
            name="Day 1",
        )
        assert day.day_number == 1

    def test_invalid_day_number_zero(self):
        """day_number rejects 0."""
        with pytest.raises(ValidationError) as exc_info:
            PlanDayCreate(
                day_number=0,
                name="Day 1",
            )
        assert "greater than 0" in str(exc_info.value)

    def test_invalid_day_number_negative(self):
        """day_number rejects negative values."""
        with pytest.raises(ValidationError) as exc_info:
            PlanDayCreate(
                day_number=-1,
                name="Day 1",
            )
        assert "greater than 0" in str(exc_info.value)

    def test_valid_exercises_list(self):
        """exercises accepts a list of valid PlanExerciseCreate."""
        day = PlanDayCreate(
            day_number=1,
            name="Day 1",
            exercises=[
                PlanExerciseCreate(
                    exercise_name="Push Up",
                    target_sets=3,
                    target_reps="10",
                ),
                PlanExerciseCreate(
                    exercise_name="Squat",
                    target_sets=4,
                    target_reps="8-12",
                ),
            ],
        )
        assert len(day.exercises) == 2


class TestWorkoutPlanCreate:
    """Tests for WorkoutPlanCreate schema validation."""

    def test_valid_workout_plan(self):
        """Valid workout plan with all required fields."""
        plan = WorkoutPlanCreate(
            name="Test Plan",
            description="A test plan",
            goal="strength",
            days=[
                PlanDayCreate(
                    day_number=1,
                    name="Upper Body",
                    exercises=[
                        PlanExerciseCreate(
                            exercise_name="Bench Press",
                            target_sets=3,
                            target_reps="8-10",
                        ),
                    ],
                ),
                PlanDayCreate(
                    day_number=2,
                    name="Lower Body",
                    exercises=[
                        PlanExerciseCreate(
                            exercise_name="Squat",
                            target_sets=4,
                            target_reps="10",
                        ),
                    ],
                ),
            ],
            change_reason="Initial version",
        )
        assert plan.name == "Test Plan"
        assert len(plan.days) == 2

    def test_invalid_empty_days_list(self):
        """WorkoutPlanCreate raises ValidationError for empty days list."""
        with pytest.raises(ValidationError) as exc_info:
            WorkoutPlanCreate(
                name="Test Plan",
                days=[],
            )
        assert "at least 1" in str(exc_info.value) or "min_length" in str(exc_info.value)

    def test_invalid_duplicate_day_numbers(self):
        """WorkoutPlanCreate raises ValidationError for duplicate day_number."""
        with pytest.raises(ValidationError) as exc_info:
            WorkoutPlanCreate(
                name="Test Plan",
                days=[
                    PlanDayCreate(
                        day_number=1,
                        name="Day 1",
                    ),
                    PlanDayCreate(
                        day_number=1,  # Duplicate
                        name="Day 1 Again",
                    ),
                ],
            )
        assert "Duplicate day_number" in str(exc_info.value)

    def test_valid_single_day(self):
        """WorkoutPlanCreate accepts a single day."""
        plan = WorkoutPlanCreate(
            name="Test Plan",
            days=[
                PlanDayCreate(
                    day_number=1,
                    name="Full Body",
                    exercises=[
                        PlanExerciseCreate(
                            exercise_name="Deadlift",
                            target_sets=3,
                            target_reps="5",
                        ),
                    ],
                ),
            ],
        )
        assert len(plan.days) == 1


class TestResponseSchemas:
    """Tests for response schemas serialization."""

    def test_plan_exercise_response_serialization(self):
        """PlanExerciseResponse serializes correctly with from_attributes."""
        exercise = PlanExerciseResponse(
            id=1,
            exercise_name="Push Up",
            target_sets=3,
            target_reps="10",
            rest_seconds=60,
            target_weight_kg=0.0,
            order_idx=0,
            notes="Standard push up",
        )
        assert exercise.exercise_name == "Push Up"
        assert exercise.target_sets == 3

    def test_plan_day_response_serialization(self):
        """PlanDayResponse serializes correctly with from_attributes."""
        day = PlanDayResponse(
            id=1,
            day_number=1,
            name="Day 1",
            description="First day",
            focus="Upper Body",
            order_idx=0,
            exercises=[
                PlanExerciseResponse(
                    id=1,
                    exercise_name="Push Up",
                    target_sets=3,
                    target_reps="10",
                    rest_seconds=60,
                    target_weight_kg=0.0,
                    order_idx=0,
                ),
            ],
        )
        assert day.name == "Day 1"
        assert len(day.exercises) == 1

    def test_workout_plan_response_serialization(self):
        """WorkoutPlanResponse serializes correctly with from_attributes."""
        plan = WorkoutPlanResponse(
            id=1,
            plan_identifier="plan-123",
            version=1,
            is_active=True,
            name="Test Plan",
            description="A test plan",
            goal="strength",
            change_reason="Initial version",
            created_at="2024-01-01T00:00:00",
            updated_at="2024-01-01T00:00:00",
            days=[
                PlanDayResponse(
                    id=1,
                    day_number=1,
                    name="Day 1",
                    order_idx=0,
                    exercises=[],
                ),
            ],
        )
        assert plan.name == "Test Plan"
        assert len(plan.days) == 1

    def test_plans_list_response_serialization(self):
        """PlansListResponse serializes correctly."""
        response = PlansListResponse(
            plans=[
                WorkoutPlanResponse(
                    id=1,
                    plan_identifier="plan-1",
                    version=1,
                    is_active=True,
                    name="Plan 1",
                    created_at="2024-01-01T00:00:00",
                    updated_at="2024-01-01T00:00:00",
                    days=[],
                ),
            ],
            total=1,
            page=1,
            page_size=20,
            total_pages=1,
        )
        assert response.total == 1
        assert len(response.plans) == 1

    def test_workout_plan_version_response_serialization(self):
        """WorkoutPlanVersionResponse serializes correctly."""
        version = WorkoutPlanVersionResponse(
            version=1,
            is_active=True,
            created_at="2024-01-01T00:00:00",
            change_reason="Initial version",
        )
        assert version.version == 1
        assert version.is_active is True

    def test_versions_history_response_serialization(self):
        """VersionsHistoryResponse serializes correctly with from_attributes."""
        history = VersionsHistoryResponse(
            plan_identifier="plan-123",
            versions=[
                WorkoutPlanVersionResponse(
                    version=1,
                    is_active=False,
                    created_at="2024-01-01T00:00:00",
                    change_reason="Initial version",
                ),
                WorkoutPlanVersionResponse(
                    version=2,
                    is_active=True,
                    created_at="2024-01-02T00:00:00",
                    change_reason="Updated exercises",
                ),
            ],
        )
        assert history.plan_identifier == "plan-123"
        assert len(history.versions) == 2


class TestEdgeCases:
    """Additional edge case tests."""

    def test_exercise_name_max_length(self):
        """exercise_name accepts max 255 characters."""
        exercise = PlanExerciseCreate(
            exercise_name="A" * 255,
            target_sets=3,
            target_reps="10",
        )
        assert len(exercise.exercise_name) == 255

    def test_exercise_name_over_max_length(self):
        """exercise_name rejects over 255 characters."""
        with pytest.raises(ValidationError) as exc_info:
            PlanExerciseCreate(
                exercise_name="A" * 256,
                target_sets=3,
                target_reps="10",
            )
        assert "at most 255" in str(exc_info.value) or "String should have at most 255" in str(exc_info.value)

    def test_day_name_max_length(self):
        """PlanDayCreate name accepts max 100 characters."""
        day = PlanDayCreate(
            day_number=1,
            name="A" * 100,
        )
        assert len(day.name) == 100

    def test_plan_name_max_length(self):
        """WorkoutPlanCreate name accepts max 255 characters."""
        plan = WorkoutPlanCreate(
            name="A" * 255,
            days=[
                PlanDayCreate(
                    day_number=1,
                    name="Day 1",
                ),
            ],
        )
        assert len(plan.name) == 255

    def test_focus_max_length(self):
        """PlanDayCreate focus accepts max 200 characters."""
        day = PlanDayCreate(
            day_number=1,
            name="Day 1",
            focus="A" * 200,
        )
        assert len(day.focus) == 200

    def test_goal_max_length(self):
        """WorkoutPlanCreate goal accepts max 100 characters."""
        plan = WorkoutPlanCreate(
            name="Test Plan",
            goal="A" * 100,
            days=[
                PlanDayCreate(
                    day_number=1,
                    name="Day 1",
                ),
            ],
        )
        assert len(plan.goal) == 100

    def test_target_reps_whitespace_handling(self):
        """target_reps handles whitespace correctly (strips whitespace)."""
        exercise = PlanExerciseCreate(
            exercise_name="Push Up",
            target_sets=3,
            target_reps=" 8-10 ",
        )
        assert exercise.target_reps == "8-10"  # Whitespace is stripped by validator

    def test_amrap_case_insensitive(self):
        """AMRAP accepts various case combinations."""
        for variant in ["AMRAP", "amrap", "Amrap", "aMrAp"]:
            exercise = PlanExerciseCreate(
                exercise_name="Pull Up",
                target_sets=3,
                target_reps=variant,
            )
            assert exercise.target_reps == variant


class TestRegressionFixes:
    """Regression tests for Greptile findings fixes."""

    def test_workout_plan_response_datetime_serialization(self):
        """WorkoutPlanResponse serializes datetime fields to ISO format in JSON."""
        from datetime import datetime
        now = datetime.now()

        plan = WorkoutPlanResponse(
            id=1,
            plan_identifier="test-123",
            version=1,
            is_active=True,
            name="Test Plan",
            created_at=now,
            updated_at=now,
            days=[],
        )
        # Verify datetime fields are stored as datetime objects
        assert isinstance(plan.created_at, datetime)
        assert isinstance(plan.updated_at, datetime)
        # Verify JSON serialization produces ISO format strings
        json_data = plan.model_dump(mode="json")
        assert isinstance(json_data["created_at"], str)
        assert isinstance(json_data["updated_at"], str)
        # Verify the format is ISO-like (contains T separator)
        assert "T" in json_data["created_at"]
        assert "T" in json_data["updated_at"]

    def test_workout_plan_version_response_datetime_serialization(self):
        """WorkoutPlanVersionResponse serializes datetime field to ISO format in JSON."""
        from datetime import datetime
        now = datetime.now()

        version = WorkoutPlanVersionResponse(
            version=1,
            is_active=True,
            created_at=now,
            change_reason="Initial",
        )
        # Verify datetime field is stored as datetime object
        assert isinstance(version.created_at, datetime)
        # Verify JSON serialization produces ISO format string
        json_data = version.model_dump(mode="json")
        assert isinstance(json_data["created_at"], str)
        assert "T" in json_data["created_at"]

    def test_validation_alias_plan_days_to_days(self):
        """validation_alias maps plan_days (DB model) to days (response schema)."""
        from datetime import datetime
        now = datetime.now()

        # Create a mock object with plan_days attribute (as DB model would have)
        class MockPlanExercise:
            def __init__(self):
                self.id = 1
                self.exercise_name = "Push Up"
                self.target_sets = 3
                self.target_reps = "10"
                self.rest_seconds = 60
                self.target_weight_kg = 0.0
                self.order_idx = 0
                self.notes = "test"

        class MockPlanDay:
            def __init__(self):
                self.id = 1
                self.day_number = 1
                self.name = "Day 1"
                self.order_idx = 0
                self.description = None
                self.focus = None
                self.plan_exercises = [MockPlanExercise()]  # DB model uses plan_exercises

        class MockWorkoutPlan:
            def __init__(self):
                self.id = 1
                self.plan_identifier = "test-123"
                self.version = 1
                self.is_active = True
                self.name = "Test Plan"
                self.description = None
                self.goal = None
                self.change_reason = None
                self.created_at = now
                self.updated_at = now
                self.plan_days = [MockPlanDay()]  # DB model uses plan_days

        # This should work with validation_alias mapping plan_days -> days
        mock_plan = MockWorkoutPlan()
        plan = WorkoutPlanResponse.model_validate(mock_plan)

        assert len(plan.days) == 1
        assert plan.days[0].name == "Day 1"
        assert len(plan.days[0].exercises) == 1
        assert plan.days[0].exercises[0].exercise_name == "Push Up"

    def test_validation_alias_plan_exercises_to_exercises(self):
        """validation_alias maps plan_exercises (DB model) to exercises (response schema)."""
        from datetime import datetime
        now = datetime.now()

        # Create a mock object with plan_exercises attribute (as DB model would have)
        class MockPlanExercise:
            def __init__(self):
                self.id = 1
                self.exercise_name = "Squat"
                self.target_sets = 4
                self.target_reps = "8-12"
                self.rest_seconds = 90
                self.target_weight_kg = 60.0
                self.order_idx = 0
                self.notes = "Back squat"

        class MockPlanDay:
            def __init__(self):
                self.id = 1
                self.day_number = 1
                self.name = "Leg Day"
                self.order_idx = 0
                self.description = None
                self.focus = "Lower Body"
                self.plan_exercises = [MockPlanExercise()]  # DB model uses plan_exercises

        # This should work with validation_alias mapping plan_exercises -> exercises
        mock_day = MockPlanDay()
        day = PlanDayResponse.model_validate(mock_day)

        assert len(day.exercises) == 1
        assert day.exercises[0].exercise_name == "Squat"
        assert day.exercises[0].target_sets == 4
        assert day.exercises[0].target_reps == "8-12"