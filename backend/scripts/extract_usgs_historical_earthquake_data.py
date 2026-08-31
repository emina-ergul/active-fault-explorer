import json
from pathlib import Path
from datetime import datetime
import requests

api_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
output_dir = Path("backend/data/raw/earthquakes")
output_dir.mkdir(parents=True, exist_ok=True)


def get_data_year():
    for year in range(2024, datetime.now().year):
        params = {
            "format": "geojson",
            "starttime": f"{year}-01-01",
            "endtime": f"{year}-12-31",
            "minmagnitude": 5.0,
            "orderby": "time",
            "limit": 20000,
        }
        try:
            res = requests.get(api_url, params=params)
            res.raise_for_status()
            data = res.json()

            if not data.get("features"):
                print(f"No data found for year {year}")
                continue
            else:
                print(data)
                with open(output_dir / f"{year}_earthquakes.geojson", "w") as f:
                    json.dump(data, f)
        except Exception as e:
            error = f"Failed to fetch data for year {year}: {res.status_code}: {e}"
            raise ValueError(error)


get_data_year()
