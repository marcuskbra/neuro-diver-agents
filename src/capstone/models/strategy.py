"""Strategy response models."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .behavior import BehaviorAnalysis


class Strategy(BaseModel):
    """Individual strategy recommendation."""

    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    rationale: str = Field(..., min_length=10, max_length=300)
    success_indicators: list[str] = Field(..., min_length=1)

    model_config = ConfigDict(
        validate_assignment=True,
        strict=True,
        extra="forbid",
        frozen=True,
    )


class BehaviorResponse(BaseModel):
    """Complete behavioral analysis response."""

    acknowledgment: str = Field(..., min_length=10, max_length=200)
    analysis: BehaviorAnalysis
    strategies: list[Strategy] = Field(..., min_length=1, max_length=5)
    proactive_suggestion: str | None = Field(None, max_length=300)
    disclaimer: Literal["I'm a parenting support tool, not medical advice."] = (
        "I'm a parenting support tool, not medical advice."
    )

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=False,
        strict=True,
        extra="forbid",
        frozen=True,
    )
