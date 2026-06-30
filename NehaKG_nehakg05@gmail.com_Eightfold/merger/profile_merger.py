SOURCE_CONFIDENCE = {
    "ATS": 0.95,
    "LinkedIn": 0.85
}


# =====================================================
# DYNAMIC CONFIDENCE
# =====================================================

def compute_confidence(profile):

    scores = []

    provenance = profile.get(
        "provenance",
        {}
    )

    for field_info in provenance.values():

        if isinstance(field_info, dict):

            scores.append(
                field_info.get(
                    "confidence",
                    0
                )
            )

    if not scores:
        return 0.0

    return round(
        sum(scores) / len(scores),
        2
    )


# =====================================================
# MERGE
# =====================================================

def merge_profiles(ats, linkedin):

    profile = {}
    provenance = {}

    profile["candidate_id"] = "C001"

    profile["links"] = []
    profile["experience"] = []
    profile["education"] = []

    # =================================================
    # FULL NAME
    # =================================================

    profile["full_name"] = (
        ats.get("full_name")
        or linkedin.get("full_name")
    )

    if ats.get("full_name"):

        provenance["full_name"] = {
            "source": "ATS",
            "method": "preferred_source",
            "confidence": 0.95
        }

    elif linkedin.get("full_name"):

        provenance["full_name"] = {
            "source": "LinkedIn",
            "method": "fallback_source",
            "confidence": 0.85
        }

    # =================================================
    # EMAILS
    # =================================================

    profile["emails"] = (
        ats.get("emails")
        or linkedin.get("emails")
        or []
    )

    if ats.get("emails"):

        provenance["emails"] = {
            "source": "ATS",
            "method": "direct",
            "confidence": 0.95
        }

    elif linkedin.get("emails"):

        provenance["emails"] = {
            "source": "LinkedIn",
            "method": "fallback_source",
            "confidence": 0.85
        }

    # =================================================
    # PHONES
    # =================================================

    profile["phones"] = (
        ats.get("phones")
        or linkedin.get("phones")
        or []
    )

    profile["_raw_phones"] = (
        ats.get("_raw_phones")
        or linkedin.get("_raw_phones")
        or []
    )

    if profile["phones"]:

        provenance["phones"] = {
            "source": "ATS",
            "method": "normalized",
            "confidence": 0.95
        }

    # =================================================
    # HEADLINE
    # =================================================

    profile["headline"] = (
        linkedin.get("headline")
        or ""
    )

    if profile["headline"]:

        provenance["headline"] = {
            "source": "LinkedIn",
            "method": "direct",
            "confidence": 0.85
        }

    # =================================================
    # LOCATION
    # =================================================

    profile["location"] = (
        linkedin.get("location")
        or ""
    )

    if profile["location"]:

        provenance["location"] = {
            "source": "LinkedIn",
            "method": "direct",
            "confidence": 0.85
        }

    # =================================================
    # EXPERIENCE
    # =================================================

    ats_exp = ats.get(
        "years_experience"
    )

    linkedin_exp = linkedin.get(
        "years_experience"
    )

    if ats_exp is not None and ats_exp > 0:

        profile["years_experience"] = ats_exp

        provenance["years_experience"] = {
            "source": "ATS",
            "method": "preferred_source",
            "confidence": 0.95
        }

    elif linkedin_exp is not None and linkedin_exp > 0:

        profile["years_experience"] = linkedin_exp

        provenance["years_experience"] = {
            "source": "LinkedIn",
            "method": "fallback_source",
            "confidence": 0.85
        }

    else:

        profile["years_experience"] = 0

    # =================================================
    # SKILLS
    # =================================================

    ats_skills = ats.get(
        "skills",
        []
    )

    linkedin_skills = linkedin.get(
        "skills",
        []
    )

    merged_skills = []

    for skill in ats_skills + linkedin_skills:

        if not skill:
            continue

        if skill.lower() not in [
            s.lower()
            for s in merged_skills
        ]:

            merged_skills.append(
                skill
            )

    profile["skills"] = []

    for skill in merged_skills:

        sources = []

        if any(
            skill.lower() == s.lower()
            for s in ats_skills
        ):
            sources.append("ATS")

        if any(
            skill.lower() == s.lower()
            for s in linkedin_skills
        ):
            sources.append("LinkedIn")

        profile["skills"].append({

            "name": skill,

            "confidence": 0.90,

            "sources": sources
        })

    provenance["skills"] = {

        "source": "ATS + LinkedIn",

        "method": "merged",

        "confidence": 0.90,

        "ats_skill_count": len(
            ats_skills
        ),

        "linkedin_skill_count": len(
            linkedin_skills
        )
    }

    # =================================================
    # PROVENANCE
    # =================================================

    profile["provenance"] = provenance

    # =================================================
    # OVERALL CONFIDENCE
    # =================================================

    profile["overall_confidence"] = (
        compute_confidence(
            profile
        )
    )

    return profile