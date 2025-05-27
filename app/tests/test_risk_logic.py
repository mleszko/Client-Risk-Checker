from app.risk_logic import check_industry_risk, check_text_risk

def test_industry():
    assert check_industry_risk("crypto") is True
    assert check_industry_risk("insurance") is False

def test_text():
    assert "fraud" in check_text_risk("accused of fraud and laundering")
    assert check_text_risk("honest business") == []
