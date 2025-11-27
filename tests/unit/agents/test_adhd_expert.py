"""Tests for ADHD expert agent."""

from unittest.mock import Mock, patch

from google.adk.agents import LlmAgent
from google.genai.types import GenerateContentConfig

from capstone.agents.specialist_factory import create_adhd_expert


class TestCreateADHDExpert:
    """Tests for create_adhd_expert function."""

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

        agent = create_adhd_expert()

        assert agent == mock_agent
        mock_llm_agent.assert_called_once()

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_uses_correct_model(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test agent uses gemini-2.0-flash-exp model."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_adhd_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        assert call_kwargs["model"] == "gemini-2.0-flash-exp"

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_has_correct_name(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test agent has correct name."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_adhd_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        assert call_kwargs["name"] == "adhd_expert"

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_has_correct_description(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test agent has descriptive text."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_adhd_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        description = call_kwargs["description"]
        assert "ADHD" in description
        assert "executive function" in description
        assert "8-year-old" in description

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_system_prompt_contains_adhd_keywords(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt includes ADHD-specific content."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_adhd_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"].lower()

        # ADHD-specific keywords
        assert "adhd" in instruction
        assert "executive function" in instruction
        assert "attention" in instruction
        assert "impulse" in instruction or "impulsivity" in instruction
        assert "hyperactivity" in instruction

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_system_prompt_references_evidence_sources(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt references ADHD evidence sources."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_adhd_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]

        # Evidence-based sources
        assert "CHADD" in instruction or "chadd" in instruction.lower()
        assert "Russell Barkley" in instruction or "barkley" in instruction.lower()

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_tools_includes_google_search(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test tools parameter includes google_search for web research."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_adhd_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        tools = call_kwargs["tools"]
        assert len(tools) == 1
        # google_search is the ADK's pre-instantiated GoogleSearchTool
        assert tools[0].__class__.__name__ == "GoogleSearchTool"

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_uses_retry_configuration(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test agent uses retry config from get_retry_config()."""
        mock_config = Mock(spec=GenerateContentConfig)
        mock_retry_config.return_value = mock_config

        create_adhd_expert()

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

        create_adhd_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]

        # Response format guidelines
        assert "Response Format" in instruction or "response format" in instruction.lower()
        assert "strategies" in instruction.lower()

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_system_prompt_includes_guidelines(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt includes important guidelines."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_adhd_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]

        # Important guidelines
        assert "support tool" in instruction.lower()
        assert "not a medical professional" in instruction.lower()
