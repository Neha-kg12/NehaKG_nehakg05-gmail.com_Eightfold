from merger.profile_merger import (
    merge_profiles
)

ats = {
    "full_name": "John Doe",
    "skills": []
}

linkedin = {}

profile = merge_profiles(
    ats,
    linkedin
)

assert (
    profile["headline"] is None
)

assert (
    profile["location"] is None
)

print(
    "Missing Source Test Passed"
)