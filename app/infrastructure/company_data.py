import os

import httpx
import pandas as pd


class OpenCorporatesCompanyDataProvider:
    def __init__(self, api_key: str | None = None, timeout: int = 10) -> None:
        self._api_key = api_key if api_key is not None else os.getenv("OPENCORPORATES_API_KEY", "")
        self._timeout = timeout

    def fetch_company_description(self, name: str) -> str:
        url = "https://api.opencorporates.com/v0.4/companies/search"
        params = {"q": name, "api_token": self._api_key}

        try:
            response = httpx.get(url, params=params, timeout=self._timeout)
            response.raise_for_status()
            data = response.json()

            companies = data.get("results", {}).get("companies", [])
            if companies:
                company = companies[0].get("company", {})
                description_parts = [
                    f"jurisdiction: {company.get('jurisdiction_code')}",
                    f"industry_codes: {company.get('industry_codes')}",
                    f"company_number: {company.get('company_number')}",
                    f"registered_address: {company.get('registered_address')}",
                ]
                return ". ".join([part for part in description_parts if part])
            return "No additional company info found."
        except Exception as exc:  # noqa: BLE001
            return f"Error fetching company data: {exc!s}"


def fetch_companies_from_csv(csv_path: str) -> pd.DataFrame:
    try:
        dataframe = pd.read_csv(csv_path)
        dataframe.columns = [col.strip().lower().replace(" ", "_") for col in dataframe.columns]
        return dataframe
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Error reading CSV file: {exc!s}") from exc
