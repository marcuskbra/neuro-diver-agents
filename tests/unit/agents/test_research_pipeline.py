"""Tests for research pipeline agent."""

from unittest.mock import MagicMock, patch

from capstone.agents.research_pipeline import (
    create_behavior_analysis_pipeline,
    create_custom_pipeline,
    create_research_pipeline,
)


class TestCreateResearchPipeline:
    """Tests for create_research_pipeline function."""

    @patch("capstone.agents.research_pipeline.SequentialAgent")
    def test_creates_sequential_agent_instance(self, mock_sequential_agent: MagicMock) -> None:
        """Test creates SequentialAgent with correct configuration."""
        mock_researcher = MagicMock()
        mock_analyzer = MagicMock()
        mock_synthesizer = MagicMock()

        create_research_pipeline(mock_researcher, mock_analyzer, mock_synthesizer)

        mock_sequential_agent.assert_called_once()

    @patch("capstone.agents.research_pipeline.SequentialAgent")
    def test_has_correct_name(self, mock_sequential_agent: MagicMock) -> None:
        """Test pipeline has correct name."""
        mock_researcher = MagicMock()
        mock_analyzer = MagicMock()
        mock_synthesizer = MagicMock()

        create_research_pipeline(mock_researcher, mock_analyzer, mock_synthesizer)

        call_kwargs = mock_sequential_agent.call_args[1]
        assert call_kwargs["name"] == "research_pipeline"

    @patch("capstone.agents.research_pipeline.SequentialAgent")
    def test_has_description(self, mock_sequential_agent: MagicMock) -> None:
        """Test pipeline has descriptive text."""
        mock_researcher = MagicMock()
        mock_analyzer = MagicMock()
        mock_synthesizer = MagicMock()

        create_research_pipeline(mock_researcher, mock_analyzer, mock_synthesizer)

        call_kwargs = mock_sequential_agent.call_args[1]
        description = call_kwargs["description"]
        assert "sequential" in description.lower()
        assert "research" in description.lower()

    @patch("capstone.agents.research_pipeline.SequentialAgent")
    def test_contains_three_stages(self, mock_sequential_agent: MagicMock) -> None:
        """Test pipeline contains all three stage agents."""
        mock_researcher = MagicMock()
        mock_analyzer = MagicMock()
        mock_synthesizer = MagicMock()

        create_research_pipeline(mock_researcher, mock_analyzer, mock_synthesizer)

        call_kwargs = mock_sequential_agent.call_args[1]
        sub_agents = call_kwargs["sub_agents"]
        assert len(sub_agents) == 3
        assert mock_researcher in sub_agents
        assert mock_analyzer in sub_agents
        assert mock_synthesizer in sub_agents

    @patch("capstone.agents.research_pipeline.SequentialAgent")
    def test_stages_order_is_sequential(self, mock_sequential_agent: MagicMock) -> None:
        """Test stages maintain sequential order: Research -> Analyze -> Synthesize."""
        mock_researcher = MagicMock()
        mock_analyzer = MagicMock()
        mock_synthesizer = MagicMock()

        create_research_pipeline(mock_researcher, mock_analyzer, mock_synthesizer)

        call_kwargs = mock_sequential_agent.call_args[1]
        sub_agents = call_kwargs["sub_agents"]
        assert sub_agents[0] is mock_researcher
        assert sub_agents[1] is mock_analyzer
        assert sub_agents[2] is mock_synthesizer


class TestCreateBehaviorAnalysisPipeline:
    """Tests for create_behavior_analysis_pipeline function."""

    @patch("capstone.agents.research_pipeline.SequentialAgent")
    @patch("capstone.agents.specialist_factory.create_developmental_expert")
    @patch("capstone.agents.specialist_factory.create_asd_expert")
    @patch("capstone.agents.specialist_factory.create_adhd_expert")
    def test_creates_sequential_agent_instance(
        self,
        mock_adhd_factory: MagicMock,
        mock_asd_factory: MagicMock,
        mock_dev_factory: MagicMock,
        mock_sequential_agent: MagicMock,
    ) -> None:
        """Test creates SequentialAgent with specialist experts."""
        mock_adhd_factory.return_value = MagicMock()
        mock_asd_factory.return_value = MagicMock()
        mock_dev_factory.return_value = MagicMock()

        create_behavior_analysis_pipeline()

        mock_sequential_agent.assert_called_once()

    @patch("capstone.agents.research_pipeline.SequentialAgent")
    @patch("capstone.agents.specialist_factory.create_developmental_expert")
    @patch("capstone.agents.specialist_factory.create_asd_expert")
    @patch("capstone.agents.specialist_factory.create_adhd_expert")
    def test_has_correct_name(
        self,
        mock_adhd_factory: MagicMock,
        mock_asd_factory: MagicMock,
        mock_dev_factory: MagicMock,
        mock_sequential_agent: MagicMock,
    ) -> None:
        """Test pipeline has behavior analysis name."""
        mock_adhd_factory.return_value = MagicMock()
        mock_asd_factory.return_value = MagicMock()
        mock_dev_factory.return_value = MagicMock()

        create_behavior_analysis_pipeline()

        call_kwargs = mock_sequential_agent.call_args[1]
        assert call_kwargs["name"] == "behavior_analysis_pipeline"

    @patch("capstone.agents.research_pipeline.SequentialAgent")
    @patch("capstone.agents.specialist_factory.create_developmental_expert")
    @patch("capstone.agents.specialist_factory.create_asd_expert")
    @patch("capstone.agents.specialist_factory.create_adhd_expert")
    def test_contains_specialist_experts(
        self,
        mock_adhd_factory: MagicMock,
        mock_asd_factory: MagicMock,
        mock_dev_factory: MagicMock,
        mock_sequential_agent: MagicMock,
    ) -> None:
        """Test pipeline contains ADHD, ASD, and developmental experts."""
        mock_adhd = MagicMock()
        mock_asd = MagicMock()
        mock_dev = MagicMock()
        mock_adhd_factory.return_value = mock_adhd
        mock_asd_factory.return_value = mock_asd
        mock_dev_factory.return_value = mock_dev

        create_behavior_analysis_pipeline()

        call_kwargs = mock_sequential_agent.call_args[1]
        sub_agents = call_kwargs["sub_agents"]
        assert len(sub_agents) == 3
        assert sub_agents[0] is mock_adhd
        assert sub_agents[1] is mock_asd
        assert sub_agents[2] is mock_dev

    @patch("capstone.agents.research_pipeline.SequentialAgent")
    @patch("capstone.agents.specialist_factory.create_developmental_expert")
    @patch("capstone.agents.specialist_factory.create_asd_expert")
    @patch("capstone.agents.specialist_factory.create_adhd_expert")
    def test_calls_expert_factories(
        self,
        mock_adhd_factory: MagicMock,
        mock_asd_factory: MagicMock,
        mock_dev_factory: MagicMock,
        mock_sequential_agent: MagicMock,
    ) -> None:
        """Test pipeline calls all expert factory functions."""
        mock_adhd_factory.return_value = MagicMock()
        mock_asd_factory.return_value = MagicMock()
        mock_dev_factory.return_value = MagicMock()

        create_behavior_analysis_pipeline()

        mock_adhd_factory.assert_called_once()
        mock_asd_factory.assert_called_once()
        mock_dev_factory.assert_called_once()


class TestCreateCustomPipeline:
    """Tests for create_custom_pipeline function."""

    @patch("capstone.agents.research_pipeline.SequentialAgent")
    def test_creates_sequential_agent_instance(self, mock_sequential_agent: MagicMock) -> None:
        """Test creates SequentialAgent with custom stages."""
        mock_stage1 = MagicMock()
        mock_stage2 = MagicMock()

        create_custom_pipeline(mock_stage1, mock_stage2)

        mock_sequential_agent.assert_called_once()

    @patch("capstone.agents.research_pipeline.SequentialAgent")
    def test_uses_default_name(self, mock_sequential_agent: MagicMock) -> None:
        """Test uses default name when not provided."""
        mock_stage = MagicMock()

        create_custom_pipeline(mock_stage)

        call_kwargs = mock_sequential_agent.call_args[1]
        assert call_kwargs["name"] == "custom_pipeline"

    @patch("capstone.agents.research_pipeline.SequentialAgent")
    def test_uses_custom_name(self, mock_sequential_agent: MagicMock) -> None:
        """Test uses custom name when provided."""
        mock_stage = MagicMock()

        create_custom_pipeline(mock_stage, name="my_pipeline")

        call_kwargs = mock_sequential_agent.call_args[1]
        assert call_kwargs["name"] == "my_pipeline"

    @patch("capstone.agents.research_pipeline.SequentialAgent")
    def test_auto_generates_description(self, mock_sequential_agent: MagicMock) -> None:
        """Test auto-generates description with stage count."""
        mock_stage1 = MagicMock()
        mock_stage2 = MagicMock()
        mock_stage3 = MagicMock()

        create_custom_pipeline(mock_stage1, mock_stage2, mock_stage3)

        call_kwargs = mock_sequential_agent.call_args[1]
        description = call_kwargs["description"]
        assert "3" in description
        assert "stages" in description.lower()

    @patch("capstone.agents.research_pipeline.SequentialAgent")
    def test_uses_custom_description(self, mock_sequential_agent: MagicMock) -> None:
        """Test uses custom description when provided."""
        mock_stage = MagicMock()

        create_custom_pipeline(mock_stage, description="My custom pipeline description")

        call_kwargs = mock_sequential_agent.call_args[1]
        assert call_kwargs["description"] == "My custom pipeline description"

    @patch("capstone.agents.research_pipeline.SequentialAgent")
    def test_works_with_single_stage(self, mock_sequential_agent: MagicMock) -> None:
        """Test pipeline works with single stage."""
        mock_stage = MagicMock()

        create_custom_pipeline(mock_stage)

        call_kwargs = mock_sequential_agent.call_args[1]
        sub_agents = call_kwargs["sub_agents"]
        assert len(sub_agents) == 1
        assert sub_agents[0] is mock_stage

    @patch("capstone.agents.research_pipeline.SequentialAgent")
    def test_works_with_many_stages(self, mock_sequential_agent: MagicMock) -> None:
        """Test pipeline works with many stages."""
        stages = [MagicMock() for _ in range(5)]

        create_custom_pipeline(*stages)

        call_kwargs = mock_sequential_agent.call_args[1]
        sub_agents = call_kwargs["sub_agents"]
        assert len(sub_agents) == 5
        for i, stage in enumerate(stages):
            assert sub_agents[i] is stage

    @patch("capstone.agents.research_pipeline.SequentialAgent")
    def test_preserves_stage_order(self, mock_sequential_agent: MagicMock) -> None:
        """Test stages maintain provided order."""
        mock_stage1 = MagicMock()
        mock_stage2 = MagicMock()
        mock_stage3 = MagicMock()

        create_custom_pipeline(mock_stage1, mock_stage2, mock_stage3)

        call_kwargs = mock_sequential_agent.call_args[1]
        sub_agents = call_kwargs["sub_agents"]
        assert sub_agents[0] is mock_stage1
        assert sub_agents[1] is mock_stage2
        assert sub_agents[2] is mock_stage3
