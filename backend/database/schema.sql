CREATE TABLE IF NOT EXISTS earthquakes (
    id TEXT PRIMARY KEY,
    magnitude FLOAT,
    place TEXT,
    time TEXT,
    depth FLOAT,
    geometry Geometry(Point, 4326)
);

CREATE TABLE IF NOT EXISTS faults (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    catalog_id TEXT,
    catalog_name TEXT,
    name TEXT,
    slip_type TEXT,
    last_movement TEXT,
    net_slip_rate_most_likely_mm FLOAT,
    net_slip_rate_min_mm FLOAT,
    net_slip_rate_max_mm FLOAT,
    geometry Geometry(LineString, 4326)
);