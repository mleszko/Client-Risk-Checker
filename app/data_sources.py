import httpx
import os

API_KEY = os.getenv("OPENCORPORATES_API_KEY", "")

def fetch_company_data_from_opencorporates(name: str) -> str:
    url = f"https://api.opencorporates.com/v0.4/companies/search"
    params = {"q": name, "api_token": API_KEY}

    try:
        response = httpx.get(url, params=params, timeout=10)
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
            return ". ".join([p for p in description_parts if p])
        return "No additional company info found."

    except Exception as e:
        return f"Error fetching company data: {str(e)}"
