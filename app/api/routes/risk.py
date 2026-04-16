from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_risk_assessment_service
from app.application.services.risk_assessment import RiskAssessmentService
from app.domain.entities import ClientProfile, RiskAssessmentResult
from app.models import ClientInfo

router = APIRouter()


@router.post("/check_risk")
def check_risk(
    client: ClientInfo,
    service: Annotated[RiskAssessmentService, Depends(get_risk_assessment_service)],
) -> RiskAssessmentResult:
    profile = ClientProfile(
        name=client.name,
        industry=client.industry,
        description=client.description,
    )
    return service.assess(profile)
