"""Parenting coordinator agent that orchestrates specialist agents."""

from google.adk.agents import LlmAgent

from ..infrastructure.agent_factory import AgentFactory
from .agent_configs import COORDINATOR_SYSTEM_PROMPT
from .retry_config import get_retry_config
from .specialist_helpers import consult_specialist
from .tool_wrappers import (
    create_analyze_behavior_wrapper,
    create_analyze_patterns_wrapper,
    create_plan_activity_wrapper,
)


def create_coordinator(agent_factory: AgentFactory | None = None) -> LlmAgent:
    """
    Create parenting coordinator agent with dependency injection.

    This agent orchestrates 5 specialist agents:
    1. ADHD Expert - Executive function and attention challenges
    2. ASD Expert - Sensory processing and communication patterns
    3. Developmental Expert - Age-appropriate expectations
    4. Memory Agent - Pattern learning from past experiences
    5. Activity Planner - Structured activity recommendations

    The coordinator:
    - Routes questions to appropriate specialists
    - Synthesizes insights from multiple experts
    - Provides comprehensive, personalized support
    - Maintains empathetic, supportive communication

    Args:
        agent_factory: Optional AgentFactory instance for dependency injection.
                      If None, creates a new factory instance.

    Returns:
        Configured LlmAgent coordinator instance.
    """
    # Use injected factory or create new one (dependency injection)
    factory = agent_factory or AgentFactory()

    # Create specialist consultation functions using the factory
    def _consult_adhd_expert(question: str) -> str:
        """Consult ADHD specialist agent."""
        return consult_specialist(
            agent_getter=factory.get_adhd_expert,
            question=question,
            specialist_name="ADHD expert",
        )

    def _consult_asd_expert(question: str) -> str:
        """Consult ASD specialist agent."""
        return consult_specialist(
            agent_getter=factory.get_asd_expert,
            question=question,
            specialist_name="ASD expert",
        )

    def _consult_developmental_expert(question: str) -> str:
        """Consult developmental specialist agent."""
        return consult_specialist(
            agent_getter=factory.get_developmental_expert,
            question=question,
            specialist_name="developmental expert",
        )

    def _consult_memory_agent(question: str) -> str:
        """Consult memory and pattern learning agent."""
        return consult_specialist(
            agent_getter=lambda: factory.get_memory_agent(tools=[]),
            question=question,
            specialist_name="memory agent",
        )

    def _consult_activity_planner(question: str) -> str:
        """Consult activity planning specialist agent."""
        return consult_specialist(
            agent_getter=lambda: factory.get_activity_planner_agent(tools=[]),
            question=question,
            specialist_name="activity planner",
        )

    # Create tool wrappers
    _analyze_behavior_wrapper = create_analyze_behavior_wrapper()
    _plan_activity_wrapper = create_plan_activity_wrapper()
    _analyze_patterns_wrapper = create_analyze_patterns_wrapper()

    # Combine all tools - pass raw Python callables
    all_tools = [
        # Specialist agents as raw Python functions
        _consult_adhd_expert,
        _consult_asd_expert,
        _consult_developmental_expert,
        _consult_memory_agent,
        _consult_activity_planner,
        # Direct capability functions
        _analyze_behavior_wrapper,
        _plan_activity_wrapper,
        _analyze_patterns_wrapper,
    ]

    # Create coordinator agent with retry config (ADK best practice for 429 errors)
    coordinator = LlmAgent(
        model="gemini-2.0-flash-exp",
        instruction=COORDINATOR_SYSTEM_PROMPT,
        tools=all_tools,
        name="parenting_coordinator",
        description="Orchestrates specialist agents to provide comprehensive parenting support for neurodivergent children",
        generate_content_config=get_retry_config(),
    )

    return coordinator
