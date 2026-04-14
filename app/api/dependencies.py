from app.application.services.risk_assessment import RiskAssessmentService
from app.domain.services.risk_rules import RuleBasedRiskEvaluator
from app.domain.services.scoring_strategy import RuleBasedRiskScoringStrategy
from app.infrastructure.company_data import OpenCorporatesCompanyDataProvider


def get_risk_assessment_service() -> RiskAssessmentService:
    evaluator = RuleBasedRiskEvaluator(scoring_strategy=RuleBasedRiskScoringStrategy())
    return RiskAssessmentService(
        company_data_provider=OpenCorporatesCompanyDataProvider(),
        evaluator=evaluator,
    )
