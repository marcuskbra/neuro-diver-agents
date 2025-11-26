"""Tool wrapper functions for coordinator agent."""

import json
from collections.abc import Callable

from ..models import (
    ActivityGoal,
    ActivityRequest,
    ActivityType,
    BehaviorInput,
    SessionOutcome,
    TimeOfDay,
)
from ..models.results import ToolError, ToolSuccess
from ..tools.activity_planner import get_activity_plan
from ..tools.behavior_classifier import classify_behavior
from ..tools.pattern_analyzer import analyze_patterns
from .tool_formatters import (
    format_activity_plan,
    format_behavior_analysis,
    format_pattern_analysis,
)


def create_analyze_behavior_wrapper() -> Callable[..., str]:
    """Create wrapper for behavior classifier tool."""

    def _analyze_behavior_wrapper(
        description: str,
        time_of_day: TimeOfDay,
        activity_type: ActivityType,
        context: str,
    ) -> str:
        """Analyze behavior using the classifier tool."""
        behavior_input = BehaviorInput(
            description=description,
            time_of_day=time_of_day,
            activity_type=activity_type,
            context=context,
        )
        result = classify_behavior(behavior_input)

        if isinstance(result, ToolError):
            return f"Error analyzing behavior: {result.error_message}"

        # Type narrowing: result is ToolSuccess
        assert isinstance(result, ToolSuccess)
        return format_behavior_analysis(result.data)

    return _analyze_behavior_wrapper


def create_plan_activity_wrapper() -> Callable[..., str]:
    """Create wrapper for activity planner tool."""

    def _plan_activity_wrapper(
        goal: str,
        duration_minutes: int,
        materials: str,
    ) -> str:
        """Plan an activity using the planner tool."""
        try:
            # Parse materials from comma-separated string
            materials_list = [m.strip() for m in materials.split(",") if m.strip()]

            # Parse goal string to enum
            goal_enum = ActivityGoal(goal)

            # Create activity request
            request = ActivityRequest(
                goal=goal_enum,
                duration_minutes=duration_minutes,
                available_materials=materials_list,
            )

            # Plan activity
            result = get_activity_plan(request)

            if isinstance(result, ToolError):
                return f"Error planning activity: {result.error_message}"

            # Type narrowing: result is ToolSuccess
            assert isinstance(result, ToolSuccess)
            return format_activity_plan(result.data)

        except Exception as e:
            return f"Error: {str(e)}"

    return _plan_activity_wrapper


def create_analyze_patterns_wrapper() -> Callable[..., str]:
    """Create wrapper for pattern analyzer tool."""

    def _analyze_patterns_wrapper(
        session_history_json: str,
        behavior_type: str,
    ) -> str:
        """Analyze patterns from session history."""
        try:
            # Parse JSON session history
            session_data = json.loads(session_history_json)
            session_outcomes = []

            for session in session_data:
                outcome = SessionOutcome(
                    strategy_used=session["strategy_used"],
                    worked=session["worked"],
                    notes=session["notes"],
                )
                session_outcomes.append(outcome)

            # Analyze patterns
            result = analyze_patterns(session_outcomes, behavior_type)

            if isinstance(result, ToolError):
                return f"Error analyzing patterns: {result.error_message}"

            # Type narrowing: result is ToolSuccess
            assert isinstance(result, ToolSuccess)
            return format_pattern_analysis(result.data)

        except json.JSONDecodeError as e:
            return f"Error parsing session history JSON: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

    return _analyze_patterns_wrapper
