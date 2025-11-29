"""Behavioral analysis models with type safety."""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class BehaviorFactor(str, Enum):
    """Behavioral factor categories."""

    ADHD = "adhd"
    ASD = "asd"
    AGE_TYPICAL = "age_typical"
    COMBINED = "combined"


class TimeOfDay(str, Enum):
    """Time periods for behavior tracking."""

    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    BEDTIME = "bedtime"


class ActivityType(str, Enum):
    """Types of activities."""

    SCHOOL = "school"
    HOMEWORK = "homework"
    PLAY = "play"
    TRANSITIONS = "transitions"
    MEALS = "meals"
    BEDTIME_ROUTINE = "bedtime_routine"
    HYGIENE = "hygiene"


class BehaviorInput(BaseModel):
    """Input for behavior analysis.

    Note: strict=False allows LLM tool calls to pass string values
    for enums (e.g., "evening" -> TimeOfDay.EVENING).
    """

    description: str = Field(..., min_length=10, max_length=1000)
    time_of_day: TimeOfDay
    activity_type: ActivityType
    context: str = Field(..., min_length=5, max_length=500)

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=False,
        strict=False,  # Allow string coercion for LLM tool inputs
        extra="forbid",
    )


class BehaviorAnalysis(BaseModel):
    """Result of behavior analysis."""

    adhd_factors: list[str] = Field(default_factory=list)
    asd_factors: list[str] = Field(default_factory=list)
    age_typical_factors: list[str] = Field(default_factory=list)
    primary_driver: BehaviorFactor

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=False,
        strict=True,
        extra="forbid",
        frozen=True,
    )
