from pathlib import Path
import json
from shapely.geometry import Point

RAW_DIR = Path("backend/data/raw/earthquakes")
OUTPUT_DIR = Path("backend/data/processed/earthquakes")


def transform_earthquake_data():
    transformed_data = []
    files = list(RAW_DIR.glob("historic_quakes_*.geojson"))

    for file in files:
        with open(file) as f:
            data = json.load(f)

        features = data.get("features", [])

        for feature in features:
            # print(feature)
            properties = feature.get("properties", {})
            geometry = feature.get("geometry", {})
            coordinates = geometry.get("coordinates", None)

            # print(coordinates)

            if not coordinates or properties.get("mag") is None:
                continue

            if properties.get("type") == "earthquake":

                lon, lat, depth = coordinates

                row = {
                    "id": feature.get("id"),
                    "magnitude": properties.get("mag"),
                    "place": properties.get("place"),
                    "time": properties.get("time"),
                    "depth": depth,
                    "geometry": Point(lon, lat),
                }
                print(row)
                transformed_data.append(row)


transform_earthquake_data()
