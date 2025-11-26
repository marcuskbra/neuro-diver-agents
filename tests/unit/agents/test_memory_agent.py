"""Tests for memory agent."""

from unittest.mock import Mock, patch

from google.adk.agents import LlmAgent
from google.genai.types import GenerateContentConfig

from capstone.agents.specialist_factory import create_memory_agent


class TestCreateMemoryAgent:
    """Tests for create_memory_agent function."""

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

        agent = create_memory_agent()

        assert agent == mock_agent
        mock_llm_agent.assert_called_once()

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_uses_correct_model(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test agent uses gemini-2.0-flash-exp model."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_memory_agent()

        call_kwargs = mock_llm_agent.call_args[1]
        assert call_kwargs["model"] == "gemini-2.0-flash-exp"

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_has_correct_name(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test agent has correct name."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_memory_agent()

        call_kwargs = mock_llm_agent.call_args[1]
        assert call_kwargs["name"] == "memory_agent"

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_has_correct_description(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test agent has descriptive text."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_memory_agent()

        call_kwargs = mock_llm_agent.call_args[1]
        description = call_kwargs["description"]
        assert "pattern" in description.lower()
        assert "learning" in description.lower() or "memory" in description.lower()
        assert "history" in description.lower() or "session" in description.lower()

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_system_prompt_contains_memory_keywords(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt includes memory-specific content."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_memory_agent()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"].lower()

        # Memory-specific keywords
        assert "memory" in instruction or "pattern" in instruction
        assert "history" in instruction or "session" in instruction
        assert "learning" in instruction
        assert "personalized" in instruction or "personalization" in instruction

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_system_prompt_describes_pattern_analysis(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt includes pattern analysis approach."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_memory_agent()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]

        # Pattern analysis approach
        assert "pattern" in instruction.lower()
        assert "strategies" in instruction.lower()
        assert "successful" in instruction.lower() or "success" in instruction.lower()

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_system_prompt_includes_session_history_format(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt specifies session history format."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_memory_agent()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]

        # Session history format
        assert "Session History Format" in instruction or "session history" in instruction.lower()
        assert "JSON" in instruction or "json" in instruction.lower()

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_tools_set_to_empty_list(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test tools parameter is empty list (orchestration-only)."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_memory_agent()

        call_kwargs = mock_llm_agent.call_args[1]
        assert call_kwargs["tools"] == []

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_uses_retry_configuration(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test agent uses retry config from get_retry_config()."""
        mock_config = Mock(spec=GenerateContentConfig)
        mock_retry_config.return_value = mock_config

        create_memory_agent()

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

        create_memory_agent()

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

        create_memory_agent()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]

        # Important guidelines
        assert "support tool" in instruction.lower()
        assert "not a medical professional" in instruction.lower()
