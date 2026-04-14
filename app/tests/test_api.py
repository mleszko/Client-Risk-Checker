from dataclasses import dataclass

from fastapi.testclient import TestClient

from app.api.dependencies import get_risk_assessment_service
from app.domain.entities import ClientProfile, RiskAssessmentResult
from app.main import app

client = TestClient(app)


@dataclass
class StubRiskAssessmentService:
    def assess(self, client: ClientProfile) -> RiskAssessmentResult:
        return {
            "name": "Acme Corp",
            "risk_level": "high",
            "reasons": {
                "industry_risk": True,
                "keywords": ["money laundering"],
                "external_data_used": "No additional company info found....",
            },
        }


def test_check_risk() -> None:
    app.dependency_overrides[get_risk_assessment_service] = StubRiskAssessmentService
    response = client.post(
        "/check_risk",
        json={
            "name": "Acme Corp",
            "industry": "crypto",
            "description": "A startup under investigation for money laundering.",
        },
    )
    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] == "high"
