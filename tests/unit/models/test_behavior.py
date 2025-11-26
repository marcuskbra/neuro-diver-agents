"""Unit tests for behavior models."""

from typing import Any, cast

import pytest
from pydantic import ValidationError

from capstone.models.behavior import (
    ActivityType,
    BehaviorInput,
    TimeOfDay,
)


class TestBehaviorInput:
    """Test BehaviorInput Pydantic model."""

    def test_valid_behavior_input_creation(self):
        """Test creating valid BehaviorInput."""
        behavior = BehaviorInput(
            description="Child refuses homework and gets frustrated.",
            time_of_day=TimeOfDay.AFTERNOON,
            activity_type=ActivityType.HOMEWORK,
            context="After school around 5-6pm, most days.",
        )

        assert behavior.description == "Child refuses homework and gets frustrated."
        assert behavior.time_of_day == TimeOfDay.AFTERNOON
        assert behavior.activity_type == ActivityType.HOMEWORK
        assert behavior.context == "After school around 5-6pm, most days."

    def test_description_min_length_validation(self):
        """Test description must be at least 10 characters."""
        with pytest.raises(ValidationError) as exc_info:
            BehaviorInput(
                description="Short",  # Only 5 characters
                time_of_day=TimeOfDay.MORNING,
                activity_type=ActivityType.PLAY,
                context="Test context for validation",
            )

        validation_error = cast(ValidationError, exc_info.value)
        errors = validation_error.errors()
        assert any(
            error["loc"] == ("description",) and "at least 10 characters" in error["msg"]
            for error in errors
        )

    def test_description_max_length_validation(self):
        """Test description must be at most 1000 characters."""
        with pytest.raises(ValidationError) as exc_info:
            BehaviorInput(
                description="x" * 1001,  # 1001 characters
                time_of_day=TimeOfDay.EVENING,
                activity_type=ActivityType.TRANSITIONS,
                context="Test context for validation",
            )

        validation_error = cast(ValidationError, exc_info.value)
        errors = validation_error.errors()
        assert any(
            error["loc"] == ("description",) and "at most 1000 characters" in error["msg"]
            for error in errors
        )

    def test_context_min_length_validation(self):
        """Test context must be at least 5 characters."""
        with pytest.raises(ValidationError) as exc_info:
            BehaviorInput(
                description="Child refuses to transition to bedtime routine.",
                time_of_day=TimeOfDay.EVENING,
                activity_type=ActivityType.BEDTIME_ROUTINE,
                context="Bad",  # Only 3 characters
            )

        validation_error = cast(ValidationError, exc_info.value)
        errors = validation_error.errors()
        assert any(
            error["loc"] == ("context",) and "at least 5 characters" in error["msg"]
            for error in errors
        )

    def test_strict_mode_no_extra_fields(self):
        """Test that extra fields are forbidden (ConfigDict extra='forbid')."""
        with pytest.raises(ValidationError) as exc_info:
            # Use **kwargs to pass extra field (avoids type checker error)
            kwargs: dict[str, Any] = {
                "description": "Valid description for testing",
                "time_of_day": TimeOfDay.MORNING,
                "activity_type": ActivityType.MEALS,
                "context": "Valid context",
                "extra_field": "should not be allowed",
            }
            BehaviorInput(**kwargs)

        validation_error = cast(ValidationError, exc_info.value)
        errors = validation_error.errors()
        assert any(error["type"] == "extra_forbidden" for error in errors)

    def test_enum_validation(self):
        """Test that invalid enum values are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            # Use **kwargs to pass invalid enum value (avoids type checker error)
            kwargs: dict[str, Any] = {
                "description": "Valid description for testing",
                "time_of_day": "invalid_time",
                "activity_type": ActivityType.HOMEWORK,
                "context": "Valid context",
            }
            BehaviorInput(**kwargs)

        validation_error = cast(ValidationError, exc_info.value)
        errors = validation_error.errors()
        assert any(error["loc"] == ("time_of_day",) for error in errors)

    def test_factory_pattern(self, behavior_input_factory):
        """Test using factory fixture for creating test instances."""
        behavior = behavior_input_factory()

        assert isinstance(behavior, BehaviorInput)
        assert len(behavior.description) >= 10
        assert isinstance(behavior.time_of_day, TimeOfDay)
        assert isinstance(behavior.activity_type, ActivityType)

    def test_factory_with_overrides(self, behavior_input_factory):
        """Test factory allows overriding defaults."""
        behavior = behavior_input_factory(
            description="Custom description for this test case.",
            time_of_day=TimeOfDay.MORNING,
        )

        assert behavior.description == "Custom description for this test case."
        assert behavior.time_of_day == TimeOfDay.MORNING
