from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.entities import RiskLevel


@dataclass(frozen=True)
class RiskEvaluationContext:
    industry_risk: bool
    keyword_hits_count: int


class RiskScoringStrategy(ABC):
    @abstractmethod
    def score_level(self, context: RiskEvaluationContext) -> RiskLevel:
        """Return a risk level from a normalized evaluation context."""


class RuleBasedRiskScoringStrategy(RiskScoringStrategy):
    def score_level(self, context: RiskEvaluationContext) -> RiskLevel:
        score = (2 if context.industry_risk else 0) + context.keyword_hits_count

        if score == 0:
            return "low"
        if score == 1:
            return "medium"
        return "high"
