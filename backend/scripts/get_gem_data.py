import geopandas as gpd

gem_data = gpd.read_file("backend/data/gem/geojson/gem_active_faults.geojson")
gem_data = gem_data.to_crs(epsg=4326)

print(gem_data.head())
print(gem_data.geometry[0])

print(gem_data.columns)
print(gem_data.crs)
print(gem_data.geom_type.value_counts())
