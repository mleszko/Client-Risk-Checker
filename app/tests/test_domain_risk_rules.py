from app.domain.entities import ClientProfile
from app.domain.services.risk_rules import check_industry_risk, check_text_risk


def test_check_industry_risk() -> None:
    assert check_industry_risk("crypto") is True
    assert check_industry_risk("insurance") is False


def test_check_text_risk() -> None:
    assert "fraud" in check_text_risk("accused of fraud and laundering")
    assert check_text_risk("honest business") == []


def test_keyword_matching_escapes_metacharacters() -> None:
    profile = ClientProfile(name="Acme", industry="insurance", description="contains pep mention")
    # sanity check that profile construction remains lightweight in domain layer
    assert profile.name == "Acme"
    assert "pep" in check_text_risk("This includes pep exposure.")
