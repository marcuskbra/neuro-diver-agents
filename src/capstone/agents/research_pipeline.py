"""Sequential agent for structured research pipelines.

This module implements a SequentialAgent that processes information through
a defined pipeline of specialists, enabling deep investigation workflows.
"""

from google.adk.agents import LlmAgent, SequentialAgent


def create_research_pipeline(
    researcher: LlmAgent,
    analyzer: LlmAgent,
    synthesizer: LlmAgent,
) -> SequentialAgent:
    """Create a sequential research pipeline for deep investigation.

    The research pipeline processes queries through three stages:
    1. Research: Gather information and search for relevant data
    2. Analyze: Identify patterns, relationships, and key insights
    3. Synthesize: Combine findings into actionable recommendations

    This demonstrates the ADK SequentialAgent pattern where sub-agents
    process information in order, with each stage building on the previous.

    Args:
        researcher: Agent responsible for information gathering.
        analyzer: Agent responsible for pattern analysis.
        synthesizer: Agent responsible for combining insights.

    Returns:
        SequentialAgent that orchestrates the research pipeline.

    Example:
        >>> researcher = create_adhd_expert()  # Has Google Search
        >>> analyzer = create_asd_expert()     # Has Google Search
        >>> synthesizer = create_developmental_expert()  # Has Google Search
        >>> pipeline = create_research_pipeline(researcher, analyzer, synthesizer)
        >>> # Pipeline processes: Research -> Analyze -> Synthesize
    """
    return SequentialAgent(
        name="research_pipeline",
        description=(
            "Sequential research pipeline that processes queries through "
            "three stages: Research (gather information), Analyze (identify "
            "patterns), and Synthesize (create recommendations). Each stage "
            "builds on the previous, enabling deep investigation workflows."
        ),
        sub_agents=[researcher, analyzer, synthesizer],
    )


def create_behavior_analysis_pipeline() -> SequentialAgent:
    """Create a specialized pipeline for child behavior analysis.

    This pipeline uses three specialized stages:
    1. ADHD Expert: Research ADHD-related behaviors and strategies
    2. ASD Expert: Analyze autism spectrum considerations
    3. Developmental Expert: Synthesize age-appropriate recommendations

    Returns:
        SequentialAgent configured for behavior analysis workflow.

    Example:
        >>> pipeline = create_behavior_analysis_pipeline()
        >>> # Automatically uses specialists with Google Search
    """
    from .specialist_factory import (
        create_adhd_expert,
        create_asd_expert,
        create_developmental_expert,
    )

    return SequentialAgent(
        name="behavior_analysis_pipeline",
        description=(
            "Specialized sequential pipeline for child behavior analysis. "
            "Stage 1: ADHD specialist researches attention-related factors. "
            "Stage 2: ASD specialist analyzes sensory and social aspects. "
            "Stage 3: Developmental specialist synthesizes age-appropriate "
            "strategies. Each specialist can search for the latest research."
        ),
        sub_agents=[
            create_adhd_expert(),
            create_asd_expert(),
            create_developmental_expert(),
        ],
    )


def create_custom_pipeline(
    *stages: LlmAgent,
    name: str = "custom_pipeline",
    description: str | None = None,
) -> SequentialAgent:
    """Create a custom sequential pipeline with any number of stages.

    This factory allows creating a sequential pipeline with a variable
    number of specialist agents, useful for custom workflows.

    Args:
        *stages: Variable number of agents defining pipeline stages.
        name: Name for the pipeline (default: "custom_pipeline").
        description: Optional description (auto-generated if not provided).

    Returns:
        SequentialAgent that orchestrates the provided stages.

    Example:
        >>> pipeline = create_custom_pipeline(
        ...     adhd_expert,
        ...     developmental_expert,
        ...     name="adhd_dev_pipeline",
        ... )
        >>> # Two-stage pipeline: ADHD -> Development
    """
    auto_description = (
        f"Custom sequential pipeline with {len(stages)} stages. "
        f"Processes queries through each stage in order."
    )
    return SequentialAgent(
        name=name,
        description=description or auto_description,
        sub_agents=list(stages),
    )
