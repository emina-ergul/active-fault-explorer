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


### Resources
- <https://github.com/GEMScienceTools/gem-global-active-faults>
- <https://www.atlassian.com/git/tutorials/git-submodule>
- <https://geopandas.org/en/stable/docs/user_guide/io.html>