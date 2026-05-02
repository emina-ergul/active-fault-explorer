from database.init_db import engine
import geopandas as gpd


def load_earthquakes():
    gdf = gpd.read_file("backend/data/processed/earthquakes/earthquakes.geojson")
    gdf = gdf.to_crs(4326)
    gdf.to_postgis(name="earthquakes", con=engine, if_exists="append")


def load_faults():
    gdf = gpd.read_file("backend/data/raw/faults/faults.geojson")
    gdf = gdf.to_crs(4326)
    gdf.to_postgis(name="faults", con=engine, if_exists="append")


if __name__ == "__main__":
    load_earthquakes()
    load_faults()
