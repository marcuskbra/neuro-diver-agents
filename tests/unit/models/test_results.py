"""Unit tests for results models and type guards."""

import pytest
from pydantic import ValidationError

from capstone.models.results import (
    ToolError,
    ToolResult,
    ToolSuccess,
    is_error,
    is_success,
)


class TestToolSuccess:
    """Test ToolSuccess Pydantic model."""

    def test_create_success_with_string_data(self):
        """Test creating ToolSuccess with string values."""
        result = ToolSuccess(data={"message": "Success", "code": "OK"})

        assert result.success is True
        assert result.data["message"] == "Success"
        assert result.data["code"] == "OK"

    def test_create_success_with_numeric_data(self):
        """Test creating ToolSuccess with numeric values."""
        result = ToolSuccess(data={"count": 42, "rate": 3.14, "active": True})

        assert result.data["count"] == 42
        assert result.data["rate"] == 3.14
        assert result.data["active"] is True

    def test_create_success_with_list_data(self):
        """Test creating ToolSuccess with list values."""
        result = ToolSuccess(data={"items": ["a", "b", "c"]})

        assert result.data["items"] == ["a", "b", "c"]

    def test_success_is_frozen(self):
        """Test that ToolSuccess is immutable."""
        result = ToolSuccess(data={"key": "value"})

        with pytest.raises(ValidationError):
            result.data = {"new": "data"}  # type: ignore


class TestToolSuccessAccessors:
    """Test ToolSuccess type-safe accessors."""

    def test_get_str_returns_string_value(self):
        """Test get_str returns string when key exists with string value."""
        result = ToolSuccess(data={"name": "test"})

        assert result.get_str("name") == "test"

    def test_get_str_returns_default_for_missing_key(self):
        """Test get_str returns default when key doesn't exist."""
        result = ToolSuccess(data={"other": "value"})

        assert result.get_str("name") == ""
        assert result.get_str("name", "default") == "default"

    def test_get_str_returns_default_for_non_string_value(self):
        """Test get_str returns default when value is not a string."""
        result = ToolSuccess(data={"count": 42, "active": True, "items": ["a", "b"]})

        assert result.get_str("count") == ""
        assert result.get_str("active") == ""
        assert result.get_str("items") == ""
        assert result.get_str("count", "default") == "default"

    def test_get_int_returns_integer_value(self):
        """Test get_int returns integer when key exists with int value."""
        result = ToolSuccess(data={"count": 42})

        assert result.get_int("count") == 42

    def test_get_int_returns_default_for_missing_key(self):
        """Test get_int returns default when key doesn't exist."""
        result = ToolSuccess(data={"other": "value"})

        assert result.get_int("count") == 0
        assert result.get_int("count", -1) == -1

    def test_get_int_returns_default_for_bool_value(self):
        """Test get_int returns default for boolean (not treated as int)."""
        result = ToolSuccess(data={"flag": True})

        # bool is subclass of int in Python, but we don't want to treat it as int
        assert result.get_int("flag") == 0
        assert result.get_int("flag", 99) == 99

    def test_get_int_returns_default_for_non_int_value(self):
        """Test get_int returns default when value is not an integer."""
        result = ToolSuccess(data={"name": "test", "rate": 3.14, "items": ["a"]})

        assert result.get_int("name") == 0
        assert result.get_int("rate") == 0
        assert result.get_int("items") == 0

    def test_get_float_returns_float_value(self):
        """Test get_float returns float when key exists with float value."""
        result = ToolSuccess(data={"rate": 3.14})

        assert result.get_float("rate") == 3.14

    def test_get_float_converts_int_to_float(self):
        """Test get_float converts integer values to float."""
        result = ToolSuccess(data={"count": 42})

        assert result.get_float("count") == 42.0
        assert isinstance(result.get_float("count"), float)

    def test_get_float_returns_default_for_missing_key(self):
        """Test get_float returns default when key doesn't exist."""
        result = ToolSuccess(data={"other": "value"})

        assert result.get_float("rate") == 0.0
        assert result.get_float("rate", -1.5) == -1.5

    def test_get_float_returns_default_for_bool_value(self):
        """Test get_float returns default for boolean (not treated as float)."""
        result = ToolSuccess(data={"flag": True})

        assert result.get_float("flag") == 0.0
        assert result.get_float("flag", 99.9) == 99.9

    def test_get_float_returns_default_for_non_numeric_value(self):
        """Test get_float returns default when value is not numeric."""
        result = ToolSuccess(data={"name": "test", "items": ["a"]})

        assert result.get_float("name") == 0.0
        assert result.get_float("items") == 0.0

    def test_get_bool_returns_boolean_value(self):
        """Test get_bool returns boolean when key exists with bool value."""
        result = ToolSuccess(data={"active": True, "disabled": False})

        assert result.get_bool("active") is True
        assert result.get_bool("disabled") is False

    def test_get_bool_returns_default_for_missing_key(self):
        """Test get_bool returns default when key doesn't exist."""
        result = ToolSuccess(data={"other": "value"})

        assert result.get_bool("active") is False
        assert result.get_bool("active", True) is True

    def test_get_bool_returns_default_for_non_bool_value(self):
        """Test get_bool returns default when value is not a boolean."""
        result = ToolSuccess(data={"count": 1, "name": "true", "items": []})

        assert result.get_bool("count") is False
        assert result.get_bool("name") is False
        assert result.get_bool("items") is False

    def test_get_list_returns_list_value(self):
        """Test get_list returns list when key exists with list value."""
        result = ToolSuccess(data={"items": ["a", "b", "c"]})

        assert result.get_list("items") == ["a", "b", "c"]

    def test_get_list_returns_empty_list_for_missing_key(self):
        """Test get_list returns empty list when key doesn't exist."""
        result = ToolSuccess(data={"other": "value"})

        assert result.get_list("items") == []

    def test_get_list_returns_custom_default_for_missing_key(self):
        """Test get_list returns custom default when key doesn't exist."""
        result = ToolSuccess(data={"other": "value"})

        assert result.get_list("items", ["default"]) == ["default"]

    def test_get_list_returns_default_for_non_list_value(self):
        """Test get_list returns default when value is not a list."""
        result = ToolSuccess(data={"name": "test", "count": 42})

        assert result.get_list("name") == []
        assert result.get_list("count") == []
        assert result.get_list("name", ["default"]) == ["default"]


class TestToolError:
    """Test ToolError Pydantic model."""

    def test_create_error_with_valid_data(self):
        """Test creating ToolError with valid data."""
        error = ToolError(error_code="NOT_FOUND", error_message="Item not found")

        assert error.success is False
        assert error.error_code == "NOT_FOUND"
        assert error.error_message == "Item not found"

    def test_error_requires_error_code(self):
        """Test that error_code is required."""
        with pytest.raises(ValidationError):
            ToolError(error_code="", error_message="Some error")  # type: ignore

    def test_error_requires_error_message(self):
        """Test that error_message is required."""
        with pytest.raises(ValidationError):
            ToolError(error_code="ERROR", error_message="")  # type: ignore

    def test_error_is_frozen(self):
        """Test that ToolError is immutable."""
        error = ToolError(error_code="ERROR", error_message="Something failed")

        with pytest.raises(ValidationError):
            error.error_code = "NEW_CODE"  # type: ignore


class TestTypeGuards:
    """Test is_success and is_error type guard functions."""

    def test_is_success_returns_true_for_success(self):
        """Test is_success returns True for ToolSuccess."""
        result: ToolResult = ToolSuccess(data={"key": "value"})

        assert is_success(result) is True

    def test_is_success_returns_false_for_error(self):
        """Test is_success returns False for ToolError."""
        result: ToolResult = ToolError(error_code="ERROR", error_message="Failed")

        assert is_success(result) is False

    def test_is_error_returns_true_for_error(self):
        """Test is_error returns True for ToolError."""
        result: ToolResult = ToolError(error_code="ERROR", error_message="Failed")

        assert is_error(result) is True

    def test_is_error_returns_false_for_success(self):
        """Test is_error returns False for ToolSuccess."""
        result: ToolResult = ToolSuccess(data={"key": "value"})

        assert is_error(result) is False

    def test_type_guards_enable_type_narrowing(self):
        """Test that type guards work for type narrowing in conditional blocks."""
        success_result: ToolResult = ToolSuccess(data={"message": "ok"})
        error_result: ToolResult = ToolError(error_code="ERR", error_message="fail")

        # These should type-check correctly due to type guards
        if is_success(success_result):
            # Inside this block, success_result is narrowed to ToolSuccess
            assert success_result.data["message"] == "ok"

        if is_error(error_result):
            # Inside this block, error_result is narrowed to ToolError
            assert error_result.error_code == "ERR"
