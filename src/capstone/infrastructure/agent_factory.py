"""Agent factory for creating and caching specialist agents."""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from ..agents.agent_configs import AGENT_CONFIGS
from ..agents.specialist_factory import ToolType, create_specialist_agent


class AgentFactory:
    """Factory for creating and caching specialist agents.

    Provides thread-safe agent creation with caching to avoid
    recreating agents on every request. Uses the centralized
    agent configuration system for consistency.

    Example:
        factory = AgentFactory()
        adhd_agent = factory.get_adhd_expert()  # Creates and caches
        adhd_agent2 = factory.get_adhd_expert()  # Returns cached instance
        assert adhd_agent is adhd_agent2  # Same instance
    """

    def __init__(self) -> None:
        """Initialize empty agent cache."""
        self._cache: dict[str, LlmAgent] = {}

    def get_adhd_expert(self) -> LlmAgent:
        """Get or create ADHD specialist agent with Google Search.

        The ADHD expert can search the web for the latest research,
        strategies, and resources related to ADHD management.
        """
        if "adhd_expert" not in self._cache:
            config = AGENT_CONFIGS["adhd_expert"]
            self._cache["adhd_expert"] = create_specialist_agent(config, tools=[google_search])
        return self._cache["adhd_expert"]

    def get_asd_expert(self) -> LlmAgent:
        """Get or create ASD specialist agent with Google Search.

        The ASD expert can search the web for autism support techniques,
        sensory strategies, and current research on ASD.
        """
        if "asd_expert" not in self._cache:
            config = AGENT_CONFIGS["asd_expert"]
            self._cache["asd_expert"] = create_specialist_agent(config, tools=[google_search])
        return self._cache["asd_expert"]

    def get_developmental_expert(self) -> LlmAgent:
        """Get or create developmental specialist agent with Google Search.

        The developmental expert can search for child development milestones,
        age-appropriate activities, and developmental research.
        """
        if "developmental_expert" not in self._cache:
            config = AGENT_CONFIGS["developmental_expert"]
            self._cache["developmental_expert"] = create_specialist_agent(
                config, tools=[google_search]
            )
        return self._cache["developmental_expert"]

    def get_memory_agent(self, tools: list[ToolType]) -> LlmAgent:
        """Get or create memory management agent with tools.

        Args:
            tools: List of memory management tools to provide to agent.

        Returns:
            Configured memory agent with provided tools.
        """
        if "memory_agent" not in self._cache:
            config = AGENT_CONFIGS["memory_agent"]
            self._cache["memory_agent"] = create_specialist_agent(config, tools)
        return self._cache["memory_agent"]

    def get_activity_planner_agent(self, tools: list[ToolType]) -> LlmAgent:
        """Get or create activity planning agent with tools.

        Args:
            tools: List of activity planning tools to provide to agent.

        Returns:
            Configured activity planning agent with provided tools.
        """
        if "activity_planner_agent" not in self._cache:
            config = AGENT_CONFIGS["activity_planner"]
            self._cache["activity_planner_agent"] = create_specialist_agent(config, tools)
        return self._cache["activity_planner_agent"]

    def clear_cache(self) -> None:
        """Clear all cached agents.

        Useful for testing or when agents need to be recreated.
        """
        self._cache.clear()
