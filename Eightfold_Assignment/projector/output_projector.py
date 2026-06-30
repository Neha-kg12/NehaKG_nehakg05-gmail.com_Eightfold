import json


def get_nested(data, key):

    if key.endswith("[0]"):

        base = key.replace("[0]", "")

        values = data.get(base, [])

        return values[0] if values else None

    return data.get(key)


def project_output(profile, config_path):

    with open(config_path, "r") as f:
        config = json.load(f)
    if "fields" not in config:

        raise ValueError(
            "Invalid config file"
    )

    result = {}

    for field in config["fields"]:

        target = field["path"]

        source = field["from"]

        result[target] = get_nested(
            profile,
            source
        )

    if config.get("include_confidence"):
        result["overall_confidence"] = profile.get(
            "overall_confidence"
        )

    if config.get("include_provenance"):
        result["provenance"] = profile.get(
            "provenance"
        )

    return result