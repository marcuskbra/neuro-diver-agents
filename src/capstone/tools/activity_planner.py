"""Type-safe activity planning tool."""

from ..models.activity import ActivityGoal, ActivityPlan, ActivityRequest
from ..models.results import ToolError, ToolResult, ToolSuccess

# Activity template database (type-safe)
ACTIVITY_TEMPLATES: dict[ActivityGoal, ActivityPlan] = {
    ActivityGoal.EXECUTIVE_FUNCTION: ActivityPlan(
        name="Morning Routine Mission",
        goal=ActivityGoal.EXECUTIVE_FUNCTION,
        materials=[
            "Visual checklist with pictures",
            "Timer (5 minutes per task)",
            "Reward stickers",
            "Distraction blocker sign",
        ],
        environmental_setup=(
            "Bathroom: Remove extra toys, toothbrush in clear view. "
            "Bedroom: Lay out clothes night before. Minimize choices."
        ),
        duration_minutes=15,
        structure=[
            "Brush teeth: 5 min (timer)",
            "Get dressed: 5 min (timer)",
            "Check-in: 5 min (review together)",
        ],
        success_criteria=[
            "Completes 1 task without redirection",
            "Uses visual checklist at least once",
            "Acknowledges distraction and refocuses",
        ],
        adaptations=[
            "Low energy: Reduce to 1 task only",
            "High distraction: Parent stays nearby",
            "Resistance: Offer choice of task order",
        ],
    ),
    ActivityGoal.TRANSITION_SUPPORT: ActivityPlan(
        name="Transition Timer Activity",
        goal=ActivityGoal.TRANSITION_SUPPORT,
        materials=[
            "Visual timer",
            "Transition warning cards",
            "Next activity picture",
        ],
        environmental_setup="Quiet space for transition preparation, minimal distractions",
        duration_minutes=10,
        structure=[
            "5-min warning with visual",
            "2-min warning with verbal cue",
            "Transition to next activity",
        ],
        success_criteria=[
            "Acknowledges warnings",
            "Transitions within 2 minutes of timer",
            "No major resistance",
        ],
        adaptations=[
            "Extra time: Add 10-min warning",
            "High resistance: Break into smaller steps",
        ],
    ),
    ActivityGoal.HOMEWORK_SUPPORT: ActivityPlan(
        name="Homework Break Down Strategy",
        goal=ActivityGoal.HOMEWORK_SUPPORT,
        materials=[
            "Homework divided into segments",
            "Timer for each segment",
            "Break activity (fidget, stretch)",
            "Reward system",
        ],
        environmental_setup=(
            "Quiet corner, minimal visual distractions, all materials ready before starting"
        ),
        duration_minutes=30,
        structure=[
            "Segment 1: 10 min work + 5 min break",
            "Segment 2: 10 min work + 5 min break",
        ],
        success_criteria=[
            "Completes 1 segment",
            "Takes break when timer rings",
            "Returns to work after break",
        ],
        adaptations=[
            "Overwhelm: Reduce to 1 segment",
            "High energy: Add movement breaks",
            "Low motivation: Increase reward frequency",
        ],
    ),
    ActivityGoal.ENGAGEMENT: ActivityPlan(
        name="Two-Person Board Game Practice",
        goal=ActivityGoal.ENGAGEMENT,
        materials=[
            "Simple board game (Uno, Connect 4, checkers)",
            "Visual timer",
            "Feelings chart",
        ],
        environmental_setup="Quiet corner, 2 chairs facing each other, table for game",
        duration_minutes=20,
        structure=[
            "Setup: 5 min",
            "Play: 10 min",
            "Reflection: 5 min",
        ],
        success_criteria=[
            "Takes 2-3 turns appropriately",
            "Uses 1-2 social phrases",
            "Expresses 1 feeling during game",
        ],
        adaptations=[
            "Frustration: Pause and use calming strategy",
            "Low engagement: Switch to more active game",
        ],
    ),
}


def get_activity_plan(request: ActivityRequest) -> ToolResult:
    """
    Get structured activity plan based on goal.

    Args:
        request: Validated activity request with goal and constraints

    Returns:
        ToolResult: Success with ActivityPlan or Error if goal not found
    """
    try:
        if request.goal not in ACTIVITY_TEMPLATES:
            return ToolError(
                error_code="INVALID_GOAL",
                error_message=f"Activity goal {request.goal.value} not supported",
            )

        plan = ACTIVITY_TEMPLATES[request.goal]

        # Adjust duration if requested differs from template
        if request.duration_minutes != plan.duration_minutes:
            # Create adjusted plan (immutable, so create new instance)
            plan = ActivityPlan(
                name=plan.name,
                goal=plan.goal,
                materials=plan.materials,
                environmental_setup=plan.environmental_setup,
                duration_minutes=request.duration_minutes,
                structure=plan.structure,
                success_criteria=plan.success_criteria,
                adaptations=plan.adaptations,
            )

        return ToolSuccess(
            data={
                "name": plan.name,
                "goal": plan.goal.value,
                "materials": plan.materials,
                "setup": plan.environmental_setup,
                "duration": plan.duration_minutes,
                "structure": plan.structure,
                "success_criteria": plan.success_criteria,
                "adaptations": plan.adaptations,
            }
        )

    except Exception as e:
        return ToolError(
            error_code="PLANNING_ERROR",
            error_message=f"Failed to generate activity plan: {str(e)}",
        )
