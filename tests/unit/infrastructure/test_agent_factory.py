"""Tests for AgentFactory infrastructure."""

from collections.abc import Callable
from unittest.mock import Mock, patch

from google.adk.agents import LlmAgent

from capstone.agents.agent_configs import AGENT_CONFIGS, AgentConfig
from capstone.agents.specialist_factory import create_specialist_agent
from capstone.infrastructure.agent_factory import AgentFactory


class TestAgentFactory:
    """Tests for AgentFactory class."""

    def test_initialization_creates_empty_cache(self) -> None:
        """Test factory initializes with empty cache."""
        factory = AgentFactory()

        assert factory._cache == {}
        assert isinstance(factory._cache, dict)
        assert len(factory._cache) == 0

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_get_adhd_expert_first_call_creates_and_caches_agent(self, mock_llm: Mock) -> None:
        """Test first call creates and caches ADHD expert."""
        mock_agent = Mock(spec=LlmAgent)
        mock_llm.return_value = mock_agent
        factory = AgentFactory()

        # Verify cache is empty
        assert len(factory._cache) == 0

        # Get agent
        agent = factory.get_adhd_expert()

        # Verify agent created
        assert agent is not None
        assert agent is mock_agent

        # Verify cached
        assert "adhd_expert" in factory._cache
        assert len(factory._cache) == 1
        assert factory._cache["adhd_expert"] is mock_agent

        # Verify LlmAgent was created with correct config from AGENT_CONFIGS
        mock_llm.assert_called_once()
        call_kwargs = mock_llm.call_args[1]
        assert call_kwargs["name"] == "adhd_expert"
        assert "ADHD" in call_kwargs["description"]
        assert "ADHD specialist" in call_kwargs["instruction"]

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_get_adhd_expert_second_call_returns_cached_instance(self, mock_llm: Mock) -> None:
        """Test second call returns same cached instance."""
        mock_agent = Mock(spec=LlmAgent)
        mock_llm.return_value = mock_agent
        factory = AgentFactory()

        # First call
        agent1 = factory.get_adhd_expert()

        # Second call
        agent2 = factory.get_adhd_expert()

        # Verify same instance
        assert agent1 is agent2
        assert id(agent1) == id(agent2)

        # Verify cache only has one entry
        assert len(factory._cache) == 1

        # Verify LlmAgent was only created once
        assert mock_llm.call_count == 1

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_get_asd_expert_first_call_creates_and_caches_agent(self, mock_llm: Mock) -> None:
        """Test first call creates and caches ASD expert."""
        mock_agent = Mock(spec=LlmAgent)
        mock_llm.return_value = mock_agent
        factory = AgentFactory()

        # Get agent
        agent = factory.get_asd_expert()

        # Verify agent created and cached
        assert agent is mock_agent
        assert "asd_expert" in factory._cache
        assert len(factory._cache) == 1

        # Verify LlmAgent was created with correct config
        call_kwargs = mock_llm.call_args[1]
        assert call_kwargs["name"] == "asd_expert"
        assert "autism" in call_kwargs["description"].lower() or "ASD" in call_kwargs["description"]
        assert "ASD" in call_kwargs["instruction"] or "autism" in call_kwargs["instruction"].lower()

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_get_asd_expert_second_call_returns_cached_instance(self, mock_llm: Mock) -> None:
        """Test second call returns same cached ASD expert."""
        mock_agent = Mock(spec=LlmAgent)
        mock_llm.return_value = mock_agent
        factory = AgentFactory()

        agent1 = factory.get_asd_expert()
        agent2 = factory.get_asd_expert()

        assert agent1 is agent2
        assert mock_llm.call_count == 1

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_get_developmental_expert_first_call_creates_and_caches_agent(
        self, mock_llm: Mock
    ) -> None:
        """Test first call creates and caches developmental expert."""
        mock_agent = Mock(spec=LlmAgent)
        mock_llm.return_value = mock_agent
        factory = AgentFactory()

        # Get agent
        agent = factory.get_developmental_expert()

        # Verify agent created and cached
        assert agent is mock_agent
        assert "developmental_expert" in factory._cache
        assert len(factory._cache) == 1

        # Verify LlmAgent was created with correct config
        call_kwargs = mock_llm.call_args[1]
        assert call_kwargs["name"] == "developmental_expert"
        assert "developmental" in call_kwargs["description"].lower()
        assert "developmental" in call_kwargs["instruction"].lower()

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_get_developmental_expert_second_call_returns_cached_instance(
        self, mock_llm: Mock
    ) -> None:
        """Test second call returns same cached developmental expert."""
        mock_agent = Mock(spec=LlmAgent)
        mock_llm.return_value = mock_agent
        factory = AgentFactory()

        agent1 = factory.get_developmental_expert()
        agent2 = factory.get_developmental_expert()

        assert agent1 is agent2
        assert mock_llm.call_count == 1

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_get_memory_agent_with_tools_creates_and_caches_agent(self, mock_llm: Mock) -> None:
        """Test memory agent creation with tools."""
        mock_agent = Mock(spec=LlmAgent)
        mock_llm.return_value = mock_agent
        factory = AgentFactory()

        # Create mock tools
        mock_tools: list[Callable] = [Mock(), Mock()]

        # Get agent
        agent = factory.get_memory_agent(mock_tools)

        # Verify agent created and cached
        assert agent is mock_agent
        assert "memory_agent" in factory._cache
        assert len(factory._cache) == 1

        # Verify LlmAgent was created with correct config
        call_kwargs = mock_llm.call_args[1]
        assert call_kwargs["name"] == "memory_agent"
        assert (
            "pattern" in call_kwargs["description"].lower()
            or "memory" in call_kwargs["description"].lower()
        )
        assert (
            "memory" in call_kwargs["instruction"].lower()
            or "pattern" in call_kwargs["instruction"].lower()
        )
        assert call_kwargs["tools"] == mock_tools

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_get_memory_agent_second_call_returns_cached_instance(self, mock_llm: Mock) -> None:
        """Test second call returns same cached memory agent."""
        mock_agent = Mock(spec=LlmAgent)
        mock_llm.return_value = mock_agent
        factory = AgentFactory()

        mock_tools: list[Callable] = [Mock()]

        agent1 = factory.get_memory_agent(mock_tools)
        agent2 = factory.get_memory_agent(mock_tools)

        assert agent1 is agent2
        assert mock_llm.call_count == 1

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_get_activity_planner_agent_with_tools_creates_and_caches_agent(
        self, mock_llm: Mock
    ) -> None:
        """Test activity planner agent creation with tools."""
        mock_agent = Mock(spec=LlmAgent)
        mock_llm.return_value = mock_agent
        factory = AgentFactory()

        # Create mock tools
        mock_tools: list[Callable] = [Mock(), Mock(), Mock()]

        # Get agent
        agent = factory.get_activity_planner_agent(mock_tools)

        # Verify agent created and cached
        assert agent is mock_agent
        assert "activity_planner_agent" in factory._cache
        assert len(factory._cache) == 1

        # Verify LlmAgent was created with correct config
        call_kwargs = mock_llm.call_args[1]
        assert call_kwargs["name"] == "activity_planner"
        assert "activity" in call_kwargs["description"].lower()
        assert "activity" in call_kwargs["instruction"].lower()
        assert call_kwargs["tools"] == mock_tools

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_get_activity_planner_agent_second_call_returns_cached_instance(
        self, mock_llm: Mock
    ) -> None:
        """Test second call returns same cached activity planner agent."""
        mock_agent = Mock(spec=LlmAgent)
        mock_llm.return_value = mock_agent
        factory = AgentFactory()

        mock_tools: list[Callable] = [Mock()]

        agent1 = factory.get_activity_planner_agent(mock_tools)
        agent2 = factory.get_activity_planner_agent(mock_tools)

        assert agent1 is agent2
        assert mock_llm.call_count == 1

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_multiple_agents_can_coexist_in_cache(self, mock_llm: Mock) -> None:
        """Test multiple different agents can be cached simultaneously."""
        # Create different mock instances for each agent
        mock_adhd = Mock(spec=LlmAgent)
        mock_asd = Mock(spec=LlmAgent)
        mock_dev = Mock(spec=LlmAgent)
        mock_llm.side_effect = [mock_adhd, mock_asd, mock_dev]
        factory = AgentFactory()

        # Create multiple agents
        adhd = factory.get_adhd_expert()
        asd = factory.get_asd_expert()
        dev = factory.get_developmental_expert()

        # Verify all cached
        assert len(factory._cache) == 3
        assert "adhd_expert" in factory._cache
        assert "asd_expert" in factory._cache
        assert "developmental_expert" in factory._cache

        # Verify they are different instances
        assert adhd is not asd
        assert adhd is not dev
        assert asd is not dev

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_clear_cache_empties_cache(self, mock_llm: Mock) -> None:
        """Test clear_cache removes all cached agents."""
        mock_llm.return_value = Mock(spec=LlmAgent)
        factory = AgentFactory()

        # Create some agents
        factory.get_adhd_expert()
        factory.get_asd_expert()
        assert len(factory._cache) == 2

        # Clear cache
        factory.clear_cache()

        # Verify cache is empty
        assert len(factory._cache) == 0
        assert factory._cache == {}

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_agents_recreated_after_cache_clear(self, mock_llm: Mock) -> None:
        """Test agents can be recreated after cache clear."""
        mock_agent1 = Mock(spec=LlmAgent)
        mock_agent2 = Mock(spec=LlmAgent)
        mock_llm.side_effect = [mock_agent1, mock_agent2]
        factory = AgentFactory()

        # Create agent
        agent1 = factory.get_adhd_expert()
        assert agent1 is mock_agent1

        # Clear cache
        factory.clear_cache()

        # Create agent again
        agent2 = factory.get_adhd_expert()
        assert agent2 is mock_agent2

        # Verify they are different instances
        assert agent1 is not agent2
        assert mock_llm.call_count == 2

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_cache_keys_are_correct_for_all_agents(self, mock_llm: Mock) -> None:
        """Test all agent getters use correct cache keys."""
        mock_llm.return_value = Mock(spec=LlmAgent)
        factory = AgentFactory()
        mock_tools: list[Callable] = [Mock()]

        # Create all agents
        factory.get_adhd_expert()
        factory.get_asd_expert()
        factory.get_developmental_expert()
        factory.get_memory_agent(mock_tools)
        factory.get_activity_planner_agent(mock_tools)

        # Verify all cache keys exist
        expected_keys = {
            "adhd_expert",
            "asd_expert",
            "developmental_expert",
            "memory_agent",
            "activity_planner_agent",
        }
        assert set(factory._cache.keys()) == expected_keys
        assert len(factory._cache) == 5


class TestCreateSpecialistAgent:
    """Tests for create_specialist_agent factory function."""

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_creates_agent_with_correct_model(self, mock_llm: Mock) -> None:
        """Test agent is created with correct model from config."""
        mock_agent = Mock(spec=LlmAgent)
        mock_llm.return_value = mock_agent
        config = AgentConfig(
            name="test_agent",
            description="Test Description",
            system_prompt="Test Prompt",
            model="gemini-2.0-flash-exp",
        )

        result = create_specialist_agent(config)

        assert result is mock_agent
        mock_llm.assert_called_once()
        call_kwargs = mock_llm.call_args[1]
        assert call_kwargs["model"] == "gemini-2.0-flash-exp"

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_creates_agent_with_provided_name(self, mock_llm: Mock) -> None:
        """Test agent is created with provided name from config."""
        mock_llm.return_value = Mock(spec=LlmAgent)
        config = AgentConfig(
            name="my_custom_agent",
            description="Description",
            system_prompt="Prompt",
        )

        create_specialist_agent(config)

        call_kwargs = mock_llm.call_args[1]
        assert call_kwargs["name"] == "my_custom_agent"

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_creates_agent_with_provided_description(self, mock_llm: Mock) -> None:
        """Test agent is created with provided description from config."""
        mock_llm.return_value = Mock(spec=LlmAgent)
        config = AgentConfig(
            name="agent",
            description="My custom description",
            system_prompt="Prompt",
        )

        create_specialist_agent(config)

        call_kwargs = mock_llm.call_args[1]
        assert call_kwargs["description"] == "My custom description"

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_creates_agent_with_provided_system_prompt(self, mock_llm: Mock) -> None:
        """Test agent is created with provided system prompt from config."""
        mock_llm.return_value = Mock(spec=LlmAgent)
        config = AgentConfig(
            name="agent",
            description="Description",
            system_prompt="My custom system instruction",
        )

        create_specialist_agent(config)

        call_kwargs = mock_llm.call_args[1]
        assert call_kwargs["instruction"] == "My custom system instruction"

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_creates_agent_with_retry_config(self, mock_llm: Mock) -> None:
        """Test agent is created with retry configuration."""
        mock_llm.return_value = Mock(spec=LlmAgent)
        config = AgentConfig(
            name="agent",
            description="Description",
            system_prompt="Prompt",
        )

        create_specialist_agent(config)

        call_kwargs = mock_llm.call_args[1]
        assert "generate_content_config" in call_kwargs
        gen_config = call_kwargs["generate_content_config"]
        # Verify it has retry options (from get_retry_config)
        assert gen_config.http_options is not None
        assert gen_config.http_options.retry_options is not None

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_tools_defaults_to_empty_list_when_none(self, mock_llm: Mock) -> None:
        """Test tools parameter defaults to empty list when None."""
        mock_llm.return_value = Mock(spec=LlmAgent)
        config = AgentConfig(
            name="agent",
            description="Description",
            system_prompt="Prompt",
        )

        create_specialist_agent(config, tools=None)

        call_kwargs = mock_llm.call_args[1]
        assert call_kwargs["tools"] == []

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_tools_are_passed_when_provided(self, mock_llm: Mock) -> None:
        """Test tools are passed to LlmAgent when provided."""
        mock_llm.return_value = Mock(spec=LlmAgent)
        mock_tools: list[Callable] = [Mock(), Mock()]
        config = AgentConfig(
            name="agent",
            description="Description",
            system_prompt="Prompt",
        )

        create_specialist_agent(config, tools=mock_tools)

        call_kwargs = mock_llm.call_args[1]
        assert call_kwargs["tools"] == mock_tools
        assert len(call_kwargs["tools"]) == 2

    @patch("capstone.agents.specialist_factory.LlmAgent")
    def test_creates_agent_with_all_parameters_correct(self, mock_llm: Mock) -> None:
        """Test agent creation with all parameters validates correctly."""
        mock_agent = Mock(spec=LlmAgent)
        mock_llm.return_value = mock_agent
        mock_tools: list[Callable] = [Mock()]
        config = AgentConfig(
            name="complete_agent",
            description="Complete Description",
            system_prompt="Complete System Prompt",
            model="gemini-2.0-flash-exp",
        )

        result = create_specialist_agent(config, tools=mock_tools)

        # Verify return value
        assert result is mock_agent

        # Verify all parameters passed correctly
        mock_llm.assert_called_once()
        call_kwargs = mock_llm.call_args[1]

        assert call_kwargs["model"] == "gemini-2.0-flash-exp"
        assert call_kwargs["name"] == "complete_agent"
        assert call_kwargs["description"] == "Complete Description"
        assert call_kwargs["instruction"] == "Complete System Prompt"
        assert call_kwargs["tools"] == mock_tools


class TestAgentConfigs:
    """Tests for AGENT_CONFIGS dictionary."""

    def test_agent_configs_contains_all_expected_agents(self) -> None:
        """Test AGENT_CONFIGS contains all expected agent types."""
        expected_keys = {
            "adhd_expert",
            "asd_expert",
            "developmental_expert",
            "memory_agent",
            "activity_planner",
        }
        assert set(AGENT_CONFIGS.keys()) == expected_keys

    def test_each_config_is_agent_config_instance(self) -> None:
        """Test each config is an AgentConfig instance."""
        for key, config in AGENT_CONFIGS.items():
            assert isinstance(config, AgentConfig), f"{key} is not AgentConfig"

    def test_each_config_has_required_fields(self) -> None:
        """Test each config has all required fields populated."""
        for key, config in AGENT_CONFIGS.items():
            assert config.name, f"{key} missing name"
            assert config.description, f"{key} missing description"
            assert config.system_prompt, f"{key} missing system_prompt"
            assert config.model, f"{key} missing model"

    def test_adhd_config_has_correct_name(self) -> None:
        """Test ADHD config has correct name."""
        assert AGENT_CONFIGS["adhd_expert"].name == "adhd_expert"

    def test_asd_config_has_correct_name(self) -> None:
        """Test ASD config has correct name."""
        assert AGENT_CONFIGS["asd_expert"].name == "asd_expert"

    def test_developmental_config_has_correct_name(self) -> None:
        """Test developmental config has correct name."""
        assert AGENT_CONFIGS["developmental_expert"].name == "developmental_expert"

    def test_memory_config_has_correct_name(self) -> None:
        """Test memory config has correct name."""
        assert AGENT_CONFIGS["memory_agent"].name == "memory_agent"

    def test_activity_planner_config_has_correct_name(self) -> None:
        """Test activity planner config has correct name."""
        assert AGENT_CONFIGS["activity_planner"].name == "activity_planner"
