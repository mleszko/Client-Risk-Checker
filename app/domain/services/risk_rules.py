import re
from dataclasses import dataclass

from app.domain.entities import (
    ClientProfile,
    RiskAssessment,
    RiskAssessmentResult,
    RiskReasons,
)
from app.domain.services.scoring_strategy import RiskEvaluationContext, RiskScoringStrategy

HIGH_RISK_KEYWORDS = ["sanctions", "money laundering", "fraud", "pep", "arms", "terror"]
RISKY_INDUSTRIES = ["crypto", "gambling", "weapons"]


def check_industry_risk(industry: str) -> bool:
    return industry.lower() in RISKY_INDUSTRIES


def check_text_risk(description: str) -> list[str]:
    found: list[str] = []
    for keyword in HIGH_RISK_KEYWORDS:
        if re.search(rf"\b{re.escape(keyword)}\b", description.lower()):
            found.append(keyword)
    return found


@dataclass
class RuleBasedRiskEvaluator:
    scoring_strategy: RiskScoringStrategy

    def evaluate(self, client: ClientProfile, full_description: str) -> RiskAssessmentResult:
        industry_risk = check_industry_risk(client.industry)
        keyword_hits = check_text_risk(full_description)
        level = self.scoring_strategy.score_level(
            RiskEvaluationContext(industry_risk=industry_risk, keyword_hits_count=len(keyword_hits))
        )
        assessment = RiskAssessment(
            name=client.name,
            risk_level=level,
            reasons=RiskReasons(
                industry_risk=industry_risk,
                keywords=keyword_hits,
                external_data_used=full_description[:120] + "...",
            ),
        )
        return assessment.to_result()
