import json
from pathlib import Path
from datetime import datetime, timedelta
import requests

BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
OUTPUT_DIR = Path("backend/data/raw/earthquakes")


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
            res = requests.get(BASE_URL, params=params)
            data = res.json()
            print(data)
            with open(OUTPUT_DIR / f"historic_quakes_{year}.geojson", "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Failed to fetch data: {res.status_code}: {e}")


get_data_year()
