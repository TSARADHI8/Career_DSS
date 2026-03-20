"""
DSS Engine — Career Decision Support Logic
Extracted and upgraded from the original Jupyter notebooks.
"""

def compute_features(skills: str, backlogs: int, projects: int, internships: int) -> dict:
    skill_list = [s.strip() for s in skills.split(",") if s.strip()] if skills else []
    skill_count = len(skill_list)

    if internships >= 2 and projects >= 5:
        experience_level = "High"
    elif internships >= 1 or projects >= 3:
        experience_level = "Medium"
    else:
        experience_level = "Low"

    if backlogs <= 1:
        academic_risk = "Low"
    elif backlogs <= 3:
        academic_risk = "Medium"
    else:
        academic_risk = "High"

    if skill_count >= 3 and experience_level == "High" and academic_risk == "Low":
        placement_readiness = "High"
    elif skill_count >= 2 and academic_risk != "High":
        placement_readiness = "Medium"
    else:
        placement_readiness = "Low"

    return {
        "skill_count": skill_count,
        "experience_level": experience_level,
        "academic_risk": academic_risk,
        "placement_readiness": placement_readiness,
    }


def rule_based_scores(features: dict, higher_studies: bool = False) -> dict:
    pr = features["placement_readiness"]
    exp = features["experience_level"]
    risk = features["academic_risk"]
    sc = features["skill_count"]

    job = 0
    if pr == "High":              job += 2
    if exp in ("High", "Medium"): job += 1
    if risk != "High":            job += 1

    hs = 0
    if higher_studies:            hs += 2
    if risk == "Low":             hs += 1
    if exp in ("High", "Medium"): hs += 1

    skill_imp = 0
    if pr == "Medium":  skill_imp += 2
    if sc < 3:          skill_imp += 1
    if risk != "High":  skill_imp += 1

    wait = 0
    if pr == "Low":     wait += 2
    if risk == "High":  wait += 1

    return {
        "Immediate Job": job,
        "Higher Studies": hs,
        "Skill Improvement": skill_imp,
        "Wait & Improve": wait,
    }


def rank_options(scores: dict) -> list:
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
