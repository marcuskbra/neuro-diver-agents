"""Unit tests for activity planner tool."""

from capstone.models.activity import ActivityGoal
from capstone.models.results import ToolSuccess
from capstone.tools.activity_planner import get_activity_plan


class TestActivityPlanner:
    """Test activity planning tool."""

    def test_get_activity_plan_with_executive_function_goal_returns_plan(
        self, activity_request_factory
    ):
        """Test activity planner returns plan for executive function goal."""
        request = activity_request_factory(
            goal=ActivityGoal.EXECUTIVE_FUNCTION,
            duration_minutes=15,
        )

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        assert result.success is True
        assert "name" in result.data
        assert result.data["name"] == "Morning Routine Mission"
        assert result.data["goal"] == ActivityGoal.EXECUTIVE_FUNCTION.value
        assert result.data["duration"] == 15

    def test_get_activity_plan_with_transition_support_goal_returns_plan(
        self, activity_request_factory
    ):
        """Test activity planner returns plan for transition support goal."""
        request = activity_request_factory(
            goal=ActivityGoal.TRANSITION_SUPPORT,
            duration_minutes=10,
        )

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        assert result.success is True
        assert result.data["name"] == "Transition Timer Activity"
        assert result.data["goal"] == ActivityGoal.TRANSITION_SUPPORT.value
        assert result.data["duration"] == 10

    def test_get_activity_plan_with_homework_support_goal_returns_plan(
        self, activity_request_factory
    ):
        """Test activity planner returns plan for homework support goal."""
        request = activity_request_factory(
            goal=ActivityGoal.HOMEWORK_SUPPORT,
            duration_minutes=30,
        )

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        assert result.success is True
        assert result.data["name"] == "Homework Break Down Strategy"
        assert result.data["goal"] == ActivityGoal.HOMEWORK_SUPPORT.value
        assert result.data["duration"] == 30

    def test_get_activity_plan_with_engagement_goal_returns_plan(self, activity_request_factory):
        """Test activity planner returns plan for engagement goal."""
        request = activity_request_factory(
            goal=ActivityGoal.ENGAGEMENT,
            duration_minutes=20,
        )

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        assert result.success is True
        assert result.data["name"] == "Two-Person Board Game Practice"
        assert result.data["goal"] == ActivityGoal.ENGAGEMENT.value
        assert result.data["duration"] == 20

    def test_get_activity_plan_adjusts_duration_when_different_from_template(
        self, activity_request_factory
    ):
        """Test activity planner adjusts duration when requested differs from template."""
        request = activity_request_factory(
            goal=ActivityGoal.ENGAGEMENT,
            duration_minutes=45,  # Different from template's 20
        )

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        assert result.data["duration"] == 45

    def test_get_activity_plan_result_contains_materials_list(self, activity_request_factory):
        """Test activity plan result contains materials list."""
        request = activity_request_factory(goal=ActivityGoal.EXECUTIVE_FUNCTION)

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        assert "materials" in result.data
        assert isinstance(result.data["materials"], list)
        assert len(result.data["materials"]) > 0
        # Check specific materials from executive function template
        assert "Visual checklist with pictures" in result.data["materials"]

    def test_get_activity_plan_result_contains_environmental_setup(self, activity_request_factory):
        """Test activity plan result contains environmental setup."""
        request = activity_request_factory(goal=ActivityGoal.HOMEWORK_SUPPORT)

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        assert "setup" in result.data
        assert isinstance(result.data["setup"], str)
        assert len(result.data["setup"]) > 0
        assert "Quiet corner" in result.data["setup"]

    def test_get_activity_plan_result_contains_structure_steps(self, activity_request_factory):
        """Test activity plan result contains structure steps."""
        request = activity_request_factory(goal=ActivityGoal.TRANSITION_SUPPORT)

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        assert "structure" in result.data
        assert isinstance(result.data["structure"], list)
        assert len(result.data["structure"]) > 0

    def test_get_activity_plan_result_contains_success_criteria(self, activity_request_factory):
        """Test activity plan result contains success criteria."""
        request = activity_request_factory(goal=ActivityGoal.ENGAGEMENT)

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        assert "success_criteria" in result.data
        assert isinstance(result.data["success_criteria"], list)
        assert len(result.data["success_criteria"]) > 0

    def test_get_activity_plan_result_contains_adaptations(self, activity_request_factory):
        """Test activity plan result contains adaptations."""
        request = activity_request_factory(goal=ActivityGoal.HOMEWORK_SUPPORT)

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        assert "adaptations" in result.data
        assert isinstance(result.data["adaptations"], list)

    def test_get_activity_plan_with_all_goals_succeeds(self, activity_request_factory):
        """Test activity planner succeeds for all defined goals."""
        for goal in ActivityGoal:
            request = activity_request_factory(goal=goal)

            result = get_activity_plan(request)

            assert isinstance(result, ToolSuccess)
            assert result.success is True
            assert result.data["goal"] == goal.value

    def test_get_activity_plan_with_minimum_duration_succeeds(self, activity_request_factory):
        """Test activity planner accepts minimum duration of 5 minutes."""
        request = activity_request_factory(
            goal=ActivityGoal.TRANSITION_SUPPORT,
            duration_minutes=5,
        )

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        assert result.data["duration"] == 5

    def test_get_activity_plan_with_maximum_duration_succeeds(self, activity_request_factory):
        """Test activity planner accepts maximum duration of 120 minutes."""
        request = activity_request_factory(
            goal=ActivityGoal.HOMEWORK_SUPPORT,
            duration_minutes=120,
        )

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        assert result.data["duration"] == 120

    def test_get_activity_plan_result_structure_matches_schema(self, activity_request_factory):
        """Test activity plan result has expected structure."""
        request = activity_request_factory(goal=ActivityGoal.EXECUTIVE_FUNCTION)

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)

        # Check all required keys present
        required_keys = {
            "name",
            "goal",
            "materials",
            "setup",
            "duration",
            "structure",
            "success_criteria",
            "adaptations",
        }
        assert required_keys.issubset(result.data.keys())

    def test_get_activity_plan_with_available_materials_succeeds(self, activity_request_factory):
        """Test activity planner handles available materials specification."""
        request = activity_request_factory(
            goal=ActivityGoal.ENGAGEMENT,
            available_materials=["timer", "board games", "fidgets"],
        )

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        # Plan should still return regardless of available materials
        assert "materials" in result.data

    def test_get_activity_plan_with_specific_needs_succeeds(self, activity_request_factory):
        """Test activity planner handles specific needs specification."""
        request = activity_request_factory(
            goal=ActivityGoal.HOMEWORK_SUPPORT,
            specific_needs="Child needs frequent breaks and prefers quiet environment",
        )

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)

    def test_get_activity_plan_data_types_are_correct(self, activity_request_factory):
        """Test activity plan result has correct data types."""
        request = activity_request_factory(goal=ActivityGoal.TRANSITION_SUPPORT)

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        assert isinstance(result.data["name"], str)
        assert isinstance(result.data["goal"], str)
        assert isinstance(result.data["materials"], list)
        assert isinstance(result.data["setup"], str)
        assert isinstance(result.data["duration"], int)
        assert isinstance(result.data["structure"], list)
        assert isinstance(result.data["success_criteria"], list)
        assert isinstance(result.data["adaptations"], list)

    def test_get_activity_plan_materials_are_all_strings(self, activity_request_factory):
        """Test activity plan materials list contains only strings."""
        request = activity_request_factory(goal=ActivityGoal.EXECUTIVE_FUNCTION)

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        materials = result.get_list("materials")
        for material in materials:
            assert isinstance(material, str)

    def test_get_activity_plan_structure_steps_are_all_strings(self, activity_request_factory):
        """Test activity plan structure list contains only strings."""
        request = activity_request_factory(goal=ActivityGoal.HOMEWORK_SUPPORT)

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        structure = result.get_list("structure")
        for step in structure:
            assert isinstance(step, str)

    def test_get_activity_plan_success_criteria_are_all_strings(self, activity_request_factory):
        """Test activity plan success criteria list contains only strings."""
        request = activity_request_factory(goal=ActivityGoal.ENGAGEMENT)

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        success_criteria = result.get_list("success_criteria")
        for criterion in success_criteria:
            assert isinstance(criterion, str)

    def test_get_activity_plan_adaptations_are_all_strings(self, activity_request_factory):
        """Test activity plan adaptations list contains only strings."""
        request = activity_request_factory(goal=ActivityGoal.TRANSITION_SUPPORT)

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        adaptations = result.get_list("adaptations")
        for adaptation in adaptations:
            assert isinstance(adaptation, str)

    def test_get_activity_plan_preserves_goal_enum_value(self, activity_request_factory):
        """Test activity plan preserves the exact goal enum value."""
        request = activity_request_factory(goal=ActivityGoal.HOMEWORK_SUPPORT)

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        assert result.data["goal"] == "homework_support"

    def test_get_activity_plan_with_empty_materials_list_succeeds(self, activity_request_factory):
        """Test activity planner handles empty available materials list."""
        request = activity_request_factory(
            goal=ActivityGoal.ENGAGEMENT,
            available_materials=[],
        )

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)
        # Plan should still return template materials
        materials = result.get_list("materials")
        assert len(materials) > 0

    def test_get_activity_plan_with_none_specific_needs_succeeds(self, activity_request_factory):
        """Test activity planner handles None specific needs."""
        request = activity_request_factory(
            goal=ActivityGoal.EXECUTIVE_FUNCTION,
            specific_needs=None,
        )

        result = get_activity_plan(request)

        assert isinstance(result, ToolSuccess)

    def test_get_activity_plan_each_goal_has_unique_plan(self, activity_request_factory):
        """Test each activity goal returns a unique plan."""
        plans = {}

        for goal in ActivityGoal:
            request = activity_request_factory(goal=goal)
            result = get_activity_plan(request)

            assert isinstance(result, ToolSuccess)
            plans[goal] = result.data["name"]

        # Check all plan names are unique
        assert len(plans) == len(set(plans.values()))
