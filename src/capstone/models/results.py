"""Discriminated union for tool results."""

from typing import Literal, TypeGuard

from pydantic import BaseModel, ConfigDict, Field


class ToolSuccess(BaseModel):
    """Successful tool execution."""

    success: Literal[True] = True
    data: dict[str, str | int | float | bool | list[str]]

    model_config = ConfigDict(
        validate_assignment=True,
        strict=True,
        extra="forbid",
        frozen=True,
    )

    def get_str(self, key: str, default: str = "") -> str:
        """Get a string value from data with type safety."""
        value = self.data.get(key, default)
        if isinstance(value, str):
            return value
        return default

    def get_int(self, key: str, default: int = 0) -> int:
        """Get an integer value from data with type safety."""
        value = self.data.get(key, default)
        if isinstance(value, int) and not isinstance(value, bool):
            return value
        return default

    def get_float(self, key: str, default: float = 0.0) -> float:
        """Get a float value from data with type safety."""
        value = self.data.get(key, default)
        if isinstance(value, float):
            return value
        if isinstance(value, int) and not isinstance(value, bool):
            return float(value)
        return default

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get a boolean value from data with type safety."""
        value = self.data.get(key, default)
        if isinstance(value, bool):
            return value
        return default

    def get_list(self, key: str, default: list[str] | None = None) -> list[str]:
        """Get a list value from data with type safety."""
        if default is None:
            default = []
        value = self.data.get(key, default)
        if isinstance(value, list):
            return value
        return default


class ToolError(BaseModel):
    """Tool execution error."""

    success: Literal[False] = False
    error_code: str = Field(..., min_length=1)
    error_message: str = Field(..., min_length=1)

    model_config = ConfigDict(
        validate_assignment=True,
        strict=True,
        extra="forbid",
        frozen=True,
    )


ToolResult = ToolSuccess | ToolError


def is_success(result: ToolResult) -> TypeGuard[ToolSuccess]:
    """Type guard for successful results."""
    return result.success is True


def is_error(result: ToolResult) -> TypeGuard[ToolError]:
    """Type guard for error results."""
    return result.success is False
