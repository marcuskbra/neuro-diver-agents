"""Type-safe pattern analysis tool."""

from ..models.memory import BehaviorPattern, SessionOutcome
from ..models.results import ToolError, ToolResult, ToolSuccess


def analyze_patterns(
    session_history: list[SessionOutcome],
    behavior_type: str,
) -> ToolResult:
    """
    Analyze behavioral patterns from session history.

    Args:
        session_history: List of validated session outcomes
        behavior_type: Type of behavior to analyze (e.g., "bedtime", "homework")

    Returns:
        ToolResult: Success with BehaviorPattern or Error if insufficient data
    """
    try:
        if len(session_history) < 1:
            return ToolError(
                error_code="INSUFFICIENT_DATA",
                error_message="Need at least 1 session for pattern analysis",
            )

        # Filter relevant sessions
        relevant_sessions = [
            s
            for s in session_history
            if behavior_type.lower() in s.strategy_used.lower()
            or behavior_type.lower() in s.notes.lower()
        ]

        if len(relevant_sessions) == 0:
            return ToolError(
                error_code="NO_MATCHING_SESSIONS",
                error_message=f"No sessions found for behavior type: {behavior_type}",
            )

        # Analyze successful strategies
        successful: list[str] = []
        unsuccessful: list[str] = []

        for session in relevant_sessions:
            if session.worked:
                successful.append(session.strategy_used)
            else:
                unsuccessful.append(session.strategy_used)

        # Extract common triggers from notes (simplified pattern matching)
        triggers: list[str] = []
        for session in relevant_sessions:
            notes_lower = session.notes.lower()
            if "screen time" in notes_lower:
                triggers.append("Screen time within 1 hour")
            if "skip" in notes_lower or "missed" in notes_lower:
                triggers.append("Skipped routine step")
            if "change" in notes_lower or "unexpected" in notes_lower:
                triggers.append("Schedule disruption earlier in day")

        # Count frequency (number of successful outcomes)
        frequency = sum(1 for s in relevant_sessions if s.worked)
        total_sessions = len(relevant_sessions)

        # Ensure frequency doesn't exceed total sessions (validation requirement)
        if frequency > total_sessions:
            frequency = total_sessions

        pattern = BehaviorPattern(
            behavior_type=behavior_type,
            common_triggers=list(set(triggers)),
            successful_strategies=list(set(successful)),
            unsuccessful_approaches=list(set(unsuccessful)),
            frequency_count=frequency,
            sessions_analyzed=total_sessions,
        )

        return ToolSuccess(
            data={
                "behavior_type": pattern.behavior_type,
                "common_triggers": pattern.common_triggers,
                "successful_strategies": pattern.successful_strategies,
                "unsuccessful_approaches": pattern.unsuccessful_approaches,
                "frequency": pattern.frequency_count,
                "sessions": pattern.sessions_analyzed,
            }
        )

    except Exception as e:
        return ToolError(
            error_code="ANALYSIS_ERROR",
            error_message=f"Failed to analyze patterns: {str(e)}",
        )
