CREATE TABLE IF NOT EXISTS earthquakes (
    id TEXT PRIMARY KEY,
    magnitude FLOAT,
    place TEXT,
    time TEXT,
    depth FLOAT,
    geometry Geometry(Point, 4326)
);

CREATE TABLE IF NOT EXISTS faults (
    name TEXT,
    slip_type TEXT,
    last_movement TEXT,
    geometry Geometry(LineString, 4326)
);