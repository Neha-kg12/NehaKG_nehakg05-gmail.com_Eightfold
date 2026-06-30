def validate(profile):

    return [
        ("Name Valid", bool(profile.get("full_name"))),

        ("Email Exists", len(profile.get("emails", [])) > 0),
        ("Email Format", all("@" in e for e in profile.get("emails", []))),

        ("Phone Format", all(str(p).startswith("+") for p in profile.get("phones", []))),

        ("Skills Present", len(profile.get("skills", [])) > 0),

        ("No Duplicate Skills",
         len(profile.get("skills", [])) ==
         len(set([s["name"] for s in profile.get("skills", [])]))),

        ("Experience Valid", profile.get("years_experience") is not None),

        ("Confidence Range", 0 <= profile.get("overall_confidence", 0) <= 1),
    ]