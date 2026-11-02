from database.init_db import engine
import geopandas as gpd
import shapely


def load_earthquake_data():
    gdf = gpd.read_file("data/processed/earthquakes/earthquakes.geojson")
    gdf = gdf.to_crs(4326)
    print("Loading earthquake data into PostGIS...")
    gdf.to_postgis(name="earthquakes", con=engine, if_exists="replace", index=False)


def load_fault_data():
    gdf = gpd.read_file("data/processed/faults/faults.geojson")
    gdf = gdf.to_crs(4326)

    gdf["geometry"] = gdf["geometry"].apply(
        lambda geom: shapely.force_2d(geom) if geom is not None else None
    )  # this function makes the geomrtry 2d by removing the z coordinate

    print("Loading fault data into PostGIS...")
    gdf.to_postgis(
        name="faults",
        con=engine,
        if_exists="replace",
        index=False,
    )
