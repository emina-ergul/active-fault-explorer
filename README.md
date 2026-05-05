# active-fault-explorer project overview
This project will be able to analyse and visualise seismic hazard risks using real world data for active faults.

Ideally I want to make it so that you can identify active faults, see historical earthquake data, and estimate risk based on fault proximity and earthquake frequency and magnitude. This will be done using leaflet to craete an interactive map with filters and a heatmap overlay.

Using the GEM foundations global active faults data I will extract the data, create an ETL (extract transform load) pipeline that will convert and clean data as needed and push it to a POSTGIS database. Then create a backend and frontend to query and visualise the data as planned.

## Aims of project:
- Become familiar with basic geopandas
- Aquire appropriate data shapefiles (set up submodule of GEM active fault data)
- Process/transform data in an ETL pipeline
- Set up/understand POSTGIS
- Set up FastAPI backend
- spatial queries
- Become familair with Leaflet
- Create a risk heatmap overlay
- Create a basic frontend
- dockerise

### Learning Points

- Geojson is a text representation of vector data, for spatial data such as shapes lines or boundaries, using coordinates

- Since I will be using Leaflet, I convert the gem geojson data to a standard coordinate system of WGS84 using EPSG4326

- The transform part of an ETL pipeline is to clean the data, by removing duplicates or invalid data

- A point is a geometry that represetns a single location with an x, y and sometimes z value e.g. Point(1, 2). These can be used in spatial queries

- A LineString is a number of Points that connect to represent a feature like roads or rivers from which length can be derived. I will be using Linestrings for faults and Points for earthquakes

- GeodataFrame is like a normal data frame for tabular data but has additional columns for geographical data like crs and points

- POSTGIS usually stores data as Well-Known Binary (WKB) format which stores geometry data as binary strings


### Resources
- <https://github.com/GEMScienceTools/gem-global-active-faults>
- <https://earthquake.usgs.gov/fdsnws/event/1/>
- <https://www.atlassian.com/git/tutorials/git-submodule>
- <https://geopandas.org/en/stable/docs/user_guide/io.html>
- <https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.to_file.html>
- <https://shapely.readthedocs.io/en/2.1.2/reference/shapely.Point.html>
- <https://postgis.net/docs/manual-1.5/ch08.html>
