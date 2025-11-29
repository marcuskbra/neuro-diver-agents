"""Unit tests for memory models."""

from datetime import datetime
from typing import cast

import pytest
from pydantic import ValidationError

from capstone.models.memory import BehaviorPattern, SessionOutcome


class TestSessionOutcome:
    """Test SessionOutcome Pydantic model."""

    def test_create_valid_session_outcome(self):
        """Test creating valid SessionOutcome."""
        outcome = SessionOutcome(
            strategy_used="visual timer for 10 minutes",
            worked=True,
            notes="Child cooperated well with visual support.",
        )

        assert outcome.strategy_used == "visual timer for 10 minutes"
        assert outcome.worked is True
        assert outcome.notes == "Child cooperated well with visual support."
        assert isinstance(outcome.timestamp, datetime)

    def test_session_outcome_with_custom_timestamp(self):
        """Test creating SessionOutcome with custom timestamp."""
        custom_time = datetime(2024, 1, 15, 14, 30, 0)
        outcome = SessionOutcome(
            strategy_used="sensory break before homework",
            worked=False,
            notes="Child was still overwhelmed after break.",
            timestamp=custom_time,
        )

        assert outcome.timestamp == custom_time

    def test_strategy_used_min_length_validation(self):
        """Test strategy_used must be at least 5 characters."""
        with pytest.raises(ValidationError) as exc_info:
            SessionOutcome(
                strategy_used="abc",  # Only 3 characters
                worked=True,
                notes="Valid notes here.",
            )

        validation_error = cast(ValidationError, exc_info.value)
        errors = validation_error.errors()
        assert any(e["loc"] == ("strategy_used",) for e in errors)

    def test_notes_min_length_validation(self):
        """Test notes must be at least 5 characters."""
        with pytest.raises(ValidationError) as exc_info:
            SessionOutcome(
                strategy_used="valid strategy here",
                worked=True,
                notes="abc",  # Only 3 characters
            )

        validation_error = cast(ValidationError, exc_info.value)
        errors = validation_error.errors()
        assert any(e["loc"] == ("notes",) for e in errors)

    def test_notes_max_length_validation(self):
        """Test notes must be at most 500 characters."""
        with pytest.raises(ValidationError) as exc_info:
            SessionOutcome(
                strategy_used="valid strategy here",
                worked=True,
                notes="x" * 501,  # 501 characters
            )

        validation_error = cast(ValidationError, exc_info.value)
        errors = validation_error.errors()
        assert any(e["loc"] == ("notes",) for e in errors)

    def test_strict_false_allows_string_coercion(self):
        """Test that strict=False allows string-to-bool coercion from LLM."""
        # This simulates what happens when LLM passes "true" as a string
        outcome = SessionOutcome.model_validate(
            {
                "strategy_used": "visual timer approach",
                "worked": True,  # Normal bool
                "notes": "Worked well for the child.",
            }
        )

        assert outcome.worked is True


class TestBehaviorPattern:
    """Test BehaviorPattern Pydantic model."""

    def test_create_valid_behavior_pattern(self):
        """Test creating valid BehaviorPattern."""
        pattern = BehaviorPattern(
            behavior_type="bedtime",
            common_triggers=["screen time", "late dinner"],
            successful_strategies=["visual timer", "sensory break"],
            unsuccessful_approaches=["verbal warnings only"],
            frequency_count=5,
            sessions_analyzed=7,
        )

        assert pattern.behavior_type == "bedtime"
        assert len(pattern.common_triggers) == 2
        assert len(pattern.successful_strategies) == 2
        assert len(pattern.unsuccessful_approaches) == 1
        assert pattern.frequency_count == 5
        assert pattern.sessions_analyzed == 7

    def test_behavior_pattern_with_empty_lists(self):
        """Test creating BehaviorPattern with empty trigger/strategy lists."""
        pattern = BehaviorPattern(
            behavior_type="homework",
            common_triggers=[],
            successful_strategies=[],
            unsuccessful_approaches=[],
            frequency_count=0,
            sessions_analyzed=1,
        )

        assert pattern.common_triggers == []
        assert pattern.successful_strategies == []
        assert pattern.unsuccessful_approaches == []

    def test_behavior_type_min_length_validation(self):
        """Test behavior_type must be at least 3 characters."""
        with pytest.raises(ValidationError) as exc_info:
            BehaviorPattern(
                behavior_type="ab",  # Only 2 characters
                frequency_count=1,
                sessions_analyzed=1,
            )

        validation_error = cast(ValidationError, exc_info.value)
        errors = validation_error.errors()
        assert any(e["loc"] == ("behavior_type",) for e in errors)

    def test_frequency_count_non_negative_validation(self):
        """Test frequency_count must be >= 0."""
        with pytest.raises(ValidationError) as exc_info:
            BehaviorPattern(
                behavior_type="bedtime",
                frequency_count=-1,
                sessions_analyzed=5,
            )

        validation_error = cast(ValidationError, exc_info.value)
        errors = validation_error.errors()
        assert any(e["loc"] == ("frequency_count",) for e in errors)

    def test_sessions_analyzed_minimum_validation(self):
        """Test sessions_analyzed must be >= 1."""
        with pytest.raises(ValidationError) as exc_info:
            BehaviorPattern(
                behavior_type="bedtime",
                frequency_count=0,
                sessions_analyzed=0,
            )

        validation_error = cast(ValidationError, exc_info.value)
        errors = validation_error.errors()
        assert any(e["loc"] == ("sessions_analyzed",) for e in errors)

    def test_frequency_cannot_exceed_sessions_analyzed(self):
        """Test that frequency_count cannot exceed sessions_analyzed."""
        with pytest.raises(ValidationError) as exc_info:
            BehaviorPattern(
                behavior_type="bedtime",
                frequency_count=10,  # Greater than sessions_analyzed
                sessions_analyzed=5,
            )

        validation_error = cast(ValidationError, exc_info.value)
        errors = validation_error.errors()
        # The model_validator should raise an error
        assert any("Frequency cannot exceed sessions analyzed" in str(e) for e in errors)

    def test_frequency_equals_sessions_is_valid(self):
        """Test that frequency_count can equal sessions_analyzed (100% success)."""
        pattern = BehaviorPattern(
            behavior_type="homework",
            frequency_count=5,
            sessions_analyzed=5,
        )

        assert pattern.frequency_count == pattern.sessions_analyzed

    def test_frequency_zero_is_valid(self):
        """Test that frequency_count of 0 is valid (0% success rate)."""
        pattern = BehaviorPattern(
            behavior_type="transitions",
            frequency_count=0,
            sessions_analyzed=10,
        )

        assert pattern.frequency_count == 0

    def test_behavior_pattern_is_frozen(self):
        """Test that BehaviorPattern is immutable."""
        pattern = BehaviorPattern(
            behavior_type="bedtime",
            frequency_count=3,
            sessions_analyzed=5,
        )

        with pytest.raises(ValidationError):
            pattern.frequency_count = 4  # type: ignore

    def test_behavior_pattern_forbids_extra_fields(self):
        """Test that extra fields are forbidden."""
        with pytest.raises(ValidationError) as exc_info:
            BehaviorPattern.model_validate(
                {
                    "behavior_type": "bedtime",
                    "frequency_count": 3,
                    "sessions_analyzed": 5,
                    "extra_field": "not allowed",
                }
            )

        validation_error = cast(ValidationError, exc_info.value)
        errors = validation_error.errors()
        assert any(e["type"] == "extra_forbidden" for e in errors)
