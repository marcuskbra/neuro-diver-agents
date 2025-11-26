"""Global test fixtures and configuration."""

import pytest


@pytest.fixture
def sample_behavior_description() -> str:
    """Sample behavior description for testing."""
    return (
        "My 8-year-old refuses to start homework after school. "
        "He gets frustrated and sometimes has meltdowns when I ask him to begin."
    )


@pytest.fixture
def sample_activity_materials() -> list[str]:
    """Sample materials for activity planning tests."""
    return ["visual timer", "fidget toys", "favorite books", "drawing supplies"]


@pytest.fixture
def sample_session_history() -> list[dict[str, str | bool]]:
    """Sample session history for pattern analysis tests."""
    return [
        {
            "strategy_used": "visual timer for 10 minutes",
            "worked": True,
            "notes": "Went to bed without resistance",
        },
        {
            "strategy_used": "verbal reminders only",
            "worked": False,
            "notes": "Got upset, took 45 minutes",
        },
        {
            "strategy_used": "visual timer + sensory break",
            "worked": True,
            "notes": "Very calm and cooperative",
        },
    ]
