from unittest.mock import Mock, patch

import pandas as pd
import pytest

from app.data_sources import fetch_companies_from_csv
from app.infrastructure.company_data import OpenCorporatesCompanyDataProvider


def test_open_corporates_provider_success() -> None:
    provider = OpenCorporatesCompanyDataProvider(api_key="test-token")
    mocked_response = Mock()
    mocked_response.raise_for_status.return_value = None
    mocked_response.json.return_value = {
        "results": {
            "companies": [
                {
                    "company": {
                        "jurisdiction_code": "us_ca",
                        "industry_codes": ["software"],
                        "company_number": "12345",
                        "registered_address": "San Francisco",
                    }
                }
            ]
        }
    }

    with patch("app.infrastructure.company_data.httpx.get", return_value=mocked_response):
        description = provider.fetch_company_description("Acme Corp")

    assert "jurisdiction: us_ca" in description
    assert "company_number: 12345" in description


def test_open_corporates_provider_no_data() -> None:
    provider = OpenCorporatesCompanyDataProvider(api_key="test-token")
    mocked_response = Mock()
    mocked_response.raise_for_status.return_value = None
    mocked_response.json.return_value = {"results": {"companies": []}}

    with patch("app.infrastructure.company_data.httpx.get", return_value=mocked_response):
        description = provider.fetch_company_description("Unknown Corp")

    assert description == "No additional company info found."


def test_open_corporates_provider_error() -> None:
    provider = OpenCorporatesCompanyDataProvider(api_key="test-token")
    with patch(
        "app.infrastructure.company_data.httpx.get",
        side_effect=Exception("request failed"),
    ):
        description = provider.fetch_company_description("Broken Corp")

    assert "Error fetching company data: request failed" in description


def test_fetch_companies_from_csv_success() -> None:
    raw_df = pd.DataFrame({"Company Name": ["Acme Corp"], "Risk Label": ["low"]})

    with patch("app.infrastructure.company_data.pd.read_csv", return_value=raw_df):
        normalized_df = fetch_companies_from_csv("fake/path.csv")

    assert list(normalized_df.columns) == ["company_name", "risk_label"]


def test_fetch_companies_from_csv_error() -> None:
    with patch("app.infrastructure.company_data.pd.read_csv", side_effect=Exception("bad csv")):
        with pytest.raises(RuntimeError, match="Error reading CSV file: bad csv"):
            fetch_companies_from_csv("broken/path.csv")
