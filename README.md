# active-fault-explorer project overview
This project will be able to analyse and visualise seismic hazard risks using real world data for active faults.

Ideally I want to make it so that you can identify active faults, see historical earthquake data, and estimate risk based on fault proximity and earthquake frequency and magnitude. This will be done using leaflet to craete an interactive map with filters and a heatmap overlay.

Using the GEM foundations global active faults data I will extract the data, create an ETL (extract transform load) pipeline that will convert and clean data as needed and push it to a POSTGIS database. Then create a backend and front end to query and visualise the data as planned.

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

- Since I will be using Leaflet, I convert the gem geojson data to a standard coordinate system of WGS84

- difference between WSG84 and EPSG4326: WSG is 3D data for defining the earths shape, EPSG is used to define coordinate systems

- The transform part of an ETL pipeline is to clean the data, by removing duplicates or invalid data

- A point is a geometry that represetns a single coordinate with an x, y and sometimes z value e.g. Point(1, 2). These can be used in spatial queries

- GeodataFrame is like a normal data frame for tabular data but has additional columns for geographical data like crs and points


### Resources
- <https://github.com/GEMScienceTools/gem-global-active-faults>
- <https://earthquake.usgs.gov/fdsnws/event/1/>
- <https://www.atlassian.com/git/tutorials/git-submodule>
- <https://geopandas.org/en/stable/docs/user_guide/io.html>
- <https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.to_file.html>
- <https://shapely.readthedocs.io/en/2.1.2/reference/shapely.Point.html>
