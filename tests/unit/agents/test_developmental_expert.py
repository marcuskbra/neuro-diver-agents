"""Tests for developmental expert agent."""

from unittest.mock import Mock, patch

from google.adk.agents import LlmAgent
from google.genai.types import GenerateContentConfig

from capstone.agents.specialist_factory import create_developmental_expert


class TestCreateDevelopmentalExpert:
    """Tests for create_developmental_expert function."""

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

        agent = create_developmental_expert()

        assert agent == mock_agent
        mock_llm_agent.assert_called_once()

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_uses_correct_model(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test agent uses gemini-2.0-flash-exp model."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_developmental_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        assert call_kwargs["model"] == "gemini-2.0-flash-exp"

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_has_correct_name(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test agent has correct name."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_developmental_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        assert call_kwargs["name"] == "developmental_expert"

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_has_correct_description(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test agent has descriptive text."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_developmental_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        description = call_kwargs["description"]
        assert "developmental" in description.lower()
        assert "age-appropriate" in description.lower()
        assert "8-year-old" in description

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_system_prompt_contains_developmental_keywords(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt includes developmental-specific content."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_developmental_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"].lower()

        # Developmental-specific keywords
        assert "developmental" in instruction
        assert "age-appropriate" in instruction or "age appropriate" in instruction
        assert "milestones" in instruction
        assert "8-year-old" in instruction

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_system_prompt_references_evidence_sources(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt references developmental evidence sources."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_developmental_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]

        # Evidence-based sources
        assert "CDC" in instruction or "cdc" in instruction.lower()
        assert (
            "American Academy of Pediatrics" in instruction
            or "AAP" in instruction
            or "pediatrics" in instruction.lower()
        )

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_system_prompt_mentions_developmental_domains(
        self, mock_llm_agent: Mock, mock_retry_config: Mock
    ) -> None:
        """Test system prompt covers multiple developmental domains."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_developmental_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"].lower()

        # Developmental domains
        assert "cognitive" in instruction
        assert "social" in instruction
        assert "emotional" in instruction

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_tools_set_to_empty_list(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test tools parameter is empty list (orchestration-only)."""
        mock_retry_config.return_value = Mock(spec=GenerateContentConfig)

        create_developmental_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        assert call_kwargs["tools"] == []

    @patch("capstone.agents.specialist_factory.get_retry_config")
    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_uses_retry_configuration(self, mock_llm_agent: Mock, mock_retry_config: Mock) -> None:
        """Test agent uses retry config from get_retry_config()."""
        mock_config = Mock(spec=GenerateContentConfig)
        mock_retry_config.return_value = mock_config

        create_developmental_expert()

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

        create_developmental_expert()

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

        create_developmental_expert()

        call_kwargs = mock_llm_agent.call_args[1]
        instruction = call_kwargs["instruction"]

        # Important guidelines
        assert "support tool" in instruction.lower()
        assert "not a medical professional" in instruction.lower()
