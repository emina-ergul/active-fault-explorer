from pathlib import Path
from shapely.geometry import Point
import geopandas as gpd
import json

RAW_DIR = Path("backend/data/raw/earthquakes")


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

        gdf = gpd.GeoDataFrame(transformed_data, geometry="geometry", crs="EPSG:4326")

        output_file = Path("backend/data/processed/earthquakes/earthquakes.geojson")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        gdf.to_file(output_file, driver="GeoJSON")
