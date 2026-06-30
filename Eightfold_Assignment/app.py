import json
import os

from extractors.ats_extractor import extract_ats
from extractors.linkedin_extractor import extract_linkedin
from normalizers.text_normalizer import normalize_name, normalize_email
from normalizers.phone_normalizer import normalize_phone
from normalizers.skill_normalizer import normalize_skills
from merger.profile_merger import merge_profiles
from projector.output_projector import project_output
from schema.candidate_schema import CandidateProfile


# =========================
# NORMALIZATION
# =========================

def normalize_profile(profile):

    if profile.get("full_name"):
        profile["full_name"] = normalize_name(
            profile["full_name"]
        )

    profile["emails"] = [
        normalize_email(email)
        for email in profile.get("emails", [])
        if email
    ]

    # Save original phones for demo
    profile["_raw_phones"] = profile.get(
        "phones",
        []
    ).copy()

    profile["phones"] = [
        normalize_phone(phone)
        for phone in profile.get("phones", [])
        if normalize_phone(phone)
    ]

    profile["skills"] = normalize_skills(
        profile.get("skills", [])
    )

    return profile
# =========================
# CUSTOM OUTPUT
# =========================

def custom_projection(profile):
    emails = profile.get("emails", [])
    return {
        "candidate_name": profile.get("full_name"),
         "primary_email":
            emails[0] if len(emails) > 0 else None,

        "skills_count":
            len(profile.get("skills", [])),

        "experience":
            profile.get("years_experience"),

        "confidence":
            profile.get("overall_confidence")
    }


# =========================
# PIPELINE
# =========================

def run_pipeline(
    ats_path="input/ats.json",
    linkedin_path="input/linkedin.txt",
    config_path="config/output_config.json"
):

    ats = normalize_profile(extract_ats(ats_path))
    linkedin = normalize_profile(extract_linkedin(linkedin_path))

    canonical = merge_profiles(ats, linkedin)

    CandidateProfile(**canonical)

    projected = project_output(canonical, config_path)
    custom = custom_projection(canonical)

    return canonical, projected, custom


# =========================
# MANUAL PIPELINE
# =========================

def run_manual_pipeline(ats_data, linkedin_data, config_path="config/output_config.json"):
    
    ats = normalize_profile(ats_data)
    
    linkedin = normalize_profile(linkedin_data)

    canonical = merge_profiles(ats, linkedin)

    CandidateProfile(**canonical)

    projected = project_output(canonical, config_path)
    custom = custom_projection(canonical)

    return canonical, projected, custom


# =========================
# SAVE OUTPUTS
# =========================

def save_outputs(canonical, projected):

    os.makedirs("output", exist_ok=True)

    with open("output/canonical.json", "w") as f:
        json.dump(canonical, f, indent=4)

    with open("output/projected.json", "w") as f:
        json.dump(projected, f, indent=4)