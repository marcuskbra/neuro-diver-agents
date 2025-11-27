"""ADK specialist agents for neurodivergent parenting support."""

from .coordinator import create_coordinator
from .parallel_analyzer import create_parallel_expert_panel, create_research_panel
from .research_pipeline import (
    create_behavior_analysis_pipeline,
    create_custom_pipeline,
    create_research_pipeline,
)
from .specialist_factory import (
    ToolType,
    create_activity_planner_agent,
    create_adhd_expert,
    create_agent_by_type,
    create_asd_expert,
    create_developmental_expert,
    create_memory_agent,
    create_specialist_agent,
)

__all__ = [
    # Main coordinator
    "create_coordinator",
    # Specialist agents (backward compatible)
    "create_adhd_expert",
    "create_asd_expert",
    "create_developmental_expert",
    "create_memory_agent",
    "create_activity_planner_agent",
    # New factory functions
    "create_specialist_agent",
    "create_agent_by_type",
    # ADK Orchestration Patterns
    "create_parallel_expert_panel",
    "create_research_panel",
    "create_research_pipeline",
    "create_behavior_analysis_pipeline",
    "create_custom_pipeline",
    # Type definitions
    "ToolType",
]
