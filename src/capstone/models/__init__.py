"""Pydantic models for the Neurodivergent Parenting Support Agent."""

from .activity import ActivityGoal, ActivityPlan, ActivityRequest
from .behavior import (
    ActivityType,
    BehaviorAnalysis,
    BehaviorFactor,
    BehaviorInput,
    TimeOfDay,
)
from .memory import BehaviorPattern, SessionOutcome
from .results import ToolError, ToolResult, ToolSuccess, is_error, is_success
from .strategy import BehaviorResponse, Strategy

__all__ = [
    # Activity models
    "ActivityGoal",
    "ActivityPlan",
    "ActivityRequest",
    # Behavior models
    "ActivityType",
    "BehaviorAnalysis",
    "BehaviorFactor",
    "BehaviorInput",
    "TimeOfDay",
    # Memory models
    "BehaviorPattern",
    "SessionOutcome",
    # Result models
    "ToolError",
    "ToolResult",
    "ToolSuccess",
    "is_error",
    "is_success",
    # Strategy models
    "BehaviorResponse",
    "Strategy",
]
