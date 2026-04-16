import pandas as pd

from app.infrastructure.company_data import (
    OpenCorporatesCompanyDataProvider,
)


def fetch_company_data_from_opencorporates(name: str) -> str:
    provider = OpenCorporatesCompanyDataProvider()
    return provider.fetch_company_description(name)


def fetch_companies_from_csv(csv_path: str) -> pd.DataFrame:
    try:
        dataframe = pd.read_csv(csv_path)
        dataframe.columns = [col.strip().lower().replace(" ", "_") for col in dataframe.columns]
        return dataframe
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Error reading CSV file: {exc!s}") from exc