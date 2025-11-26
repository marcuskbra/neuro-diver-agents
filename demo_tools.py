"""Demo script showing type-safe tool usage."""

from datetime import datetime

from src.capstone.models import (
    ActivityGoal,
    ActivityRequest,
    ActivityType,
    BehaviorInput,
    SessionOutcome,
    TimeOfDay,
    ToolError,
    ToolSuccess,
)
from src.capstone.tools import (
    analyze_patterns,
    classify_behavior,
    get_activity_plan,
)


def demo_behavior_classification():
    """Demonstrate type-safe behavior classification."""
    print("=" * 80)
    print("DEMO 1: Behavior Classification")
    print("=" * 80)

    # Create validated input
    behavior_input = BehaviorInput(
        description="My son refused to start homework after playing video games for an hour. He got agitated when I reminded him it was time to work.",
        time_of_day=TimeOfDay.EVENING,
        activity_type=ActivityType.HOMEWORK,
        context="Transition from high-interest gaming to low-interest homework activity",
    )

    print("\n📋 Input:")
    print(f"  Description: {behavior_input.description[:80]}...")
    print(f"  Time: {behavior_input.time_of_day.value}")
    print(f"  Activity: {behavior_input.activity_type.value}")

    # Classify behavior (type-safe)
    result: ToolSuccess | ToolError = classify_behavior(behavior_input)

    print("\n🔍 Result:")
    if isinstance(result, ToolSuccess):
        print("  ✅ Success!")
        print("\n  ADHD Factors:")
        for factor in result.get_list("adhd_factors"):
            print(f"    - {factor}")
        print("\n  ASD Factors:")
        for factor in result.get_list("asd_factors"):
            print(f"    - {factor}")
        print("\n  Age-Typical Factors:")
        for factor in result.get_list("age_typical_factors"):
            print(f"    - {factor}")
        print(f"\n  Primary Driver: {result.get_str('primary_driver')}")
    elif isinstance(result, ToolError):
        print(f"  ❌ Error: {result.error_code}")
        print(f"  Message: {result.error_message}")


def demo_activity_planning():
    """Demonstrate type-safe activity planning."""
    print("\n\n" + "=" * 80)
    print("DEMO 2: Activity Planning")
    print("=" * 80)

    # Create validated request
    activity_request = ActivityRequest(
        goal=ActivityGoal.HOMEWORK_SUPPORT,
        duration_minutes=30,
        available_materials=["timer", "fidget"],
    )

    print("\n📋 Request:")
    print(f"  Goal: {activity_request.goal.value}")
    print(f"  Duration: {activity_request.duration_minutes} minutes")
    print(f"  Materials: {', '.join(activity_request.available_materials)}")

    # Get activity plan (type-safe)
    result = get_activity_plan(activity_request)

    print("\n🎯 Result:")
    if isinstance(result, ToolSuccess):
        print("  ✅ Success!")
        print(f"\n  📝 {result.get_str('name')}")
        print("\n  🛠️  Materials:")
        for material in result.get_list("materials"):
            print(f"    - {material}")
        print("\n  🏠 Setup:")
        print(f"    {result.get_str('setup')}")
        print("\n  ⏱️  Structure:")
        for step in result.get_list("structure"):
            print(f"    - {step}")
        print("\n  ✅ Success Criteria:")
        for criterion in result.get_list("success_criteria"):
            print(f"    - {criterion}")
    elif isinstance(result, ToolError):
        print(f"  ❌ Error: {result.error_code}")
        print(f"  Message: {result.error_message}")


def demo_pattern_analysis():
    """Demonstrate type-safe pattern analysis."""
    print("\n\n" + "=" * 80)
    print("DEMO 3: Pattern Analysis")
    print("=" * 80)

    # Create sample session history
    session_history = [
        SessionOutcome(
            strategy_used="Visual timer for bedtime",
            worked=True,
            notes="Used visual timer, smooth transition to bed",
            timestamp=datetime.now(),
        ),
        SessionOutcome(
            strategy_used="Verbal reminders only for bedtime",
            worked=False,
            notes="Just verbal reminders, resistance and meltdown. Screen time 30 min before bed.",
            timestamp=datetime.now(),
        ),
        SessionOutcome(
            strategy_used="Visual timer + sensory break for bedtime",
            worked=True,
            notes="Visual timer plus 5-min quiet time with weighted blanket worked well",
            timestamp=datetime.now(),
        ),
    ]

    print(f"\n📊 Analyzing {len(session_history)} sessions for 'bedtime' behavior")

    # Analyze patterns (type-safe)
    result = analyze_patterns(session_history, "bedtime")

    print("\n📈 Result:")
    if isinstance(result, ToolSuccess):
        print("  ✅ Success!")
        print(f"\n  🎯 Behavior: {result.get_str('behavior_type')}")
        print("\n  ⚠️  Common Triggers:")
        for trigger in result.get_list("common_triggers"):
            print(f"    - {trigger}")
        print("\n  ✅ Successful Strategies:")
        for strategy in result.get_list("successful_strategies"):
            print(f"    - {strategy}")
        print("\n  ❌ Unsuccessful Approaches:")
        for approach in result.get_list("unsuccessful_approaches"):
            print(f"    - {approach}")
        print(f"\n  📊 Success Rate: {result.get_int('frequency')}/{result.get_int('sessions')}")
    elif isinstance(result, ToolError):
        print(f"  ❌ Error: {result.error_code}")
        print(f"  Message: {result.error_message}")


if __name__ == "__main__":
    demo_behavior_classification()
    demo_activity_planning()
    demo_pattern_analysis()

    print("\n\n" + "=" * 80)
    print("✨ All demos completed successfully!")
    print("=" * 80)
