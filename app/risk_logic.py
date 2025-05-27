import re
from .models import ClientInfo
from typing import List

HIGH_RISK_KEYWORDS = ["sanctions", "money laundering", "fraud", "PEP", "arms", "terror"]
RISKY_INDUSTRIES = ["crypto", "gambling", "weapons"]

def check_industry_risk(industry: str) -> bool:
    return industry.lower() in RISKY_INDUSTRIES

def check_text_risk(description: str) -> List[str]:
    found = []
    for keyword in HIGH_RISK_KEYWORDS:
        if re.search(rf"\\b{keyword}\\b", description.lower()):
            found.append(keyword)
    return found

def score_client(info: ClientInfo) -> dict:
    external_description = fetch_company_data_from_opencorporates(info.name)
    full_description = f"{info.description}. {external_description}"

    industry_risk = check_industry_risk(info.industry)
    keyword_hits = check_text_risk(full_description)

    score = 0
    if industry_risk:
        score += 2
    score += len(keyword_hits)

    if score == 0:
        level = "low"
    elif score == 1:
        level = "medium"
    else:
        level = "high"

    return {
        "name": info.name,
        "risk_level": level,
        "reasons": {
            "industry_risk": industry_risk,
            "keywords": keyword_hits,
            "external_data_used": external_description[:120] + "..."  # skrót
        }
    }
