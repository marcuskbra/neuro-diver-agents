"""Parallel agent for simultaneous expert consultation.

This module implements a ParallelAgent that consults multiple specialists
in parallel, enabling faster multi-perspective analysis of parenting situations.
"""

from google.adk.agents import LlmAgent, ParallelAgent


def create_parallel_expert_panel(
    adhd_expert: LlmAgent,
    asd_expert: LlmAgent,
    developmental_expert: LlmAgent,
) -> ParallelAgent:
    """Create a parallel analyzer for simultaneous expert consultation.

    The parallel expert panel consults ADHD, ASD, and developmental specialists
    simultaneously, enabling faster comprehensive analysis. Each expert can
    use Google Search to research the latest strategies and resources.

    This demonstrates the ADK ParallelAgent pattern where multiple sub-agents
    process the same input concurrently, with results aggregated for synthesis.

    Args:
        adhd_expert: ADHD specialist agent with Google Search capability.
        asd_expert: ASD specialist agent with Google Search capability.
        developmental_expert: Developmental specialist with Google Search.

    Returns:
        ParallelAgent that orchestrates simultaneous expert consultation.

    Example:
        >>> adhd = create_adhd_expert()
        >>> asd = create_asd_expert()
        >>> dev = create_developmental_expert()
        >>> panel = create_parallel_expert_panel(adhd, asd, dev)
        >>> # Panel consults all three experts in parallel
    """
    return ParallelAgent(
        name="parallel_expert_panel",
        description=(
            "Consults ADHD, ASD, and developmental experts in parallel "
            "for comprehensive multi-perspective analysis. Each expert "
            "can search the web for the latest research and strategies."
        ),
        sub_agents=[adhd_expert, asd_expert, developmental_expert],
    )


def create_research_panel(
    *experts: LlmAgent,
) -> ParallelAgent:
    """Create a flexible parallel research panel with any number of experts.

    This factory allows creating a parallel panel with a variable number
    of specialist agents, useful for custom expert combinations.

    Args:
        *experts: Variable number of specialist agents to consult in parallel.

    Returns:
        ParallelAgent that orchestrates the provided experts.

    Example:
        >>> panel = create_research_panel(adhd_expert, asd_expert)
        >>> # Consults only ADHD and ASD experts in parallel
    """
    return ParallelAgent(
        name="research_panel",
        description=(
            f"Parallel research panel with {len(experts)} specialists "
            "for concurrent multi-perspective analysis."
        ),
        sub_agents=list(experts),
    )
