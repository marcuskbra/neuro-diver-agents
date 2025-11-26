"""Helper functions for specialist agent consultation."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from google.adk.agents import LlmAgent


def consult_specialist(
    agent_getter: Callable[[], LlmAgent],
    question: str,
    specialist_name: str,
) -> str:
    """
    Generic specialist consultation with error handling.

    This function replaces 5 nearly identical consultation functions,
    reducing code duplication while maintaining consistent error handling.

    Args:
        agent_getter: Callable that returns the specialist agent instance.
        question: Question to ask the specialist.
        specialist_name: Human-readable name for error messages.

    Returns:
        The specialist's response text, or an error message.
    """
    try:
        agent = agent_getter()
        # Use getattr to safely access generate_content method
        generate_method = getattr(agent, "generate_content", None)
        if generate_method is None:
            return f"Error: {specialist_name} agent does not have generate_content method"
        response: Any = generate_method(question)
        if hasattr(response, "text"):
            return str(response.text)
        return str(response)
    except Exception as e:
        return f"Error consulting {specialist_name}: {str(e)}"
