"""Unit tests for specialist agent consultation helpers."""

from unittest.mock import MagicMock, patch

from google.adk.agents import LlmAgent

from capstone.agents.specialist_helpers import consult_specialist


class TestConsultSpecialist:
    """Test the consult_specialist helper function."""

    def test_consult_specialist_returns_response_text(self):
        """Test consult_specialist returns response text on success."""
        # Create a mock agent
        mock_agent = MagicMock(spec=LlmAgent)
        mock_agent.model = "gemini-2.0-flash"
        mock_agent.instruction = "You are a test expert."

        # Create agent getter
        def agent_getter() -> LlmAgent:
            return mock_agent

        # Mock the genai.Client and its response
        mock_response = MagicMock()
        mock_response.text = "This is the specialist response."

        with patch("capstone.agents.specialist_helpers.genai.Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client.models.generate_content.return_value = mock_response
            mock_client_class.return_value = mock_client

            result = consult_specialist(
                agent_getter=agent_getter,
                question="What is ADHD?",
                specialist_name="ADHD Expert",
            )

            assert result == "This is the specialist response."
            mock_client.models.generate_content.assert_called_once()

    def test_consult_specialist_returns_message_on_empty_response(self):
        """Test consult_specialist returns message when response.text is empty."""
        mock_agent = MagicMock(spec=LlmAgent)
        mock_agent.model = "gemini-2.0-flash"
        mock_agent.instruction = "You are a test expert."

        def agent_getter() -> LlmAgent:
            return mock_agent

        # Mock response with empty text
        mock_response = MagicMock()
        mock_response.text = ""

        with patch("capstone.agents.specialist_helpers.genai.Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client.models.generate_content.return_value = mock_response
            mock_client_class.return_value = mock_client

            result = consult_specialist(
                agent_getter=agent_getter,
                question="What is ADHD?",
                specialist_name="ADHD Expert",
            )

            assert result == "No response from ADHD Expert"

    def test_consult_specialist_returns_message_on_none_response(self):
        """Test consult_specialist returns message when response.text is None."""
        mock_agent = MagicMock(spec=LlmAgent)
        mock_agent.model = "gemini-2.0-flash"
        mock_agent.instruction = "You are a test expert."

        def agent_getter() -> LlmAgent:
            return mock_agent

        # Mock response with None text
        mock_response = MagicMock()
        mock_response.text = None

        with patch("capstone.agents.specialist_helpers.genai.Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client.models.generate_content.return_value = mock_response
            mock_client_class.return_value = mock_client

            result = consult_specialist(
                agent_getter=agent_getter,
                question="What is ADHD?",
                specialist_name="ADHD Expert",
            )

            assert result == "No response from ADHD Expert"

    def test_consult_specialist_handles_api_exception(self):
        """Test consult_specialist handles API exceptions gracefully."""
        mock_agent = MagicMock(spec=LlmAgent)
        mock_agent.model = "gemini-2.0-flash"
        mock_agent.instruction = "You are a test expert."

        def agent_getter() -> LlmAgent:
            return mock_agent

        with patch("capstone.agents.specialist_helpers.genai.Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client.models.generate_content.side_effect = Exception("API connection failed")
            mock_client_class.return_value = mock_client

            result = consult_specialist(
                agent_getter=agent_getter,
                question="What is ADHD?",
                specialist_name="ADHD Expert",
            )

            assert "Error consulting ADHD Expert" in result
            assert "API connection failed" in result

    def test_consult_specialist_handles_agent_getter_exception(self):
        """Test consult_specialist handles exception in agent_getter."""

        def failing_agent_getter() -> LlmAgent:
            raise RuntimeError("Failed to create agent")

        result = consult_specialist(
            agent_getter=failing_agent_getter,
            question="What is ADHD?",
            specialist_name="ADHD Expert",
        )

        assert "Error consulting ADHD Expert" in result
        assert "Failed to create agent" in result

    def test_consult_specialist_uses_correct_model_and_instruction(self):
        """Test consult_specialist passes correct model and instruction to API."""
        mock_agent = MagicMock(spec=LlmAgent)
        mock_agent.model = "gemini-pro"
        mock_agent.instruction = "You are an ASD specialist."

        def agent_getter() -> LlmAgent:
            return mock_agent

        mock_response = MagicMock()
        mock_response.text = "Response text"

        with patch("capstone.agents.specialist_helpers.genai.Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client.models.generate_content.return_value = mock_response
            mock_client_class.return_value = mock_client

            consult_specialist(
                agent_getter=agent_getter,
                question="What is autism?",
                specialist_name="ASD Expert",
            )

            # Verify the call was made with correct parameters
            call_kwargs = mock_client.models.generate_content.call_args
            assert call_kwargs.kwargs["model"] == "gemini-pro"
            assert call_kwargs.kwargs["contents"] == "What is autism?"

    def test_consult_specialist_with_different_specialist_names(self):
        """Test consult_specialist uses correct specialist name in error messages."""

        def failing_agent_getter() -> LlmAgent:
            raise RuntimeError("Connection error")

        # Test with different specialist names
        result1 = consult_specialist(
            agent_getter=failing_agent_getter,
            question="Question",
            specialist_name="Memory Agent",
        )
        assert "Error consulting Memory Agent" in result1

        result2 = consult_specialist(
            agent_getter=failing_agent_getter,
            question="Question",
            specialist_name="Activity Planner",
        )
        assert "Error consulting Activity Planner" in result2
