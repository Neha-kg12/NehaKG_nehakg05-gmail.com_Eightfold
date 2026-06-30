import json

from extractors.ats_extractor import extract_ats
from extractors.linkedin_extractor import extract_linkedin

from merger.profile_merger import merge_profiles


ats = extract_ats("input/ats.json")

linkedin = extract_linkedin(
    "input/linkedin.txt"
)

profile = merge_profiles(
    ats,
    linkedin
)

with open(
    "tests/gold_profile.json"
) as f:

    gold = json.load(f)

assert (
    profile["full_name"]
    == gold["full_name"]
)

assert (
    profile["emails"][0]
    == gold["emails"][0]
)

print("TEST PASSED")