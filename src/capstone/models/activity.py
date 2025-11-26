"""Activity planning models."""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class ActivityGoal(str, Enum):
    """Activity goal categories."""

    ENGAGEMENT = "engagement"
    EXECUTIVE_FUNCTION = "executive_function"
    TRANSITION_SUPPORT = "transition_support"
    HOMEWORK_SUPPORT = "homework_support"


class ActivityPlan(BaseModel):
    """Complete activity plan with all preparation details."""

    name: str = Field(..., min_length=5, max_length=100)
    goal: ActivityGoal
    materials: list[str] = Field(..., min_length=1)
    environmental_setup: str = Field(..., min_length=10)
    duration_minutes: int = Field(..., ge=5, le=120)
    structure: list[str] = Field(..., min_length=1)
    success_criteria: list[str] = Field(..., min_length=1)
    adaptations: list[str] = Field(default_factory=list)
    from_memory: str | None = Field(None, description="Past successful patterns")

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=False,
        strict=True,
        extra="forbid",
    )


class ActivityRequest(BaseModel):
    """Request for activity planning."""

    goal: ActivityGoal
    duration_minutes: int = Field(..., ge=5, le=120)
    available_materials: list[str] = Field(default_factory=list)
    specific_needs: str | None = Field(None, max_length=500)

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=False,
        strict=True,
        extra="forbid",
    )
