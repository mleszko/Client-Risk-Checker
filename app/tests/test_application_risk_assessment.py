from app.application.services.risk_assessment import RiskAssessmentService
from app.domain.entities import ClientProfile
from app.domain.services.risk_rules import RuleBasedRiskEvaluator
from app.domain.services.scoring_strategy import RuleBasedRiskScoringStrategy


class StubCompanyDataProvider:
    def fetch_company_description(self, company_name: str) -> str:
        return "jurisdiction: us_ca. notes: no flags"


def test_risk_assessment_service_uses_provider_and_evaluator() -> None:
    service = RiskAssessmentService(
        company_data_provider=StubCompanyDataProvider(),
        evaluator=RuleBasedRiskEvaluator(scoring_strategy=RuleBasedRiskScoringStrategy()),
    )

    result = service.assess(
        ClientProfile(
            name="Acme Corp",
            industry="crypto",
            description="Under investigation for fraud activity",
        )
    )

    assert result["name"] == "Acme Corp"
    assert result["risk_level"] == "high"
    assert result["reasons"]["industry_risk"] is True
    assert "fraud" in result["reasons"]["keywords"]
