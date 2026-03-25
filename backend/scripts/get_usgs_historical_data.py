import json
from pathlib import Path
from datetime import datetime, timedelta
import requests

BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
OUTPUT_DIR = Path("data/raw")


def get_data_year():
    params = {
        "format": "geojson",
        "starttime": (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
        "endtime": datetime.now().strftime("%Y-%m-%d"),
        "minmagnitude": 5.0,
        "orderby": "time",
        "limit": 20000,
    }
    try:
        res = requests.get(BASE_URL, params=params)
        data = res.json()
        with open(OUTPUT_DIR / "usgs_historical_data.json", "w") as f:
            json.dump(data, f)
        return
    except Exception as e:
        print(f"Failed to fetch data: {res.status_code}: {e}")
