import re

def extract_linkedin(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        profile = {
            "full_name": None,
            "headline": None,
            "location": None,
            "skills": [],
            "years_experience": None,
            "_source": "LinkedIn"
        }

        if len(lines) > 0:
            profile["full_name"] = lines[0]

        if len(lines) > 1:
            profile["headline"] = lines[1]

        location_match = re.search(r"Location:\s*(.*)", text)
        if location_match:
            profile["location"] = location_match.group(1)

        skills_match = re.search(r"Skills:\s*(.*)", text)
        if skills_match:
            profile["skills"] = [
                s.strip()
                for s in skills_match.group(1).split(",")
            ]

        exp_match = re.search(r"Experience:\s*(\d+)", text)
        if exp_match:
            profile["years_experience"] = int(exp_match.group(1))

        return profile

    except Exception as e:
        print("LinkedIn Extraction Error:", e)
        return {}