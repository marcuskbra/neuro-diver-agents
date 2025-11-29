"""Helper functions for specialist agent consultation."""

from __future__ import annotations

from collections.abc import Callable

from google import genai
from google.adk.agents import LlmAgent


def consult_specialist(
    agent_getter: Callable[[], LlmAgent],
    question: str,
    specialist_name: str,
) -> str:
    """
    Generic specialist consultation with error handling.

    This function uses the genai.Client directly to consult specialist agents,
    passing the agent's instruction as the system prompt.

    Args:
        agent_getter: Callable that returns the specialist agent instance.
        question: Question to ask the specialist.
        specialist_name: Human-readable name for error messages.

    Returns:
        The specialist's response text, or an error message.
    """
    try:
        agent: LlmAgent = agent_getter()

        # Use genai.Client directly with agent's instruction as system prompt
        client = genai.Client()
        response = client.models.generate_content(
            model=str(agent.model),
            contents=question,
            config=genai.types.GenerateContentConfig(
                system_instruction=agent.instruction,
            ),
        )

        if response.text:
            return response.text

        return f"No response from {specialist_name}"
    except Exception as e:
        return f"Error consulting {specialist_name}: {str(e)}"
