"""Demo script showcasing ADK multi-agent system."""

import asyncio
import os
import re

from google import genai
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from src.capstone.agents import create_coordinator


def print_separator(title: str) -> None:
    """Print formatted section separator."""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80 + "\n")


def extract_retry_delay(error_message: str) -> float:
    """Extract retry delay in seconds from error message.

    Args:
        error_message: Error message containing retry delay

    Returns:
        Delay in seconds, defaults to 10.0 if not found
    """
    # Look for "Please retry in X.Xs" or "retryDelay': 'Xs'"
    match = re.search(r"retry in (\d+\.?\d*)s", error_message)
    if match:
        return float(match.group(1))

    match = re.search(r"retryDelay.*?(\d+)s", error_message)
    if match:
        return float(match.group(1))

    return 10.0  # Default to 10 seconds


async def run_scenario_with_retry(
    runner: Runner,
    user_id: str,
    session_id: str,
    message: genai.types.Content,
    max_retries: int = 3,
) -> None:
    """Run a scenario with automatic retry on 429 errors.

    Args:
        runner: ADK Runner instance
        user_id: User ID for the session
        session_id: Session ID
        message: Message content to send
        max_retries: Maximum number of retries
    """
    for attempt in range(max_retries):
        try:
            response_received = False
            final_response = ""
            event_count = 0

            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=message,
            ):
                event_count += 1

                # Check for agent thinking/calling tools
                if hasattr(event, "agent_turn_event"):
                    agent_event = event.agent_turn_event
                    if hasattr(agent_event, "agent_name"):
                        print(f"  🤖 {agent_event.agent_name} is analyzing...")

                # Check for final text response in event.content
                if hasattr(event, "content") and event.content:
                    content = event.content
                    has_text = False

                    if hasattr(content, "parts") and content.parts:
                        # Check if any part is text (not function_call)
                        text_parts = []
                        for part in content.parts:
                            if hasattr(part, "text") and part.text:
                                text_parts.append(part.text)

                        if text_parts:
                            has_text = True
                            final_response = "\n".join(text_parts)

                    if has_text:
                        response_received = True
                        print(f"  ✅ Got text response after {event_count} events")
                        # Break on first text response
                        break

            # Print final response after all events processed
            if response_received and final_response:
                print(f"\n💬 Response:\n{final_response}\n")
                return  # Success!
            else:
                print(f"  ⚠️ No text response after {event_count} events")

        except Exception as e:
            error_str = str(e)

            # Check if it's a 429 rate limit error
            if "429" in error_str and "RESOURCE_EXHAUSTED" in error_str:
                retry_delay = extract_retry_delay(error_str)

                if attempt < max_retries - 1:
                    print(
                        f"\n⏳ Rate limit hit. Waiting {retry_delay:.1f}s before retry (attempt {attempt + 1}/{max_retries})..."
                    )
                    await asyncio.sleep(retry_delay)
                    print("🔄 Retrying...\n")
                else:
                    print(f"\n❌ Rate limit exceeded after {max_retries} attempts.")
                    print("💡 Tips to resolve:")
                    print("   • Wait a few minutes before running again")
                    print("   • Check your API quota at: https://ai.dev/usage?tab=rate-limit")
                    print("   • Consider upgrading your plan for higher limits")
                    return
            else:
                # Non-429 error, don't retry
                print(f"❌ Error: {error_str}")
                return


async def main():
    """Run multi-agent system demo scenarios."""
    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY environment variable not set")
        print("Please set your API key:")
        print('  export GOOGLE_API_KEY="your-api-key-here"')
        return

    print_separator("🤖 Neurodivergent Parenting Support Agent - ADK Demo")
    print("Demonstrating multi-agent hierarchical system with:")
    print("  • Parenting Coordinator (Manager)")
    print("  • 5 Specialist Agents (ADHD, ASD, Developmental, Memory, Activity Planner)")
    print("  • Custom tools (Behavior Classifier, Activity Planner, Pattern Analyzer)")
    print("  • Google Search integration")
    print(
        "\n💡 Note: Retry handling follows ADK best practices with agent-level retries + application-level fallback."
    )

    # Create coordinator (which creates all specialists)
    print("\n🔧 Initializing multi-agent system...")
    coordinator = create_coordinator()

    # Create runner with session service
    session_service = InMemorySessionService()
    runner = Runner(
        app_name="agents",
        agent=coordinator,
        session_service=session_service,
    )

    # Demo Scenario 1: Behavioral Analysis
    print_separator("📋 SCENARIO 1: Homework Refusal Analysis")
    print("Parent Question:")
    scenario_1 = """My 8-year-old son refuses to start his homework after school.
He just played video games for an hour and now says he's "too tired" for homework.
When I try to get him started, he gets frustrated and sometimes has a meltdown.
This happens most evenings around 5-6pm. Is this ADHD, autism, or just being 8?"""

    print(f'"{scenario_1}"\n')
    print("🤖 Coordinator orchestrating specialists...\n")

    # Create session for scenario 1
    await session_service.create_session(
        app_name="agents",
        user_id="demo_user",
        session_id="scenario_1",
    )

    # Run scenario with automatic retry
    await run_scenario_with_retry(
        runner=runner,
        user_id="demo_user",
        session_id="scenario_1",
        message=genai.types.Content(parts=[genai.types.Part(text=scenario_1)]),
    )

    # Add delay between scenarios to avoid rate limits
    print("\n⏳ Waiting 2 seconds before next scenario...\n")
    await asyncio.sleep(2)

    # Demo Scenario 2: Activity Planning
    print_separator("📋 SCENARIO 2: Bedtime Routine Planning")
    print("Parent Question:")
    scenario_2 = """I need help creating a structured bedtime routine.
My son has trouble with the transition from play time to bedtime.
We have about 30 minutes, and I have a visual timer, some fidget toys, and his favorite books.
In the past, visual timers have worked well for him."""

    print(f'"{scenario_2}"\n')
    print("🤖 Coordinator orchestrating specialists...\n")

    # Create session for scenario 2
    await session_service.create_session(
        app_name="agents",
        user_id="demo_user",
        session_id="scenario_2",
    )

    # Run scenario with automatic retry
    await run_scenario_with_retry(
        runner=runner,
        user_id="demo_user",
        session_id="scenario_2",
        message=genai.types.Content(parts=[genai.types.Part(text=scenario_2)]),
    )

    # Add delay between scenarios to avoid rate limits
    print("\n⏳ Waiting 2 seconds before next scenario...\n")
    await asyncio.sleep(2)

    # Demo Scenario 3: Pattern Learning
    print_separator("📋 SCENARIO 3: Learning from Past Experiences")
    print("Parent Question:")
    scenario_3 = """Can you analyze what's been working for bedtime? Here's our history:

Session 1: Used visual timer (10 min), worked well, he went to bed without resistance
Session 2: Just verbal reminders, didn't work, he got upset and it took 45 minutes
Session 3: Visual timer + sensory break before bed, worked great, he was calm

What patterns do you see?"""

    print(f'"{scenario_3}"\n')
    print("🤖 Coordinator orchestrating specialists...\n")

    # Create session for scenario 3
    await session_service.create_session(
        app_name="agents",
        user_id="demo_user",
        session_id="scenario_3",
    )

    # Run scenario with automatic retry
    await run_scenario_with_retry(
        runner=runner,
        user_id="demo_user",
        session_id="scenario_3",
        message=genai.types.Content(parts=[genai.types.Part(text=scenario_3)]),
    )

    print_separator("✨ Demo Complete")
    print("This demo showcased:")
    print("  ✅ Multi-agent hierarchical orchestration (Day 1)")
    print("  ✅ Custom tools integration (Day 2)")
    print("  ✅ Google Search tool usage (Day 2)")
    print("  ✅ Pattern learning from session history (Day 3)")
    print("  ✅ Type-safe Pydantic models throughout")
    print("\nReady for Kaggle Agents Intensive Capstone submission! 🎉")


if __name__ == "__main__":
    asyncio.run(main())
