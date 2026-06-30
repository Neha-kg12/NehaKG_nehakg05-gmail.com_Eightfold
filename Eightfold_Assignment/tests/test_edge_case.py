from merger.profile_merger import (
    merge_profiles
)

ats = {
    "full_name": "John Doe",
    "emails": [],
    "phones": [],
    "skills": []
}

linkedin = {}

profile = merge_profiles(
    ats,
    linkedin
)

assert (
    profile["headline"]
    is None
)

assert (
    profile["location"]
    is None
)

print("EDGE CASE PASSED")