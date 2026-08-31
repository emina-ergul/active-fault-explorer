from backend.database.init_db import engine
import geopandas as gpd
import shapely


def load_earthquakes():
    gdf = gpd.read_file("backend/data/processed/earthquakes/earthquakes.geojson")
    gdf = gdf.to_crs(4326)
    gdf.to_postgis(name="earthquakes", con=engine, if_exists="append")


def load_faults():
    gdf = gpd.read_file("backend/data/processed/faults/faults.geojson")
    gdf = gdf.to_crs(4326)

    gdf["geometry"] = gdf["geometry"].apply(
        lambda g: shapely.force_2d(g) if g is not None else None
    )  # this function makes the geomrtry 2d by removing the z coordinate because i already have depth field

    gdf.to_postgis(name="faults", con=engine, if_exists="append")


if __name__ == "__main__":
    load_earthquakes()
    load_faults()
