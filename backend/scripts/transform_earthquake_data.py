from pathlib import Path
from datetime import datetime
from shapely.geometry import Point
import geopandas as gpd
import json

raw_dir = Path("backend/data/raw/earthquakes/")
raw_dir.parent.mkdir(parents=True, exist_ok=True)


def transform_earthquake_data():
    transformed_data = []
    files = list(raw_dir.glob("*_earthquakes.geojson"))

    for file in files:
        with open(file) as f:
            data = json.load(f)

        features = data.get("features", [])

        for feature in features:
            properties = feature.get("properties", {})
            geometry = feature.get("geometry", {})
            coordinates = geometry.get("coordinates", None)

            if properties.get("type") != "earthquake":
                continue

            if not coordinates or properties.get("mag") is None:
                continue

            if properties.get("time") is None:
                continue

            lon, lat, depth = coordinates

            row = {
                "id": feature.get("id"),
                "magnitude": properties.get("mag"),
                "place": properties.get("place"),
                "time": datetime.fromtimestamp(properties.get("time") / 1000),
                "depth_km": depth,
                "geometry": Point(lon, lat),
            }
            transformed_data.append(row)

        gdf = gpd.GeoDataFrame(transformed_data, geometry="geometry", crs="EPSG:4326")

        output_file = Path("backend/data/processed/earthquakes/earthquakes.geojson")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        gdf.to_file(output_file, driver="GeoJSON")


transform_earthquake_data()
