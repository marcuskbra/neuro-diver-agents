"""Output formatters for tool results - type-safe formatting functions."""


def format_behavior_analysis(data: dict[str, str | int | float | bool | list[str]]) -> str:
    """
    Format behavior analysis result into human-readable string.

    Args:
        data: Tool result data containing primary_driver and factor lists.

    Returns:
        Formatted string describing the behavior analysis.
    """
    factors = []

    adhd_factors = data.get("adhd_factors")
    if adhd_factors and isinstance(adhd_factors, list):
        factors.append(f"ADHD: {', '.join(str(f) for f in adhd_factors)}")

    asd_factors = data.get("asd_factors")
    if asd_factors and isinstance(asd_factors, list):
        factors.append(f"ASD: {', '.join(str(f) for f in asd_factors)}")

    age_factors = data.get("age_typical_factors")
    if age_factors and isinstance(age_factors, list):
        factors.append(f"Age-typical: {', '.join(str(f) for f in age_factors)}")

    return f"Primary driver: {data['primary_driver']}\nFactors:\n" + "\n".join(factors)


def format_activity_plan(data: dict[str, str | int | float | bool | list[str]]) -> str:
    """
    Format activity plan result into human-readable string.

    Args:
        data: Tool result data containing activity plan details.

    Returns:
        Formatted string describing the activity plan.
    """
    output = [
        f"Activity: {data['name']}",
        f"Goal: {data['goal']}",
        f"Duration: {data['duration_minutes']} minutes",
    ]

    materials = data.get("materials")
    if materials and isinstance(materials, list):
        output.append(f"\nMaterials needed: {', '.join(str(m) for m in materials)}")

    output.append(f"\nEnvironmental setup: {data['environmental_setup']}")
    output.append("\nStructure:")

    structure = data.get("structure")
    if structure and isinstance(structure, list):
        for step in structure:
            output.append(f"  - {step}")

    output.append("\nSuccess criteria:")
    criteria = data.get("success_criteria")
    if criteria and isinstance(criteria, list):
        for criterion in criteria:
            output.append(f"  - {criterion}")

    adaptations = data.get("adaptations")
    if adaptations and isinstance(adaptations, list):
        output.append("\nAdaptations:")
        for adaptation in adaptations:
            output.append(f"  - {adaptation}")

    return "\n".join(output)


def format_pattern_analysis(data: dict[str, str | int | float | bool | list[str]]) -> str:
    """
    Format pattern analysis result into human-readable string.

    Args:
        data: Tool result data containing pattern analysis details.

    Returns:
        Formatted string describing the pattern analysis.
    """
    output = [
        f"Behavior: {data['behavior_type']}",
        f"Sessions analyzed: {data['sessions']}",
        f"Success rate: {data['frequency']}/{data['sessions']}",
    ]

    triggers = data.get("common_triggers")
    if triggers and isinstance(triggers, list):
        output.append(f"\nCommon triggers: {', '.join(str(t) for t in triggers)}")

    strategies = data.get("successful_strategies")
    if strategies and isinstance(strategies, list):
        output.append(f"\nSuccessful strategies: {', '.join(str(s) for s in strategies)}")

    unsuccessful = data.get("unsuccessful_approaches")
    if unsuccessful and isinstance(unsuccessful, list):
        output.append(f"\nUnsuccessful approaches: {', '.join(str(a) for a in unsuccessful)}")

    return "\n".join(output)
