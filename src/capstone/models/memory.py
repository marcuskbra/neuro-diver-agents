"""Memory and pattern tracking models."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SessionOutcome(BaseModel):
    """Outcome of a strategy application.

    Note: strict=False allows LLM tool calls to pass string values
    (e.g., "true" -> True for booleans, ISO strings -> datetime).
    """

    strategy_used: str = Field(..., min_length=5)
    worked: bool
    notes: str = Field(..., min_length=5, max_length=500)
    timestamp: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(
        validate_assignment=True,
        strict=False,  # Allow string coercion for LLM tool inputs
        extra="forbid",
    )


class BehaviorPattern(BaseModel):
    """Identified behavioral pattern."""

    behavior_type: str = Field(..., min_length=3)
    common_triggers: list[str] = Field(default_factory=list)
    successful_strategies: list[str] = Field(default_factory=list)
    unsuccessful_approaches: list[str] = Field(default_factory=list)
    frequency_count: int = Field(..., ge=0)
    sessions_analyzed: int = Field(..., ge=1)

    model_config = ConfigDict(
        validate_assignment=True,
        strict=True,
        extra="forbid",
        frozen=True,
    )

    @model_validator(mode="after")
    def validate_frequency(self) -> "BehaviorPattern":
        """Validate frequency doesn't exceed sessions analyzed."""
        if self.frequency_count > self.sessions_analyzed:
            raise ValueError("Frequency cannot exceed sessions analyzed")
        return self
