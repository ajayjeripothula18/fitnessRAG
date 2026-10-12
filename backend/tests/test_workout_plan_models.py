"""
Test workout plan models.
"""
import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text, select

from app.models.workout_plan import WorkoutPlan, PlanDay, PlanExercise


@pytest.mark.asyncio
async def test_create_workout_plan(db_session):
    """Test creating a workout plan."""
    # First we need a user; we can create a minimal user for testing.
    from app.models.user import User
    user = User(
        email="test@example.com",
        hashed_password="hashedpassword",
        is_active=True,
        is_verified=True,
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    workout_plan = WorkoutPlan(
        user=user,
        plan_identifier="test-plan-id",
        version=1,
        is_active=True,
        name="Test Plan",
        description="A test workout plan",
        goal="weight_loss",
        change_reason="Initial version",
    )
    db_session.add(workout_plan)
    await db_session.flush()
    await db_session.refresh(workout_plan)

    assert workout_plan.id is not None
    assert workout_plan.user is user
    assert workout_plan.plan_identifier == "test-plan-id"
    assert workout_plan.version == 1
    assert workout_plan.is_active is True
    assert workout_plan.name == "Test Plan"
    assert workout_plan.description == "A test workout plan"
    assert workout_plan.goal == "weight_loss"
    assert workout_plan.change_reason == "Initial version"
    assert workout_plan.created_at is not None
    assert workout_plan.updated_at is not None

    # Test relationship - verify user relationship via query (avoid MissingGreenlet in async)
    result = await db_session.execute(select(User).where(User.id == workout_plan.user_id))
    user_related = result.scalar_one_or_none()
    assert user_related is not None
    assert user_related.id == user.id

    # Test ORM relationship access - user relationship should be accessible via attribute
    # With lazy="selectin", accessing the attribute will trigger a load if not already loaded
    assert workout_plan.user is not None
    assert workout_plan.user.id == user.id
    assert workout_plan.user.email == "test@example.com"

    # Verify plan_days relationship via query (avoid MissingGreenlet in async)
    result = await db_session.execute(select(PlanDay).where(PlanDay.workout_plan_id == workout_plan.id))
    plan_days_related = result.scalars().all()
    assert len(plan_days_related) == 0

    # Test ORM relationship access - plan_days relationship should be accessible via attribute
    # With lazy="selectin", accessing the attribute will trigger a load if not already loaded
    assert workout_plan.plan_days == []  # Empty list since no days added yet

    # Test reverse relationship: User should have this workout plan in its workout_plans collection
    # With lazy="selectin", accessing the attribute will trigger a load if not already loaded
    assert len(user.workout_plans) == 1
    assert user.workout_plans[0].id == workout_plan.id
    assert user.workout_plans[0].plan_identifier == "test-plan-id"


@pytest.mark.asyncio
async def test_workout_plan_unique_constraint(db_session):
    """Test unique constraint on (plan_identifier, version)."""
    from app.models.user import User
    user = User(
        email="test2@example.com",
        hashed_password="hashedpassword",
        is_active=True,
        is_verified=True,
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    wp1 = WorkoutPlan(
        user_id=user.id,
        plan_identifier="same-id",
        version=1,
        is_active=False,
        name="Plan 1",
    )
    wp2 = WorkoutPlan(
        user_id=user.id,
        plan_identifier="same-id",
        version=1,  # same identifier and version
        is_active=False,
        name="Plan 2",
    )
    db_session.add(wp1)
    db_session.add(wp2)
    # Should raise IntegrityError on flush
    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_workout_plan_version_positive(db_session):
    """Test check constraint for positive version."""
    from app.models.user import User
    user = User(
        email="test3@example.com",
        hashed_password="hashedpassword",
        is_active=True,
        is_verified=True,
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    wp = WorkoutPlan(
        user_id=user.id,
        plan_identifier="test-id",
        version=0,  # invalid
        is_active=False,
        name="Test Plan",
    )
    db_session.add(wp)
    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_plan_day_relationships(db_session):
    """Test PlanDay relationships and constraints."""
    from app.models.user import User
    user = User(
        email="test4@example.com",
        hashed_password="hashedpassword",
        is_active=True,
        is_verified=True,
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    wp = WorkoutPlan(
        user_id=user.id,
        plan_identifier="plan-day-test",
        version=1,
        is_active=False,
        name="Test Plan",
    )
    db_session.add(wp)
    await db_session.flush()
    await db_session.refresh(wp)

    day1 = PlanDay(
        workout_plan=wp,
        day_number=1,
        name="Day 1",
        description="First day",
        focus="Upper Body",
        order_idx=0,
    )
    day2 = PlanDay(
        workout_plan=wp,
        day_number=2,
        name="Day 2",
        description="Second day",
        focus="Lower Body",
        order_idx=1,
    )
    db_session.add_all([day1, day2])
    await db_session.flush()
    await db_session.refresh(day1)
    await db_session.refresh(day2)

    assert day1.id is not None
    assert day1.workout_plan is wp
    assert day1.day_number == 1
    assert day1.name == "Day 1"
    assert day1.order_idx == 0
    # Verify workout_plan relationship via query (avoid MissingGreenlet in async)
    result = await db_session.execute(select(WorkoutPlan).where(WorkoutPlan.id == day1.workout_plan.id))
    workout_plan_1 = result.scalar_one_or_none()
    assert workout_plan_1 is not None
    assert workout_plan_1.id == wp.id

    # Test ORM relationship access - workout_plan relationship should be accessible via attribute
    # With lazy="selectin", accessing the attribute will trigger a load if not already loaded
    assert day1.workout_plan is not None
    assert day1.workout_plan.id == wp.id
    assert day1.workout_plan.name == "Test Plan"

    # Test ORM relationship access - plan_exercises relationship should be accessible via attribute
    # With lazy="selectin", accessing the attribute will trigger a load if not already loaded
    assert day1.plan_exercises == []  # Empty list since no exercises added yet

    assert day2.id is not None
    assert day2.workout_plan is wp
    assert day2.day_number == 2
    assert day2.name == "Day 2"
    assert day2.order_idx == 1
    # Verify workout_plan relationship via query (avoid MissingGreenlet in async)
    result = await db_session.execute(select(WorkoutPlan).where(WorkoutPlan.id == day2.workout_plan.id))
    workout_plan_2 = result.scalar_one_or_none()
    assert workout_plan_2 is not None
    assert workout_plan_2.id == wp.id

    # Test ORM relationship access - workout_plan relationship should be accessible via attribute
    # With lazy="selectin", accessing the attribute will trigger a load if not already loaded
    assert day2.workout_plan is not None
    assert day2.workout_plan.id == wp.id
    assert day2.workout_plan.name == "Test Plan"

    # Test ORM relationship access - plan_exercises relationship should be accessible via attribute
    # With lazy="selectin", accessing the attribute will trigger a load if not already loaded
    assert day2.plan_exercises == []  # Empty list since no exercises added yet

    # Test that the workout plan has both days in its plan_days collection
    # With lazy="selectin", accessing the attribute will trigger a load if not already loaded
    assert len(wp.plan_days) == 2
    day_numbers = {day.day_number for day in wp.plan_days}
    assert day_numbers == {1, 2}

    # Test loading WorkoutPlan through explicit select() to verify lazy="selectin" works
    result = await db_session.execute(select(WorkoutPlan).where(WorkoutPlan.id == wp.id))
    wp_from_db = result.scalar_one_or_none()
    assert wp_from_db is not None
    assert wp_from_db.id == wp.id
    # Access the relationship - this should work with lazy="selectin"
    assert len(wp_from_db.plan_days) == 2
    day_numbers_from_db = {day.day_number for day in wp_from_db.plan_days}
    assert day_numbers_from_db == {1, 2}

    # Test unique constraint on day_number within same workout plan
    with pytest.raises(IntegrityError):
        async with db_session.begin_nested():
            day3 = PlanDay(
                workout_plan_id=wp.id,
                day_number=1,  # duplicate day_number
                name="Duplicate",
                order_idx=2,
            )
            db_session.add(day3)
            await db_session.flush()

    # Test unique constraint on order_idx within same workout plan
    with pytest.raises(IntegrityError):
        async with db_session.begin_nested():
            day4 = PlanDay(
                workout_plan_id=wp.id,
                day_number=3,
                name="Another",
                order_idx=0,  # duplicate order_idx
            )
            db_session.add(day4)
            await db_session.flush()


@pytest.mark.asyncio
async def test_plan_exercise_relationships(db_session):
    """Test PlanExercise relationships and constraints."""
    from app.models.user import User
    user = User(
        email="test5@example.com",
        hashed_password="hashedpassword",
        is_active=True,
        is_verified=True,
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    wp = WorkoutPlan(
        user_id=user.id,
        plan_identifier="plan-exercise-test",
        version=1,
        is_active=False,
        name="Test Plan",
    )
    db_session.add(wp)
    await db_session.flush()
    await db_session.refresh(wp)

    day = PlanDay(
        workout_plan_id=wp.id,
        day_number=1,
        name="Day 1",
        order_idx=0,
    )
    db_session.add(day)
    await db_session.flush()
    await db_session.refresh(day)

    ex1 = PlanExercise(
        plan_day=day,
        exercise_name="Push Up",
        target_sets=3,
        target_reps="8-12",
        target_weight_kg=0.0,
        rest_seconds=60,
        order_idx=0,
        notes="Standard push up",
    )
    ex2 = PlanExercise(
        plan_day=day,
        exercise_name="Squat",
        target_sets=4,
        target_reps="10",
        target_weight_kg=50.0,
        rest_seconds=90,
        order_idx=1,
        notes="Back squat",
    )
    db_session.add_all([ex1, ex2])
    await db_session.flush()
    await db_session.refresh(ex1)
    await db_session.refresh(ex2)

    assert ex1.id is not None
    assert ex1.plan_day is day
    assert ex1.exercise_name == "Push Up"
    assert ex1.target_sets == 3
    assert ex1.target_reps == "8-12"
    assert ex1.target_weight_kg == 0.0
    assert ex1.rest_seconds == 60
    assert ex1.order_idx == 0
    assert ex1.notes == "Standard push up"
    # Verify plan_day relationship via query (avoid MissingGreenlet in async)
    result = await db_session.execute(select(PlanDay).where(PlanDay.id == ex1.plan_day.id))
    plan_day_1 = result.scalar_one_or_none()
    assert plan_day_1 is not None
    assert plan_day_1.id == day.id

    # Test ORM relationship access - plan_day relationship should be accessible via attribute
    # With lazy="selectin", accessing the attribute will trigger a load if not already loaded
    assert ex1.plan_day is not None
    assert ex1.plan_day.id == day.id
    assert ex1.plan_day.name == "Day 1"

    assert ex2.id is not None
    assert ex2.plan_day is day
    assert ex2.exercise_name == "Squat"
    assert ex2.target_sets == 4
    assert ex2.target_reps == "10"
    assert ex2.target_weight_kg == 50.0
    assert ex2.rest_seconds == 90
    assert ex2.order_idx == 1
    assert ex2.notes == "Back squat"
    # Verify plan_day relationship via query (avoid MissingGreenlet in async)
    result = await db_session.execute(select(PlanDay).where(PlanDay.id == ex2.plan_day.id))
    plan_day_2 = result.scalar_one_or_none()
    assert plan_day_2 is not None
    assert plan_day_2.id == day.id

    # Test ORM relationship access - plan_day relationship should be accessible via attribute
    # With lazy="selectin", accessing the attribute will trigger a load if not already loaded
    assert ex2.plan_day is not None
    assert ex2.plan_day.id == day.id
    assert ex2.plan_day.name == "Day 1"

    # Test that the plan day has both exercises in its plan_exercises collection
    # With lazy="selectin", accessing the attribute will trigger a load if not already loaded
    assert len(day.plan_exercises) == 2
    exercise_names = {ex.exercise_name for ex in day.plan_exercises}
    assert exercise_names == {"Push Up", "Squat"}

    # Test loading PlanDay through explicit select() to verify lazy="selectin" works
    result = await db_session.execute(select(PlanDay).where(PlanDay.id == day.id))
    day_from_db = result.scalar_one_or_none()
    assert day_from_db is not None
    assert day_from_db.id == day.id
    # Access the relationship - this should work with lazy="selectin"
    assert len(day_from_db.plan_exercises) == 2
    exercise_names_from_db = {ex.exercise_name for ex in day_from_db.plan_exercises}
    assert exercise_names_from_db == {"Push Up", "Squat"}

    # Test unique constraint on order_idx within same plan day
    with pytest.raises(IntegrityError):
        async with db_session.begin_nested():
            ex3 = PlanExercise(
                plan_day_id=day.id,
                exercise_name="Another",
                target_sets=2,
                target_reps="5",
                order_idx=0,  # duplicate order_idx
            )
            db_session.add(ex3)
            await db_session.flush()

    # Test check constraint for positive target_sets
    with pytest.raises(IntegrityError):
        async with db_session.begin_nested():
            ex4 = PlanExercise(
                plan_day_id=day.id,
                exercise_name="Invalid",
                target_sets=0,  # invalid
                target_reps="5",
                order_idx=2,
            )
            db_session.add(ex4)
            await db_session.flush()

    # Test check constraint for non-negative rest_seconds
    with pytest.raises(IntegrityError):
        async with db_session.begin_nested():
            ex5 = PlanExercise(
                plan_day_id=day.id,
                exercise_name="Invalid Rest",
                target_sets=2,
                target_reps="5",
                rest_seconds=-5,  # invalid
                order_idx=3,
            )
            db_session.add(ex5)
            await db_session.flush()


@pytest.mark.asyncio
async def test_cascade_delete(db_session):
    """Test that deleting a workout plan cascades to days and exercises."""
    from app.models.user import User
    user = User(
        email="test6@example.com",
        hashed_password="hashedpassword",
        is_active=True,
        is_verified=True,
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    wp = WorkoutPlan(
        user_id=user.id,
        plan_identifier="cascade-test",
        version=1,
        is_active=False,
        name="Test Plan",
    )
    db_session.add(wp)
    await db_session.flush()
    await db_session.refresh(wp)

    day = PlanDay(
        workout_plan_id=wp.id,
        day_number=1,
        name="Day 1",
        order_idx=0,
    )
    db_session.add(day)
    await db_session.flush()
    await db_session.refresh(day)

    ex = PlanExercise(
        plan_day_id=day.id,
        exercise_name="Test Exercise",
        target_sets=3,
        target_reps="10",
        order_idx=0,
    )
    db_session.add(ex)
    await db_session.flush()
    await db_session.refresh(ex)

    # Verify they exist
    assert wp.id is not None
    assert day.id is not None
    assert ex.id is not None

    # Delete workout plan
    await db_session.delete(wp)
    await db_session.flush()

    # Now query to ensure day and exercise are deleted
    from sqlalchemy import select
    result = await db_session.execute(select(PlanDay).where(PlanDay.id == day.id))
    day_deleted = result.scalar_one_or_none()
    assert day_deleted is None

    result = await db_session.execute(select(PlanExercise).where(PlanExercise.id == ex.id))
    ex_deleted = result.scalar_one_or_none()
    assert ex_deleted is None


@pytest.mark.asyncio
async def test_user_deletion_cascade(db_session):
    """Test that deleting a user cascades to workout plans."""
    from app.models.user import User
    user = User(
        email="test7@example.com",
        hashed_password="hashedpassword",
        is_active=True,
        is_verified=True,
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    wp = WorkoutPlan(
        user=user,
        plan_identifier="user-cascade-test",
        version=1,
        is_active=False,
        name="Test Plan",
    )
    db_session.add(wp)
    await db_session.flush()
    await db_session.refresh(wp)

    # Delete user - should cascade to workout plans due to cascade="all, delete-orphan"
    await db_session.delete(user)
    await db_session.flush()

    # Verify user is deleted
    result = await db_session.execute(select(User).where(User.id == user.id))
    user_after = result.scalar_one_or_none()
    assert user_after is None

    # Verify workout plan is deleted due to cascade
    result = await db_session.execute(select(WorkoutPlan).where(WorkoutPlan.id == wp.id))
    wp_after = result.scalar_one_or_none()
    assert wp_after is None


@pytest.mark.asyncio
async def test_partial_unique_index_active_versions(db_session):
    """Test PostgreSQL partial unique index for active plan versions."""
    from app.models.user import User
    user = User(
        email="test8@example.com",
        hashed_password="hashedpassword",
        is_active=True,
        is_verified=True,
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    # Create first logical plan version 1, active
    wp1_v1 = WorkoutPlan(
        user_id=user.id,
        plan_identifier="plan-x",
        version=1,
        is_active=True,
        name="Plan X v1",
    )
    db_session.add(wp1_v1)
    await db_session.flush()
    await db_session.refresh(wp1_v1)

    # Create second logical plan version 1, active (different plan_identifier)
    wp2_v1 = WorkoutPlan(
        user_id=user.id,
        plan_identifier="plan-y",
        version=1,
        is_active=True,
        name="Plan Y v1",
    )
    db_session.add(wp2_v1)
    await db_session.flush()
    await db_session.refresh(wp2_v1)

    # Create version 2 of plan-x, inactive
    wp1_v2 = WorkoutPlan(
        user_id=user.id,
        plan_identifier="plan-x",
        version=2,
        is_active=False,
        name="Plan X v2",
    )
    db_session.add(wp1_v2)
    await db_session.flush()
    await db_session.refresh(wp1_v2)

    # Test that we cannot have two active versions for same user and same plan_identifier
    # Try to create another active version of plan-x with version 3 (different version, same plan_identifier)
    # This should fail due to the partial unique index, not the regular unique constraint
    with pytest.raises(IntegrityError):
        async with db_session.begin_nested():
            wp1_v3_active = WorkoutPlan(
                user_id=user.id,
                plan_identifier="plan-x",
                version=3,  # different version but same plan_identifier
                is_active=True,  # trying to make another active version while v1 is active
                name="Plan X v3 active",
            )
            db_session.add(wp1_v3_active)
            await db_session.flush()

    # Now deactivate the existing active version (v1) and activate v2
    wp1_v1.is_active = False
    wp1_v2.is_active = True
    await db_session.flush()
    # Should succeed now - access properties directly after flush (no need to refresh)
    assert wp1_v1.is_active is False
    assert wp1_v2.is_active is True

    # Create a third logical plan (plan-z) with version 1 active - should be fine because different plan_identifier
    wp3_v1 = WorkoutPlan(
        user_id=user.id,
        plan_identifier="plan-z",
        version=1,
        is_active=True,
        name="Plan Z v1",
    )
    db_session.add(wp3_v1)
    await db_session.flush()
    # Access property directly after flush (no need to refresh)
    assert wp3_v1.is_active is True

    # Now we have:
    # - plan-x: v1 inactive, v2 active
    # - plan-y: v1 active
    # - plan-z: v1 active
    # All should be allowed because the partial index only cares about (user_id, plan_identifier) where is_active=true.
    # For user_id, plan_identifier combinations:
    #   (user, plan-x): only v2 active -> ok
    #   (user, plan-y): only v1 active -> ok
    #   (user, plan-z): only v1 active -> ok

    # Test that we cannot have two active versions for same user and same plan_identifier
    # Try to activate v1 of plan-x again while v2 is active
    with pytest.raises(IntegrityError):
        async with db_session.begin_nested():
            wp1_v1.is_active = True
            await db_session.flush()
