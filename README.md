# active-fault-explorer project overview
This project will be able to analyse and visualise seismic hazard risks using real worldwide data for active faults and earthquakes.

Using the GEM foundations global active faults repo, and USGS Earthquake API, I will extract data, create an ETL (extract transform load) pipeline that will convert and clean data as needed and push it to a POSTGIS database. Then create a backend and frontend to query and visualise the data as planned.

Basic flow:
data -> ETL -> PostGIS -> backend spatial queries -> frontend

## Aims of project:
- Become familiar with basic geopandas
- Aquire appropriate data shapefiles (set up submodule of GEM active fault data)
- Process/transform data in an ETL pipeline
- Set up/understand POSTGIS
- Set up FastAPI backend
- Learn about and implement spatial queries
- Become familair with Leaflet
- Create a risk heatmap overlay
- Create a basic frontend
- dockerise

------------------------------------------------------------------------

### Setup

- Clone repo with submodule initialisation
- Create Conda environment and activate
- configure .env
- Run Makefile commands:
    make up
    make setup

- To update the local GEM dataset:
    make gem-update
    make etl

### Database

- Two tables, one for earthqaukes and a table for faults.

- asserting that my database is setup correctly using "docker exec" to execute psql queries in the running container, like  "SELECT COUNT(*) FROM earthquakes" to assert the database filled out.

- Most queries are straightforward but a few require using  PostGIS functions to yield results based on coordinates and distances. I used the function ST_Distance to return all quakes within a certain distance of a fault. Since i wanted distance in km I also used thre geography data type which calculates the distance over a flat 2D plane as opposed to the default WGS 84 reference system SRID 4326 which is mapped to a 3D ellipsoid, and may cause distortion when working out distances near the poles.

### ETL

- The cleaning and formatting of the earthquake data was starightforward and just required me selecting the data I needed such as magnitude, time, depth, and coordinates.
The main thing to check for was that the data fetaure was of type earthquake and had magnitude and coordinate data.

- The cleaning of the fault data was a little less straightforward as I first noticed the data had a lot of NaN values particulary in the slip rate data, so that required cleaaning to 
assert that none of the values were empty strings, strings such as "none", "na", or "nan", or simply missing values.

- Within the data "slip-type" had many options some of which were repeats such as "Sinistral-reverse" and "Reverse-Sinistral", so I had to make sure I accounted for all variants.

### Learning Points

- Geojson is a text representation of vector data for spatial data such as shapes lines or boundaries, using coordinates

- Since I will be using Leaflet, I convert the gem geojson data to a standard coordinate system of WGS84 using EPSG4326, which uses standard latitude and longitude.

- The transform part of an ETL pipeline is to clean the data, by removing duplicates, invalid data or just for general formatting.

- A Point is a geometry that represetns a single location with an x, y and sometimes z value e.g. Point(1, 2). These can be used in spatial queries and in my project will represent earthqaukes.

- A LineString is a number of Points that connect to represent a feature like roads or rivers from which length can be derived. I will be using Linestrings for faults.

- GeodataFrame is like a normal data frame for tabular data but has additional columns for geographical data like crs and points

- PostGIS stores data as geometry to allow for spatial operations






### Resources
- <https://github.com/GEMScienceTools/gem-global-active-faults>
Styron, Richard, and Marco Pagani. “The GEM Global Active Faults Database.” Earthquake Spectra, vol. 36, no. 1_suppl, Oct. 2020, pp. 160–180, doi:10.1177/8755293020944182

- <https://journals.sagepub.com/doi/10.1177/8755293020944182>
- <https://earthquake.usgs.gov/fdsnws/event/1/>
- <https://www.atlassian.com/git/tutorials/git-submodule>
- <https://geopandas.org/en/stable/docs/user_guide/io.html>
- <https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.to_file.html>
- <https://pandas.pydata.org/docs/index.html>
- <https://shapely.readthedocs.io/en/2.1.2/reference/shapely.Point.html>
- <https://postgis.net/docs/manual-1.5/ch08.html>
- <https://www.w3schools.com/sql/sql_join.asp>
- <https://react-leaflet.js.org/>
- <https://leafletjs.com/>
