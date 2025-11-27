"""Tests for ASD expert agent."""

from unittest.mock import Mock, patch

from google.adk.agents import LlmAgent
from google.genai.types import GenerateContentConfig

from capstone.agents.specialist_factory import create_asd_expert


class TestCreateASDExpert:
    """Tests for create_asd_expert function."""

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

        agent = create_asd_expert()

        assert agent == mock_agent
        mock_llm_agent.assert_called_once()

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_uses_correct_model(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test agent uses gemini-2.0-flash-exp model."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_asd_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        assert call_kwargs["model"] == "gemini-2.0-flash-exp"

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_has_correct_name(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test agent has correct name."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_asd_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        assert call_kwargs["name"] == "asd_expert"

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_has_correct_description(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test agent has descriptive text."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_asd_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        description = call_kwargs["description"]
        assert "autism" in description.lower() or "ASD" in description
        assert "sensory" in description.lower()
        assert "Level 1" in description

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_system_prompt_contains_asd_keywords(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt includes ASD-specific content."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_asd_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"].lower()

        # ASD-specific keywords
        assert "asd" in instruction or "autism" in instruction
        assert "sensory" in instruction
        assert "routine" in instruction or "predictability" in instruction
        assert "communication" in instruction

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_system_prompt_references_evidence_sources(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt references autism evidence sources."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_asd_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]

        # Evidence-based sources
        assert "Temple Grandin" in instruction or "grandin" in instruction.lower()
        assert "CDC" in instruction or "cdc" in instruction.lower()

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_tools_includes_google_search(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test tools parameter includes google_search for web research."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_asd_expert()

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

        create_asd_expert()

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

        create_asd_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]

        # Response format guidelines
        assert "Response Format" in instruction or "response format" in instruction.lower()
        assert "strategies" in instruction.lower()

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_system_prompt_includes_neurodiversity_affirmation(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt includes neurodiversity-affirming language."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_asd_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]

        # Neurodiversity-affirming approach
        assert "neurodiversity" in instruction.lower() or "affirming" in instruction.lower()
        assert "support tool" in instruction.lower()
        assert "not a medical professional" in instruction.lower()
