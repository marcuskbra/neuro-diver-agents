"""Tests for parallel analyzer agent."""

from unittest.mock import MagicMock, patch

from capstone.agents.parallel_analyzer import (
    create_parallel_expert_panel,
    create_research_panel,
)


class TestCreateParallelExpertPanel:
    """Tests for create_parallel_expert_panel function."""

    @patch("capstone.agents.parallel_analyzer.ParallelAgent")
    def test_creates_parallel_agent_instance(self, mock_parallel_agent: MagicMock) -> None:
        """Test creates ParallelAgent with correct configuration."""
        mock_adhd = MagicMock()
        mock_asd = MagicMock()
        mock_dev = MagicMock()

        create_parallel_expert_panel(mock_adhd, mock_asd, mock_dev)

        mock_parallel_agent.assert_called_once()

    @patch("capstone.agents.parallel_analyzer.ParallelAgent")
    def test_has_correct_name(self, mock_parallel_agent: MagicMock) -> None:
        """Test panel has correct name."""
        mock_adhd = MagicMock()
        mock_asd = MagicMock()
        mock_dev = MagicMock()

        create_parallel_expert_panel(mock_adhd, mock_asd, mock_dev)

        call_kwargs = mock_parallel_agent.call_args[1]
        assert call_kwargs["name"] == "parallel_expert_panel"

    @patch("capstone.agents.parallel_analyzer.ParallelAgent")
    def test_has_description(self, mock_parallel_agent: MagicMock) -> None:
        """Test panel has descriptive text."""
        mock_adhd = MagicMock()
        mock_asd = MagicMock()
        mock_dev = MagicMock()

        create_parallel_expert_panel(mock_adhd, mock_asd, mock_dev)

        call_kwargs = mock_parallel_agent.call_args[1]
        description = call_kwargs["description"]
        assert "ADHD" in description
        assert "ASD" in description
        assert "parallel" in description.lower()

    @patch("capstone.agents.parallel_analyzer.ParallelAgent")
    def test_contains_three_sub_agents(self, mock_parallel_agent: MagicMock) -> None:
        """Test panel contains all three expert agents."""
        mock_adhd = MagicMock()
        mock_asd = MagicMock()
        mock_dev = MagicMock()

        create_parallel_expert_panel(mock_adhd, mock_asd, mock_dev)

        call_kwargs = mock_parallel_agent.call_args[1]
        sub_agents = call_kwargs["sub_agents"]
        assert len(sub_agents) == 3
        assert mock_adhd in sub_agents
        assert mock_asd in sub_agents
        assert mock_dev in sub_agents

    @patch("capstone.agents.parallel_analyzer.ParallelAgent")
    def test_sub_agents_order_preserved(self, mock_parallel_agent: MagicMock) -> None:
        """Test sub-agents maintain provided order."""
        mock_adhd = MagicMock()
        mock_asd = MagicMock()
        mock_dev = MagicMock()

        create_parallel_expert_panel(mock_adhd, mock_asd, mock_dev)

        call_kwargs = mock_parallel_agent.call_args[1]
        sub_agents = call_kwargs["sub_agents"]
        assert sub_agents[0] is mock_adhd
        assert sub_agents[1] is mock_asd
        assert sub_agents[2] is mock_dev


class TestCreateResearchPanel:
    """Tests for create_research_panel function."""

    @patch("capstone.agents.parallel_analyzer.ParallelAgent")
    def test_creates_parallel_agent_instance(self, mock_parallel_agent: MagicMock) -> None:
        """Test creates ParallelAgent with variable experts."""
        mock_expert1 = MagicMock()
        mock_expert2 = MagicMock()

        create_research_panel(mock_expert1, mock_expert2)

        mock_parallel_agent.assert_called_once()

    @patch("capstone.agents.parallel_analyzer.ParallelAgent")
    def test_has_correct_name(self, mock_parallel_agent: MagicMock) -> None:
        """Test panel has correct name."""
        mock_expert = MagicMock()

        create_research_panel(mock_expert)

        call_kwargs = mock_parallel_agent.call_args[1]
        assert call_kwargs["name"] == "research_panel"

    @patch("capstone.agents.parallel_analyzer.ParallelAgent")
    def test_description_includes_expert_count(self, mock_parallel_agent: MagicMock) -> None:
        """Test description mentions number of specialists."""
        mock_expert1 = MagicMock()
        mock_expert2 = MagicMock()
        mock_expert3 = MagicMock()

        create_research_panel(mock_expert1, mock_expert2, mock_expert3)

        call_kwargs = mock_parallel_agent.call_args[1]
        description = call_kwargs["description"]
        assert "3" in description
        assert "specialists" in description.lower()

    @patch("capstone.agents.parallel_analyzer.ParallelAgent")
    def test_works_with_single_expert(self, mock_parallel_agent: MagicMock) -> None:
        """Test panel works with single expert."""
        mock_expert = MagicMock()

        create_research_panel(mock_expert)

        call_kwargs = mock_parallel_agent.call_args[1]
        sub_agents = call_kwargs["sub_agents"]
        assert len(sub_agents) == 1
        assert sub_agents[0] is mock_expert

    @patch("capstone.agents.parallel_analyzer.ParallelAgent")
    def test_works_with_many_experts(self, mock_parallel_agent: MagicMock) -> None:
        """Test panel works with many experts."""
        experts = [MagicMock() for _ in range(5)]

        create_research_panel(*experts)

        call_kwargs = mock_parallel_agent.call_args[1]
        sub_agents = call_kwargs["sub_agents"]
        assert len(sub_agents) == 5
        for expert in experts:
            assert expert in sub_agents
