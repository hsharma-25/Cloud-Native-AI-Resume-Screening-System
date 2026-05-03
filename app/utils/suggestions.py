def generate_suggestions(missing_skills):

    suggestions = []

    # Management-related
    management_skills = [
        "project management",
        "performance management",
        "leadership",
        "organizational development",
        "time management"
    ]

    # HR-related
    hr_skills = [
        "human resources",
        "recruitment",
        "employee relations"
    ]

    # Technical / tools
    tool_skills = [
        "excel",
        "power bi",
        "tableau",
        "sql",
        "python"
    ]

    # Communication
    soft_skills = [
        "communication",
        "critical thinking",
        "problem solving"
    ]

    # Group detection
    if any(skill in missing_skills for skill in management_skills):
        suggestions.append(
            "Highlight leadership, coordination, or management-related responsibilities."
        )

    if any(skill in missing_skills for skill in hr_skills):
        suggestions.append(
            "Include more HR operations, recruitment, or employee engagement experience."
        )

    if any(skill in missing_skills for skill in tool_skills):
        suggestions.append(
            "Mention relevant technical tools, analytics platforms, or software experience."
        )

    if any(skill in missing_skills for skill in soft_skills):
        suggestions.append(
            "Demonstrate communication, teamwork, or problem-solving abilities through projects or experience."
        )

    # Generic fallback
    if not suggestions:
        suggestions.append(
            "Consider aligning your resume more closely with the job description requirements."
        )

    return suggestions