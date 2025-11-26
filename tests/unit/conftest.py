"""Unit test fixtures and factories."""

from collections.abc import Callable

import pytest

from capstone.models import (
    ActivityGoal,
    ActivityRequest,
    ActivityType,
    BehaviorInput,
    SessionOutcome,
    TimeOfDay,
)


@pytest.fixture
def behavior_input_factory() -> Callable[..., BehaviorInput]:
    """Factory for creating BehaviorInput test instances."""

    def _create(
        description: str = "Child refuses to do homework and gets frustrated when asked.",
        time_of_day: TimeOfDay = TimeOfDay.AFTERNOON,
        activity_type: ActivityType = ActivityType.HOMEWORK,
        context: str = "After school around 5-6pm, most days of the week.",
        **kwargs,
    ) -> BehaviorInput:
        return BehaviorInput(
            description=description,
            time_of_day=time_of_day,
            activity_type=activity_type,
            context=context,
            **kwargs,
        )

    return _create


@pytest.fixture
def activity_request_factory() -> Callable[..., ActivityRequest]:
    """Factory for creating ActivityRequest test instances."""

    def _create(
        goal: ActivityGoal = ActivityGoal.ENGAGEMENT,
        duration_minutes: int = 30,
        available_materials: list[str] | None = None,
        **kwargs,
    ) -> ActivityRequest:
        if available_materials is None:
            available_materials = ["visual timer", "fidget toys", "books"]

        return ActivityRequest(
            goal=goal,
            duration_minutes=duration_minutes,
            available_materials=available_materials,
            **kwargs,
        )

    return _create


@pytest.fixture
def session_outcome_factory() -> Callable[..., SessionOutcome]:
    """Factory for creating SessionOutcome test instances."""

    def _create(
        strategy_used: str = "visual timer for 10 minutes",
        worked: bool = True,
        notes: str = "Child cooperated well with visual support.",
        **kwargs,
    ) -> SessionOutcome:
        return SessionOutcome(
            strategy_used=strategy_used,
            worked=worked,
            notes=notes,
            **kwargs,
        )

    return _create
