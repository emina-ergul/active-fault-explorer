from pathlib import Path
import geopandas as gpd

try:
    OUTPUT_DIR = Path("backend/data/raw/faults")
    gem_data = gpd.read_file("backend/data/gem/geojson/gem_active_faults.geojson")
    gem_data = gem_data.to_crs(epsg=4326)

    print(gem_data.head())
    print(gem_data.geometry[0])

    print(gem_data.columns)
    print(gem_data.crs)
    print(gem_data.geom_type.value_counts())

    gem_data.to_file(OUTPUT_DIR / "gem_faults.geojson", driver="GeoJSON")
except Exception as e:
    print(f"Error loading GEM data: {e}")
