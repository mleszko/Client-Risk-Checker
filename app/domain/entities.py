from dataclasses import dataclass
from typing import Literal, TypedDict

RiskLevel = Literal["low", "medium", "high"]


class RiskReasonsResult(TypedDict):
    industry_risk: bool
    keywords: list[str]
    external_data_used: str


class RiskAssessmentResult(TypedDict):
    name: str
    risk_level: RiskLevel
    reasons: RiskReasonsResult


@dataclass(frozen=True)
class ClientProfile:
    name: str
    industry: str
    description: str


@dataclass(frozen=True)
class RiskReasons:
    industry_risk: bool
    keywords: list[str]
    external_data_used: str


@dataclass(frozen=True)
class RiskAssessment:
    name: str
    risk_level: RiskLevel
    reasons: RiskReasons

    def to_result(self) -> RiskAssessmentResult:
        return {
            "name": self.name,
            "risk_level": self.risk_level,
            "reasons": {
                "industry_risk": self.reasons.industry_risk,
                "keywords": self.reasons.keywords,
                "external_data_used": self.reasons.external_data_used,
            },
        }
