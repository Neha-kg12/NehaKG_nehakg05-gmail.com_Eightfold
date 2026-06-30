SKILL_MAP = {
    "python": "Python",
    "py": "Python",
    "pyhton": "Python",     # typo fix
    "sql": "SQL",
    "mysql": "SQL",
    "aws": "AWS",
    "java": "Java"
}


def normalize_skill(skill):

    if not skill:
        return None

    cleaned = skill.strip().lower()

    return SKILL_MAP.get(
        cleaned,
        skill.strip().title()
    )


def normalize_skills(skills):

    normalized = []

    seen = set()

    for skill in skills:

        value = normalize_skill(skill)

        if value and value.lower() not in seen:

            normalized.append(value)

            seen.add(
                value.lower()
            )

    return normalized