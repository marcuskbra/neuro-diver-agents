"""Specialist agent factory - single factory function for all specialist agents."""

from collections.abc import Callable
from typing import Any

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from .agent_configs import AGENT_CONFIGS, AgentConfig, AgentType
from .retry_config import get_retry_config

# Type alias for ADK tools (can be Callable or ADK tool classes like GoogleSearchTool)
ToolType = Callable[..., Any] | Any


def create_specialist_agent(
    config: AgentConfig,
    tools: list[ToolType] | None = None,
) -> LlmAgent:
    """
    Create a specialist agent from configuration.

    This single factory function replaces 5 separate create_*() functions,
    reducing code duplication while maintaining type safety.

    Args:
        config: Agent configuration with name, description, and system prompt.
        tools: Optional list of tools for the agent. Defaults to empty list.

    Returns:
        Configured LlmAgent instance.
    """
    return LlmAgent(
        model=config.model,
        instruction=config.system_prompt,
        tools=tools or [],
        name=config.name,
        description=config.description,
        generate_content_config=get_retry_config(),
    )


def create_agent_by_type(
    agent_type: AgentType,
    tools: list[ToolType] | None = None,
) -> LlmAgent:
    """
    Create a specialist agent by type name.

    Args:
        agent_type: Type of agent to create (e.g., "adhd_expert").
        tools: Optional list of tools for the agent.

    Returns:
        Configured LlmAgent instance.

    Raises:
        KeyError: If agent_type is not a valid agent type.
    """
    config = AGENT_CONFIGS[agent_type]
    return create_specialist_agent(config, tools)


# =============================================================================
# Convenience functions for backward compatibility
# =============================================================================


def create_adhd_expert() -> LlmAgent:
    """Create ADHD specialist agent with Google Search capability.

    The ADHD expert can search the web for the latest research,
    strategies, and resources related to ADHD management.
    """
    return create_agent_by_type("adhd_expert", tools=[google_search])


def create_asd_expert() -> LlmAgent:
    """Create ASD specialist agent with Google Search capability.

    The ASD expert can search the web for autism support techniques,
    sensory strategies, and current research on ASD.
    """
    return create_agent_by_type("asd_expert", tools=[google_search])


def create_developmental_expert() -> LlmAgent:
    """Create developmental specialist agent with Google Search capability.

    The developmental expert can search for child development milestones,
    age-appropriate activities, and developmental research.
    """
    return create_agent_by_type("developmental_expert", tools=[google_search])


def create_memory_agent(tools: list[ToolType] | None = None) -> LlmAgent:
    """Create memory and pattern learning agent."""
    return create_agent_by_type("memory_agent", tools)


def create_activity_planner_agent(tools: list[ToolType] | None = None) -> LlmAgent:
    """Create activity planning agent."""
    return create_agent_by_type("activity_planner", tools)
