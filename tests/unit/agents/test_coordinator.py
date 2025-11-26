"""Comprehensive tests for parenting coordinator agent."""

import json
from unittest.mock import Mock, patch

from google.adk.agents import LlmAgent
from google.genai.types import GenerateContentConfig

from capstone.agents.coordinator import create_coordinator
from capstone.agents.tool_formatters import (
    format_activity_plan,
    format_behavior_analysis,
    format_pattern_analysis,
)
from capstone.agents.tool_wrappers import (
    create_analyze_behavior_wrapper,
    create_analyze_patterns_wrapper,
    create_plan_activity_wrapper,
)
from capstone.infrastructure.agent_factory import AgentFactory
from capstone.models import (
    ActivityGoal,
    ActivityType,
    BehaviorFactor,
    TimeOfDay,
    ToolError,
    ToolSuccess,
)


class TestCoordinatorCreation:
    """Tests for create_coordinator function."""

    @patch("capstone.agents.coordinator.get_retry_config")
    @patch("capstone.agents.coordinator.LlmAgent")
    def test_creates_llm_agent_instance(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test creates LlmAgent with correct configuration."""
        mock_agent = Mock(spec=LlmAgent)
        mock_llm_agent.return_value = mock_agent
        mock_config = Mock(spec=GenerateContentConfig)
        mock_retry_config.return_value = mock_config

        agent = create_coordinator()

        assert agent == mock_agent
        mock_llm_agent.assert_called_once()

    @patch("capstone.agents.coordinator.get_retry_config")
    @patch("capstone.agents.coordinator.LlmAgent")
    def test_uses_correct_model(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test coordinator uses gemini-2.0-flash-exp model."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_coordinator()

        call_kwargs = mock_llm_agent.call_args[1]
        assert call_kwargs["model"] == "gemini-2.0-flash-exp"

    @patch("capstone.agents.coordinator.get_retry_config")
    @patch("capstone.agents.coordinator.LlmAgent")
    def test_has_correct_name(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test coordinator has correct name."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_coordinator()

        call_kwargs = mock_llm_agent.call_args[1]
        assert call_kwargs["name"] == "parenting_coordinator"

    @patch("capstone.agents.coordinator.get_retry_config")
    @patch("capstone.agents.coordinator.LlmAgent")
    def test_has_descriptive_description(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test coordinator has descriptive text."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_coordinator()

        call_kwargs = mock_llm_agent.call_args[1]
        description = call_kwargs["description"]
        assert "specialist" in description.lower()
        assert "parenting" in description.lower()

    @patch("capstone.agents.coordinator.get_retry_config")
    @patch("capstone.agents.coordinator.LlmAgent")
    def test_system_prompt_describes_coordinator_role(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt explains coordinator's orchestration role."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_coordinator()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]
        assert "Parenting Coordinator" in instruction
        assert "orchestrate" in instruction.lower()

    @patch("capstone.agents.coordinator.get_retry_config")
    @patch("capstone.agents.coordinator.LlmAgent")
    def test_system_prompt_lists_five_specialists(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt describes all 5 specialist agents."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_coordinator()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]

        # All 5 specialists mentioned
        assert "ADHD Expert" in instruction
        assert "ASD Expert" in instruction
        assert "Developmental Expert" in instruction
        assert "Memory Agent" in instruction
        assert "Activity Planner" in instruction

    @patch("capstone.agents.coordinator.get_retry_config")
    @patch("capstone.agents.coordinator.LlmAgent")
    def test_system_prompt_includes_coordination_guidelines(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt includes how to coordinate specialists."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_coordinator()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]

        # Coordination guidelines present
        assert "How to Use Your Team" in instruction or "coordination" in instruction.lower()

    @patch("capstone.agents.coordinator.get_retry_config")
    @patch("capstone.agents.coordinator.LlmAgent")
    def test_tools_include_eight_functions(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test coordinator has all 8 tools (5 specialists + 3 tool wrappers)."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_coordinator()

        call_kwargs = mock_llm_agent.call_args[1]
        tools = call_kwargs["tools"]

        # Should have 8 tools: 5 specialists + 3 tool wrappers
        assert len(tools) == 8

    @patch("capstone.agents.coordinator.get_retry_config")
    @patch("capstone.agents.coordinator.LlmAgent")
    def test_uses_retry_configuration(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test coordinator uses retry config for 429 errors."""
        mock_config = Mock(spec=GenerateContentConfig)
        mock_retry_config.return_value = mock_config

        create_coordinator()

        call_kwargs = mock_llm_agent.call_args[1]
        assert call_kwargs["generate_content_config"] == mock_config
        mock_retry_config.assert_called_once()

    @patch("capstone.agents.coordinator.get_retry_config")
    @patch("capstone.agents.coordinator.LlmAgent")
    def test_system_prompt_includes_disclaimer(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt includes medical disclaimer."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_coordinator()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]
        assert "support tool" in instruction.lower()
        assert "not medical" in instruction.lower() or "not a medical" in instruction.lower()

    @patch("capstone.agents.coordinator.get_retry_config")
    @patch("capstone.agents.coordinator.LlmAgent")
    def test_system_prompt_includes_response_structure(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt defines response structure."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_coordinator()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]
        assert "Response Structure" in instruction or "response format" in instruction.lower()

    @patch("capstone.agents.coordinator.get_retry_config")
    @patch("capstone.agents.coordinator.LlmAgent")
    def test_system_prompt_includes_example_routing_logic(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt provides routing examples."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_coordinator()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]
        assert "Example Routing" in instruction or "routing logic" in instruction.lower()

    @patch("capstone.agents.coordinator.get_retry_config")
    @patch("capstone.agents.coordinator.LlmAgent")
    def test_accepts_custom_agent_factory(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test coordinator accepts custom AgentFactory via dependency injection."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)
        custom_factory = AgentFactory()

        # Should not raise
        create_coordinator(agent_factory=custom_factory)

        mock_llm_agent.assert_called_once()


class TestToolFormatters:
    """Tests for tool output formatters."""

    class TestFormatBehaviorAnalysis:
        """Tests for format_behavior_analysis."""

        def test_with_all_factor_types_includes_all(self) -> None:
            """Test formatter includes all factor types when present."""
            data = {
                "primary_driver": BehaviorFactor.COMBINED.value,
                "adhd_factors": ["Executive function"],
                "asd_factors": ["Sensory overload"],
                "age_typical_factors": ["Tired after school"],
            }

            result = format_behavior_analysis(data)

            assert "Primary driver: combined" in result
            assert "ADHD: Executive function" in result
            assert "ASD: Sensory overload" in result
            assert "Age-typical: Tired after school" in result

        def test_with_empty_factors_excludes_sections(self) -> None:
            """Test formatter excludes empty factor sections."""
            data = {
                "primary_driver": BehaviorFactor.AGE_TYPICAL.value,
                "adhd_factors": [],
                "asd_factors": [],
                "age_typical_factors": ["Normal 8-year-old behavior"],
            }

            result = format_behavior_analysis(data)

            # Should not include empty ADHD/ASD sections
            assert "ADHD:" not in result
            assert "ASD:" not in result
            assert "Age-typical: Normal 8-year-old behavior" in result

    class TestFormatActivityPlan:
        """Tests for format_activity_plan."""

        def test_with_complete_plan_includes_all_fields(self) -> None:
            """Test formatter includes all activity plan fields."""
            data = {
                "name": "Calming Break",
                "goal": ActivityGoal.ENGAGEMENT.value,
                "duration_minutes": 15,
                "materials": ["fidget toys", "soft music"],
                "environmental_setup": "Quiet corner",
                "structure": ["Step 1", "Step 2"],
                "success_criteria": ["Child appears calm"],
                "adaptations": ["Adjust lighting"],
            }

            result = format_activity_plan(data)

            assert "Activity: Calming Break" in result
            assert "Duration: 15 minutes" in result
            assert "Materials needed: fidget toys, soft music" in result
            assert "Environmental setup: Quiet corner" in result
            assert "Step 1" in result
            assert "Child appears calm" in result
            assert "Adjust lighting" in result

    class TestFormatPatternAnalysis:
        """Tests for format_pattern_analysis."""

        def test_with_complete_analysis_includes_all_fields(self) -> None:
            """Test formatter includes all pattern analysis fields."""
            data = {
                "behavior_type": "bedtime_resistance",
                "sessions": 5,
                "frequency": 3,
                "common_triggers": ["overtired"],
                "successful_strategies": ["visual timer"],
                "unsuccessful_approaches": ["verbal warnings"],
            }

            result = format_pattern_analysis(data)

            assert "Behavior: bedtime_resistance" in result
            assert "Sessions analyzed: 5" in result
            assert "Success rate: 3/5" in result
            assert "Common triggers: overtired" in result
            assert "Successful strategies: visual timer" in result
            assert "Unsuccessful approaches: verbal warnings" in result

        def test_with_empty_fields_excludes_sections(self) -> None:
            """Test formatter excludes sections for empty fields."""
            data = {
                "behavior_type": "test",
                "sessions": 2,
                "frequency": 1,
                "common_triggers": [],
                "successful_strategies": [],
                "unsuccessful_approaches": [],
            }

            result = format_pattern_analysis(data)

            assert "Common triggers:" not in result
            assert "Successful strategies:" not in result
            assert "Unsuccessful approaches:" not in result


class TestToolWrappers:
    """Tests for tool wrapper factory functions."""

    class TestAnalyzeBehaviorWrapper:
        """Tests for analyze behavior wrapper."""

        @patch("capstone.agents.tool_wrappers.classify_behavior")
        def test_with_valid_input_returns_formatted_analysis(self, mock_classify: Mock) -> None:
            """Test behavior wrapper formats successful analysis correctly."""
            mock_classify.return_value = ToolSuccess(
                data={
                    "primary_driver": BehaviorFactor.ADHD.value,
                    "adhd_factors": ["Attention difficulty", "Impulsivity"],
                    "asd_factors": [],
                    "age_typical_factors": ["Homework resistance"],
                }
            )

            wrapper = create_analyze_behavior_wrapper()
            result = wrapper(
                description="Cannot focus on homework",
                time_of_day=TimeOfDay.AFTERNOON,
                activity_type=ActivityType.HOMEWORK,
                context="After school",
            )

            assert "Primary driver: adhd" in result
            assert "ADHD: Attention difficulty, Impulsivity" in result
            assert "Age-typical: Homework resistance" in result

        @patch("capstone.agents.tool_wrappers.classify_behavior")
        def test_with_tool_error_returns_error_message(self, mock_classify: Mock) -> None:
            """Test behavior wrapper handles tool errors gracefully."""
            mock_classify.return_value = ToolError(
                error_code="CLASSIFICATION_FAILED",
                error_message="Failed to classify behavior",
            )

            wrapper = create_analyze_behavior_wrapper()
            result = wrapper(
                description="Test behavior",
                time_of_day=TimeOfDay.MORNING,
                activity_type=ActivityType.TRANSITIONS,
                context="Test context",
            )

            assert "Error analyzing behavior" in result
            assert "Failed to classify behavior" in result

    class TestPlanActivityWrapper:
        """Tests for plan activity wrapper."""

        @patch("capstone.agents.tool_wrappers.get_activity_plan")
        def test_with_valid_input_returns_formatted_plan(self, mock_plan: Mock) -> None:
            """Test activity wrapper formats successful plan correctly."""
            mock_plan.return_value = ToolSuccess(
                data={
                    "name": "Engagement Activity",
                    "goal": ActivityGoal.ENGAGEMENT.value,
                    "duration_minutes": 15,
                    "materials": ["fidget toys", "soft music"],
                    "environmental_setup": "Quiet, dimly lit corner",
                    "structure": ["5 min deep breathing"],
                    "success_criteria": ["Child appears calmer"],
                    "adaptations": ["Adjust lighting"],
                }
            )

            wrapper = create_plan_activity_wrapper()
            result = wrapper(
                goal=ActivityGoal.ENGAGEMENT.value,
                duration_minutes=15,
                materials="fidget toys, soft music",
            )

            assert "Activity: Engagement Activity" in result
            assert "Duration: 15 minutes" in result

        @patch("capstone.agents.tool_wrappers.get_activity_plan")
        def test_with_tool_error_returns_error_message(self, mock_plan: Mock) -> None:
            """Test activity wrapper handles tool errors gracefully."""
            mock_plan.return_value = ToolError(
                error_code="INVALID_GOAL",
                error_message="Invalid activity goal",
            )

            wrapper = create_plan_activity_wrapper()
            result = wrapper(
                goal=ActivityGoal.ENGAGEMENT.value,
                duration_minutes=30,
                materials="timer, books",
            )

            assert "Error planning activity" in result
            assert "Invalid activity goal" in result

        def test_with_invalid_goal_enum_returns_error(self) -> None:
            """Test activity wrapper returns error for invalid goal enum."""
            wrapper = create_plan_activity_wrapper()
            result = wrapper(
                goal="invalid_goal",
                duration_minutes=10,
                materials="test",
            )

            assert "Error:" in result

    class TestAnalyzePatternsWrapper:
        """Tests for analyze patterns wrapper."""

        @patch("capstone.agents.tool_wrappers.analyze_patterns")
        def test_with_valid_json_returns_formatted_analysis(self, mock_analyze: Mock) -> None:
            """Test patterns wrapper formats successful analysis correctly."""
            mock_analyze.return_value = ToolSuccess(
                data={
                    "behavior_type": "bedtime_resistance",
                    "sessions": 5,
                    "frequency": 3,
                    "common_triggers": ["overtired", "screen time"],
                    "successful_strategies": ["visual timer"],
                    "unsuccessful_approaches": ["verbal warnings"],
                }
            )

            session_json = json.dumps(
                [
                    {"strategy_used": "visual timer", "worked": True, "notes": "Smooth"},
                    {"strategy_used": "verbal warnings", "worked": False, "notes": "Meltdown"},
                ]
            )

            wrapper = create_analyze_patterns_wrapper()
            result = wrapper(
                session_history_json=session_json,
                behavior_type="bedtime_resistance",
            )

            assert "Behavior: bedtime_resistance" in result
            assert "Sessions analyzed: 5" in result

        def test_with_invalid_json_returns_parse_error(self) -> None:
            """Test patterns wrapper handles JSON parsing errors."""
            wrapper = create_analyze_patterns_wrapper()
            result = wrapper(
                session_history_json="not valid json",
                behavior_type="test_behavior",
            )

            assert "Error parsing session history JSON" in result

        @patch("capstone.agents.tool_wrappers.analyze_patterns")
        def test_with_tool_error_returns_error_message(self, mock_analyze: Mock) -> None:
            """Test patterns wrapper handles tool errors gracefully."""
            mock_analyze.return_value = ToolError(
                error_code="INSUFFICIENT_DATA",
                error_message="Insufficient session data",
            )

            session_json = json.dumps(
                [{"strategy_used": "timer", "worked": True, "notes": "Worked"}]
            )

            wrapper = create_analyze_patterns_wrapper()
            result = wrapper(
                session_history_json=session_json,
                behavior_type="test_behavior",
            )

            assert "Error analyzing patterns" in result
            assert "Insufficient session data" in result
