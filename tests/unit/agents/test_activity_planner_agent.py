"""Tests for activity planner agent."""

from unittest.mock import Mock, patch

from google.adk.agents import LlmAgent
from google.genai.types import GenerateContentConfig

from capstone.agents.specialist_factory import create_activity_planner_agent


class TestCreateActivityPlannerAgent:
    """Tests for create_activity_planner_agent function."""

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_creates_llm_agent_instance(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test creates LlmAgent with correct configuration."""
        mock_agent = Mock(spec=LlmAgent)
        mock_llm_agent.return_value = mock_agent
        mock_config = Mock(spec=GenerateContentConfig)
        mock_retry_config.return_value = mock_config

        agent = create_activity_planner_agent()

        assert agent == mock_agent
        mock_llm_agent.assert_called_once()

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_uses_correct_model(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test agent uses gemini-2.0-flash-exp model."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_activity_planner_agent()

        call_kwargs = mock_llm_agent.call_args[1]
        assert call_kwargs["model"] == "gemini-2.0-flash-exp"

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_has_correct_name(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test agent has correct name."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_activity_planner_agent()

        call_kwargs = mock_llm_agent.call_args[1]
        assert call_kwargs["name"] == "activity_planner"

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_has_correct_description(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test agent has descriptive text."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_activity_planner_agent()

        call_kwargs = mock_llm_agent.call_args[1]
        description = call_kwargs["description"]
        assert "activity" in description.lower()
        assert "structured" in description.lower()
        assert "materials" in description.lower() or "setup" in description.lower()

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_system_prompt_contains_activity_keywords(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt includes activity planning content."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_activity_planner_agent()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"].lower()

        # Activity planning keywords
        assert "activity" in instruction
        assert "structured" in instruction
        assert "materials" in instruction
        assert "setup" in instruction or "environmental" in instruction

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_system_prompt_includes_activity_goals(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt describes activity goals."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_activity_planner_agent()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]

        # Activity goals
        assert "Activity Goals" in instruction or "activity goals" in instruction.lower()
        assert "Executive Function" in instruction or "executive function" in instruction.lower()
        assert "homework" in instruction.lower()

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_system_prompt_mentions_adhd_asd_adaptations(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt includes ADHD/ASD adaptations."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_activity_planner_agent()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"].lower()

        # ADHD/ASD adaptations
        assert "adhd" in instruction
        assert "asd" in instruction or "autism" in instruction
        assert "sensory" in instruction

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_system_prompt_specifies_timing_range(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt includes activity timing range."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_activity_planner_agent()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]

        # Timing range
        assert "5-120 minutes" in instruction or "timeframe" in instruction.lower()

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_tools_set_to_empty_list(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test tools parameter is empty list (orchestration-only)."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_activity_planner_agent()

        call_kwargs = mock_llm_agent.call_args[1]
        assert call_kwargs["tools"] == []

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_uses_retry_configuration(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test agent uses retry config from get_retry_config()."""
        mock_config = Mock(spec=GenerateContentConfig)
        mock_retry_config.return_value = mock_config

        create_activity_planner_agent()

        call_kwargs = mock_llm_agent.call_args[1]
        assert call_kwargs["generate_content_config"] == mock_config
        mock_retry_config.assert_called_once()

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_system_prompt_includes_response_format(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt includes structured response format."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_activity_planner_agent()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]

        # Response format guidelines
        assert "Response Format" in instruction or "response format" in instruction.lower()

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_system_prompt_includes_guidelines(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt includes important guidelines."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_activity_planner_agent()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]

        # Important guidelines
        assert "support tool" in instruction.lower()
        assert "not a medical professional" in instruction.lower()
