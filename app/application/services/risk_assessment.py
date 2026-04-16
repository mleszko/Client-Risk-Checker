from dataclasses import dataclass
from typing import Protocol

from app.domain.entities import ClientProfile, RiskAssessmentResult
from app.domain.services.risk_rules import RuleBasedRiskEvaluator


class CompanyDataProvider(Protocol):
    def fetch_company_description(self, company_name: str) -> str:
        """Fetch additional company context used during risk evaluation."""


@dataclass
class RiskAssessmentService:
    company_data_provider: CompanyDataProvider
    evaluator: RuleBasedRiskEvaluator

    def assess(self, client: ClientProfile) -> RiskAssessmentResult:
        external_description = self.company_data_provider.fetch_company_description(client.name)
        full_description = f"{client.description}. {external_description}"
        return self.evaluator.evaluate(client, full_description)
