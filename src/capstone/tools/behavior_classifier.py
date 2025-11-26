"""Type-safe behavior classification tool."""

from ..models.behavior import (
    ActivityType,
    BehaviorAnalysis,
    BehaviorFactor,
    BehaviorInput,
)
from ..models.results import ToolError, ToolResult, ToolSuccess


def classify_behavior(behavior_input: BehaviorInput) -> ToolResult:
    """
    Classify behavior into ADHD/ASD/age-typical factors.

    Args:
        behavior_input: Validated behavior input with description and context

    Returns:
        ToolResult: Success with BehaviorAnalysis or Error with details
    """
    try:
        description_lower = behavior_input.description.lower()
        context_lower = behavior_input.context.lower()
        combined_text = f"{description_lower} {context_lower}"

        # Pattern matching for ADHD indicators
        adhd_factors: list[str] = []
        if any(
            keyword in combined_text
            for keyword in ["distracted", "focus", "attention", "concentrate"]
        ):
            adhd_factors.append("Attention regulation challenge")
        if any(keyword in combined_text for keyword in ["transition", "switching"]):
            adhd_factors.append("Executive function: difficulty with transitions")
        if "task" in combined_text and any(
            keyword in combined_text for keyword in ["start", "initiate", "begin"]
        ):
            adhd_factors.append("Executive function: task initiation difficulty")
        if any(keyword in combined_text for keyword in ["organize", "plan", "remember"]):
            adhd_factors.append("Executive function: planning and organization")
        if any(keyword in combined_text for keyword in ["impulsive", "interrupt"]):
            adhd_factors.append("Impulse control challenge")

        # Pattern matching for ASD indicators
        asd_factors: list[str] = []
        if any(keyword in combined_text for keyword in ["routine", "change", "unexpected"]):
            asd_factors.append("Routine disruption sensitivity")
        if any(keyword in combined_text for keyword in ["alone", "independent"]):
            asd_factors.append("Social/independence adjustment")
        if any(keyword in combined_text for keyword in ["sensory", "noise", "loud"]):
            asd_factors.append("Sensory processing needs")
        if any(keyword in combined_text for keyword in ["social", "friend", "peer"]):
            asd_factors.append("Social communication challenge")
        if any(keyword in combined_text for keyword in ["rigid", "flexible", "adapt"]):
            asd_factors.append("Cognitive flexibility challenge")

        # Age-typical factors
        age_typical: list[str] = []
        if behavior_input.activity_type == ActivityType.HOMEWORK:
            age_typical.append("Homework resistance common at age 8")
        if any(keyword in combined_text for keyword in ["refused", "won't", "no"]):
            age_typical.append("Testing boundaries - developmental stage")
        if behavior_input.activity_type == ActivityType.BEDTIME_ROUTINE:
            age_typical.append("Bedtime resistance typical for age group")
        if "independent" in combined_text or "alone" in combined_text:
            age_typical.append("Seeking independence - age-appropriate development")

        # Determine primary driver
        adhd_count = len(adhd_factors)
        asd_count = len(asd_factors)
        typical_count = len(age_typical)

        if adhd_count > 0 and asd_count > 0 and adhd_count == asd_count:
            primary = BehaviorFactor.COMBINED
        elif adhd_count > asd_count and adhd_count > typical_count:
            primary = BehaviorFactor.ADHD
        elif asd_count > adhd_count and asd_count > typical_count:
            primary = BehaviorFactor.ASD
        elif adhd_count > 0 and asd_count > 0:
            primary = BehaviorFactor.COMBINED
        else:
            primary = BehaviorFactor.AGE_TYPICAL

        # Create and validate analysis using Pydantic model
        analysis = BehaviorAnalysis(
            adhd_factors=adhd_factors,
            asd_factors=asd_factors,
            age_typical_factors=age_typical,
            primary_driver=primary,
        )

        # Use validated model for response
        return ToolSuccess(
            data={
                "adhd_factors": analysis.adhd_factors,
                "asd_factors": analysis.asd_factors,
                "age_typical_factors": analysis.age_typical_factors,
                "primary_driver": analysis.primary_driver.value,
            }
        )

    except Exception as e:
        return ToolError(
            error_code="CLASSIFICATION_ERROR",
            error_message=f"Failed to classify behavior: {str(e)}",
        )
