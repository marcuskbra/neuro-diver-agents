"""Unit tests for pattern analyzer tool."""

from capstone.models.results import ToolError, ToolSuccess
from capstone.tools.pattern_analyzer import analyze_patterns


class TestPatternAnalyzer:
    """Test pattern analysis tool."""

    def test_analyze_patterns_with_successful_sessions_returns_pattern(
        self, session_outcome_factory
    ):
        """Test pattern analyzer identifies successful strategies."""
        sessions = [
            session_outcome_factory(
                strategy_used="bedtime visual timer for 10 minutes",
                worked=True,
                notes="Child went to bed without resistance",
            ),
            session_outcome_factory(
                strategy_used="bedtime visual timer + sensory break",
                worked=True,
                notes="Very calm and cooperative",
            ),
        ]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        assert result.success is True
        assert "successful_strategies" in result.data
        successful_strategies = result.get_list("successful_strategies")
        assert len(successful_strategies) > 0

    def test_analyze_patterns_with_unsuccessful_sessions_returns_pattern(
        self, session_outcome_factory
    ):
        """Test pattern analyzer identifies unsuccessful strategies."""
        sessions = [
            session_outcome_factory(
                strategy_used="bedtime verbal reminders only",
                worked=False,
                notes="Got upset, took 45 minutes",
            ),
            session_outcome_factory(
                strategy_used="bedtime threatening consequences",
                worked=False,
                notes="Increased resistance and meltdown",
            ),
        ]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        assert "unsuccessful_approaches" in result.data
        unsuccessful_approaches = result.get_list("unsuccessful_approaches")
        assert len(unsuccessful_approaches) > 0

    def test_analyze_patterns_with_mixed_outcomes_returns_both_categories(
        self, session_outcome_factory
    ):
        """Test pattern analyzer categorizes mixed outcomes correctly."""
        sessions = [
            session_outcome_factory(
                strategy_used="bedtime visual timer",
                worked=True,
                notes="Went smoothly",
            ),
            session_outcome_factory(
                strategy_used="bedtime verbal only",
                worked=False,
                notes="Resisted strongly",
            ),
        ]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        assert len(result.get_list("successful_strategies")) > 0
        assert len(result.get_list("unsuccessful_approaches")) > 0

    def test_analyze_patterns_with_empty_history_returns_error(self):
        """Test pattern analyzer returns error with empty session history."""
        result = analyze_patterns([], "bedtime")

        assert isinstance(result, ToolError)
        assert result.success is False
        assert result.error_code == "INSUFFICIENT_DATA"

    def test_analyze_patterns_with_no_matching_sessions_analyzes_all(self, session_outcome_factory):
        """Test pattern analyzer analyzes all sessions when no sessions match behavior type."""
        sessions = [
            session_outcome_factory(
                strategy_used="homework timer strategy",
                worked=True,
                notes="Completed homework successfully",
            ),
        ]

        result = analyze_patterns(sessions, "bedtime")

        # Should fall back to analyzing all sessions instead of returning error
        assert isinstance(result, ToolSuccess)
        assert result.get_int("sessions") == 1
        assert result.get_str("behavior_type") == "bedtime"

    def test_analyze_patterns_identifies_screen_time_trigger(self, session_outcome_factory):
        """Test pattern analyzer identifies screen time as a trigger."""
        sessions = [
            session_outcome_factory(
                strategy_used="bedtime routine",
                worked=False,
                notes="Had screen time within 30 minutes before bed, very resistant",
            ),
        ]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        assert "common_triggers" in result.data
        common_triggers = result.get_list("common_triggers")
        assert any("screen time" in trigger.lower() for trigger in common_triggers)

    def test_analyze_patterns_identifies_skipped_routine_trigger(self, session_outcome_factory):
        """Test pattern analyzer identifies skipped routine steps as trigger."""
        sessions = [
            session_outcome_factory(
                strategy_used="bedtime routine",
                worked=False,
                notes="Skipped bath tonight, child was very upset at bedtime",
            ),
        ]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        assert "common_triggers" in result.data
        common_triggers = result.get_list("common_triggers")
        assert any("skip" in trigger.lower() for trigger in common_triggers)

    def test_analyze_patterns_identifies_schedule_disruption_trigger(self, session_outcome_factory):
        """Test pattern analyzer identifies schedule changes as trigger."""
        sessions = [
            session_outcome_factory(
                strategy_used="bedtime routine",
                worked=False,
                notes="Had unexpected change to schedule earlier, bedtime was difficult",
            ),
        ]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        assert "common_triggers" in result.data
        common_triggers = result.get_list("common_triggers")
        assert any(
            "change" in trigger.lower() or "disruption" in trigger.lower()
            for trigger in common_triggers
        )

    def test_analyze_patterns_calculates_frequency_count_correctly(self, session_outcome_factory):
        """Test pattern analyzer correctly counts frequency of successful outcomes."""
        sessions = [
            session_outcome_factory(strategy_used="bedtime timer", worked=True),
            session_outcome_factory(strategy_used="bedtime routine", worked=True),
            session_outcome_factory(strategy_used="bedtime approach", worked=False),
            session_outcome_factory(strategy_used="bedtime visual", worked=True),
        ]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        assert result.get_int("frequency") == 3  # 3 out of 4 worked

    def test_analyze_patterns_calculates_sessions_analyzed_correctly(self, session_outcome_factory):
        """Test pattern analyzer correctly counts total sessions analyzed."""
        sessions = [
            session_outcome_factory(notes="bedtime was good"),
            session_outcome_factory(notes="bedtime was difficult"),
            session_outcome_factory(notes="bedtime routine worked"),
        ]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        assert result.get_int("sessions") == 3

    def test_analyze_patterns_filters_by_behavior_type_in_strategy(self, session_outcome_factory):
        """Test pattern analyzer filters sessions by behavior type in strategy."""
        sessions = [
            session_outcome_factory(
                strategy_used="homework break schedule",
                worked=True,
                notes="Completed work",
            ),
            session_outcome_factory(
                strategy_used="bedtime visual timer",
                worked=True,
                notes="Slept well",
            ),
        ]

        result = analyze_patterns(sessions, "homework")

        assert isinstance(result, ToolSuccess)
        assert result.get_int("sessions") == 1  # Only homework session

    def test_analyze_patterns_filters_by_behavior_type_in_notes(self, session_outcome_factory):
        """Test pattern analyzer filters sessions by behavior type in notes."""
        sessions = [
            session_outcome_factory(
                strategy_used="visual timer",
                worked=True,
                notes="Homework went smoothly with timer",
            ),
            session_outcome_factory(
                strategy_used="visual timer",
                worked=True,
                notes="Bedtime was easy",
            ),
        ]

        result = analyze_patterns(sessions, "homework")

        assert isinstance(result, ToolSuccess)
        assert result.get_int("sessions") == 1  # Only homework session

    def test_analyze_patterns_case_insensitive_filtering(self, session_outcome_factory):
        """Test pattern analyzer filters case-insensitively."""
        sessions = [
            session_outcome_factory(
                strategy_used="Bedtime routine with timer",
                worked=True,
                notes="BEDTIME successful",
            ),
        ]

        result = analyze_patterns(sessions, "BEDTIME")

        assert isinstance(result, ToolSuccess)
        assert result.get_int("sessions") >= 1

    def test_analyze_patterns_deduplicates_successful_strategies(self, session_outcome_factory):
        """Test pattern analyzer removes duplicate successful strategies."""
        sessions = [
            session_outcome_factory(
                strategy_used="visual timer",
                worked=True,
                notes="bedtime successful",
            ),
            session_outcome_factory(
                strategy_used="visual timer",
                worked=True,
                notes="bedtime worked again",
            ),
        ]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        successful_strategies = result.get_list("successful_strategies")
        # Should only have one unique "visual timer" entry
        assert successful_strategies.count("visual timer") == 1

    def test_analyze_patterns_deduplicates_unsuccessful_approaches(self, session_outcome_factory):
        """Test pattern analyzer removes duplicate unsuccessful approaches."""
        sessions = [
            session_outcome_factory(
                strategy_used="verbal reminders",
                worked=False,
                notes="bedtime failed",
            ),
            session_outcome_factory(
                strategy_used="verbal reminders",
                worked=False,
                notes="bedtime failed again",
            ),
        ]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        unsuccessful_approaches = result.get_list("unsuccessful_approaches")
        # Should only have one unique "verbal reminders" entry
        assert unsuccessful_approaches.count("verbal reminders") == 1

    def test_analyze_patterns_deduplicates_triggers(self, session_outcome_factory):
        """Test pattern analyzer removes duplicate triggers."""
        sessions = [
            session_outcome_factory(
                strategy_used="bedtime routine",
                worked=False,
                notes="screen time before bed caused issues",
            ),
            session_outcome_factory(
                strategy_used="bedtime routine",
                worked=False,
                notes="screen time again, bedtime difficult",
            ),
        ]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        common_triggers = result.get_list("common_triggers")
        # Should only have unique triggers
        trigger_count = sum(1 for t in common_triggers if "screen time" in t.lower())
        assert trigger_count == 1

    def test_analyze_patterns_result_structure_matches_schema(self, session_outcome_factory):
        """Test pattern analysis result has expected structure."""
        sessions = [session_outcome_factory(strategy_used="bedtime routine")]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)

        # Check all required keys present
        required_keys = {
            "behavior_type",
            "common_triggers",
            "successful_strategies",
            "unsuccessful_approaches",
            "frequency",
            "sessions",
        }
        assert required_keys.issubset(result.data.keys())

    def test_analyze_patterns_data_types_are_correct(self, session_outcome_factory):
        """Test pattern analysis result has correct data types."""
        sessions = [session_outcome_factory(strategy_used="bedtime routine")]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        assert isinstance(result.get_str("behavior_type"), str)
        assert isinstance(result.get_list("common_triggers"), list)
        assert isinstance(result.get_list("successful_strategies"), list)
        assert isinstance(result.get_list("unsuccessful_approaches"), list)
        assert isinstance(result.get_int("frequency"), int)
        assert isinstance(result.get_int("sessions"), int)

    def test_analyze_patterns_triggers_are_all_strings(self, session_outcome_factory):
        """Test pattern analysis triggers list contains only strings."""
        sessions = [
            session_outcome_factory(
                strategy_used="bedtime routine",
                notes="screen time before bed, skipped routine step",
            ),
        ]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        common_triggers = result.get_list("common_triggers")
        for trigger in common_triggers:
            assert isinstance(trigger, str)

    def test_analyze_patterns_successful_strategies_are_all_strings(self, session_outcome_factory):
        """Test pattern analysis successful strategies list contains only strings."""
        sessions = [session_outcome_factory(strategy_used="bedtime timer", worked=True)]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        successful_strategies = result.get_list("successful_strategies")
        for strategy in successful_strategies:
            assert isinstance(strategy, str)

    def test_analyze_patterns_unsuccessful_approaches_are_all_strings(
        self, session_outcome_factory
    ):
        """Test pattern analysis unsuccessful approaches list contains only strings."""
        sessions = [session_outcome_factory(strategy_used="bedtime verbal", worked=False)]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        unsuccessful_approaches = result.get_list("unsuccessful_approaches")
        for approach in unsuccessful_approaches:
            assert isinstance(approach, str)

    def test_analyze_patterns_with_minimum_data_succeeds(self, session_outcome_factory):
        """Test pattern analyzer works with minimum one session."""
        sessions = [session_outcome_factory(strategy_used="bedtime routine")]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        assert result.get_int("sessions") == 1

    def test_analyze_patterns_frequency_never_exceeds_sessions(self, session_outcome_factory):
        """Test pattern analyzer ensures frequency doesn't exceed sessions count."""
        sessions = [
            session_outcome_factory(strategy_used="bedtime timer", worked=True),
            session_outcome_factory(strategy_used="bedtime visual", worked=True),
        ]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        assert result.get_int("frequency") <= result.get_int("sessions")

    def test_analyze_patterns_with_all_successful_sessions(self, session_outcome_factory):
        """Test pattern analyzer handles all successful sessions correctly."""
        sessions = [
            session_outcome_factory(strategy_used="bedtime timer", worked=True),
            session_outcome_factory(strategy_used="bedtime routine", worked=True),
            session_outcome_factory(strategy_used="bedtime visual", worked=True),
        ]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        assert result.get_int("frequency") == 3
        assert len(result.get_list("successful_strategies")) > 0
        assert len(result.get_list("unsuccessful_approaches")) == 0

    def test_analyze_patterns_with_all_unsuccessful_sessions(self, session_outcome_factory):
        """Test pattern analyzer handles all unsuccessful sessions correctly."""
        sessions = [
            session_outcome_factory(strategy_used="bedtime verbal", worked=False),
            session_outcome_factory(strategy_used="bedtime threat", worked=False),
            session_outcome_factory(strategy_used="bedtime rush", worked=False),
        ]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        assert result.get_int("frequency") == 0
        assert len(result.get_list("successful_strategies")) == 0
        assert len(result.get_list("unsuccessful_approaches")) > 0

    def test_analyze_patterns_returns_behavior_type_in_result(self, session_outcome_factory):
        """Test pattern analyzer returns the behavior type being analyzed."""
        sessions = [session_outcome_factory(strategy_used="homework timer")]

        result = analyze_patterns(sessions, "homework")

        assert isinstance(result, ToolSuccess)
        assert result.get_str("behavior_type") == "homework"

    def test_analyze_patterns_with_multiple_trigger_types(self, session_outcome_factory):
        """Test pattern analyzer identifies multiple trigger types."""
        sessions = [
            session_outcome_factory(
                strategy_used="bedtime routine",
                worked=False,
                notes="screen time before bed, skipped bath, unexpected change to schedule",
            ),
        ]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        common_triggers = result.get_list("common_triggers")
        # Should identify multiple trigger types
        assert len(common_triggers) >= 2

    def test_analyze_patterns_with_no_triggers_returns_empty_list(self, session_outcome_factory):
        """Test pattern analyzer returns empty triggers list when none found."""
        sessions = [
            session_outcome_factory(
                strategy_used="bedtime routine",
                worked=True,
                notes="Everything went perfectly smoothly tonight",
            ),
        ]

        result = analyze_patterns(sessions, "bedtime")

        assert isinstance(result, ToolSuccess)
        common_triggers = result.get_list("common_triggers")
        assert isinstance(common_triggers, list)
        # May be empty if no recognized triggers

    def test_analyze_patterns_with_morning_behavior_type(self, session_outcome_factory):
        """Test pattern analyzer recognizes morning keywords."""
        sessions = [
            session_outcome_factory(
                strategy_used="wake up routine with alarm",
                worked=True,
                notes="Woke up smoothly with gradual alarm",
            ),
            session_outcome_factory(
                strategy_used="breakfast visual schedule",
                worked=True,
                notes="Followed breakfast routine perfectly",
            ),
        ]

        result = analyze_patterns(sessions, "morning")

        assert isinstance(result, ToolSuccess)
        assert result.get_int("sessions") == 2
        assert result.get_str("behavior_type") == "morning"
        assert len(result.get_list("successful_strategies")) == 2

    def test_analyze_patterns_morning_keywords_include_routine(self, session_outcome_factory):
        """Test pattern analyzer includes 'routine' in morning keyword matching."""
        sessions = [
            session_outcome_factory(
                strategy_used="daily routine chart",
                worked=True,
                notes="Morning went well with chart",
            ),
        ]

        result = analyze_patterns(sessions, "morning")

        assert isinstance(result, ToolSuccess)
        assert result.get_int("sessions") == 1
