import json

def extract_ats(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return {
            "full_name": data.get("candidate_name"),
            "emails": [data["email"]] if data.get("email") else [],
            "phones": [data["phone"]] if data.get("phone") else [],
            "years_experience": data.get("experience"),
            "skills": data.get("skills", []),
            "_source": "ATS"
        }

    except Exception as e:
        print("ATS Extraction Error:", e)
        return {}