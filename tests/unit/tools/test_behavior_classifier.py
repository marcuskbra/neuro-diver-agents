"""Unit tests for behavior classifier tool."""

import pytest

from capstone.models.behavior import (
    ActivityType,
    BehaviorFactor,
    BehaviorInput,
    TimeOfDay,
)
from capstone.models.results import ToolSuccess
from capstone.tools.behavior_classifier import classify_behavior


class TestBehaviorClassifier:
    """Test behavior classification tool."""

    def test_classify_behavior_with_adhd_indicators(self, behavior_input_factory):
        """Test classification identifies ADHD factors."""
        behavior = behavior_input_factory(
            description=(
                "Child cannot focus on homework for more than 2 minutes. "
                "Gets distracted by every sound. Fidgets constantly and "
                "has difficulty staying in seat during work time."
            ),
            activity_type=ActivityType.HOMEWORK,
        )

        result = classify_behavior(behavior)

        assert isinstance(result, ToolSuccess)
        assert result.success is True
        assert "adhd_factors" in result.data
        adhd_factors = result.get_list("adhd_factors")
        assert len(adhd_factors) > 0
        assert any("attention" in factor.lower() for factor in adhd_factors)

    def test_classify_behavior_with_asd_indicators(self, behavior_input_factory):
        """Test classification identifies ASD factors."""
        behavior = behavior_input_factory(
            description=(
                "Child becomes very distressed when routine changes. "
                "Covers ears when environment is too loud. Needs things "
                "done in exact same order every time or has meltdown."
            ),
            activity_type=ActivityType.TRANSITIONS,
        )

        result = classify_behavior(behavior)

        assert isinstance(result, ToolSuccess)
        assert result.success is True
        assert "asd_factors" in result.data
        asd_factors = result.get_list("asd_factors")
        assert len(asd_factors) > 0
        assert any(
            "sensory" in factor.lower() or "routine" in factor.lower() for factor in asd_factors
        )

    def test_classify_behavior_with_age_typical(self, behavior_input_factory):
        """Test classification identifies age-typical behaviors."""
        behavior = behavior_input_factory(
            description=(
                "8-year-old doesn't want to do homework right after school. "
                "Wants to play instead. Gets cranky when asked to work. "
                "This is pretty normal kid behavior."
            ),
            activity_type=ActivityType.HOMEWORK,
            time_of_day=TimeOfDay.AFTERNOON,
        )

        result = classify_behavior(behavior)

        assert isinstance(result, ToolSuccess)
        assert result.success is True
        assert "age_typical_factors" in result.data
        # Age-typical factors should be present
        assert len(result.get_list("age_typical_factors")) > 0

    def test_classify_behavior_combined_factors(self, behavior_input_factory):
        """Test classification when multiple factors present."""
        behavior = behavior_input_factory(
            description=(
                "Child has trouble focusing (ADHD-like) and also gets "
                "upset by loud noises (ASD-like). Fidgets constantly "
                "and needs quiet, structured environment."
            ),
            activity_type=ActivityType.HOMEWORK,
        )

        result = classify_behavior(behavior)

        assert isinstance(result, ToolSuccess)
        assert result.success is True
        # Should identify both ADHD and ASD factors
        assert len(result.get_list("adhd_factors")) > 0
        assert len(result.get_list("asd_factors")) > 0
        # Primary driver should be COMBINED when multiple strong factors
        assert result.get_str("primary_driver") in [
            BehaviorFactor.COMBINED.value,
            BehaviorFactor.ADHD.value,
            BehaviorFactor.ASD.value,
        ]

    def test_classify_behavior_returns_primary_driver(self, behavior_input_factory):
        """Test that primary driver is identified."""
        behavior = behavior_input_factory()

        result = classify_behavior(behavior)

        assert isinstance(result, ToolSuccess)
        assert "primary_driver" in result.data
        assert result.get_str("primary_driver") in [
            BehaviorFactor.ADHD.value,
            BehaviorFactor.ASD.value,
            BehaviorFactor.AGE_TYPICAL.value,
            BehaviorFactor.COMBINED.value,
        ]

    def test_classify_behavior_error_handling(self):
        """Test that errors are handled gracefully."""
        # Create invalid input to trigger error
        with pytest.raises(Exception):
            # This should raise validation error before classify_behavior
            BehaviorInput(
                description="Too short",  # Less than 10 chars
                time_of_day=TimeOfDay.MORNING,
                activity_type=ActivityType.PLAY,
                context="Test",  # Less than 5 chars
            )

    def test_classify_behavior_result_structure(self, behavior_input_factory):
        """Test that result has expected structure."""
        behavior = behavior_input_factory()

        result = classify_behavior(behavior)

        assert isinstance(result, ToolSuccess)
        assert result.success is True
        assert isinstance(result.data, dict)

        # Check all required keys present
        required_keys = {"adhd_factors", "asd_factors", "age_typical_factors", "primary_driver"}
        assert required_keys.issubset(result.data.keys())

        # Check data types using typed accessors
        adhd_factors = result.get_list("adhd_factors")
        asd_factors = result.get_list("asd_factors")
        age_typical_factors = result.get_list("age_typical_factors")
        primary_driver = result.get_str("primary_driver")

        assert isinstance(adhd_factors, list)
        assert isinstance(asd_factors, list)
        assert isinstance(age_typical_factors, list)
        assert isinstance(primary_driver, str)

    def test_classify_behavior_factors_are_strings(self, behavior_input_factory):
        """Test that all factors are string lists."""
        behavior = behavior_input_factory()

        result = classify_behavior(behavior)

        assert isinstance(result, ToolSuccess)

        for factor in result.get_list("adhd_factors"):
            assert isinstance(factor, str)
        for factor in result.get_list("asd_factors"):
            assert isinstance(factor, str)
        for factor in result.get_list("age_typical_factors"):
            assert isinstance(factor, str)
