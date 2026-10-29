import { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  GeoJSON,
  useMapEvents,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";

import { getEarthquakes } from "../services/api";
import { getFaults } from "../services/api";

type Earthquake = {
  id: string;
  magnitude: number;
  place: string;
  time: string;
  depth_km: number;
  geometry: {
    type: "Point";
    coordinates: [number, number];
  };
};

type Fault = {
  id: number;
  catalog_id: string;
  catalog_name: string;
  name: string;
  slip_type: string;
  last_movement: string;
  net_slip_rate_most_likely: number;
  net_slip_rate_min_mm: number;
  net_slip_rate_max_mm: number;
  geometry: {
    type: "LineString";
    coordinates: [number, number][];
  };
};

function HandleMapBoundaries() {
  const map = useMapEvents({
    moveend: () => {
      const bounds = map.getBounds();

      console.log({
        min_lon: bounds.getWest(),
        min_lat: bounds.getSouth(),
        max_lon: bounds.getEast(),
        max_lat: bounds.getNorth(),
      });
    },
  });

  return null;
}

function Map() {
  const [earthquakes, setEarthquakes] = useState<Earthquake[]>([]);
  const [faults, setFaults] = useState<Fault[]>([]);

  useEffect(() => {
    async function fetchEarthquakes() {
      try {
        const data = await getEarthquakes();
        setEarthquakes(data);
      } catch (error) {
        console.error(error);
      }
    }
    async function fetchFaults() {
      try {
        const data = await getFaults();
        setFaults(data);
        console.log("data:", data);
      } catch (error) {
        console.error(error);
      }
    }
    fetchEarthquakes();
    fetchFaults();
  }, []);

  return (
    <MapContainer
      center={[51, 0]}
      zoom={3}
      style={{ height: "600px", width: "100%" }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      
      <HandleMapBoundaries />

      {earthquakes.map((earthquake) => (
        <Marker
          key={earthquake.id}
          position={[
            earthquake.geometry.coordinates[1],
            earthquake.geometry.coordinates[0],
          ]}
        >
          <Popup>
            <strong>{earthquake.place}</strong>
            <br />
            Magnitude: {earthquake.magnitude}
            <br />
            Depth: {earthquake.depth_km} km
            <br />
            Time: {new Date(earthquake.time).toLocaleString()}
          </Popup>
        </Marker>
      ))}

      {faults.map((fault) => (
        <GeoJSON
          key={fault.id}
          data={fault.geometry}
          style={{
            color: "red",
            weight: 2,
          }}
          onEachFeature={(_feature, layer) => {
            layer.bindPopup(`
              <strong>${fault.name ?? "Unnamed fault"}</strong>
              <br />
              Type: ${fault.slip_type?.replace(/_/g, " ") ?? "Unknown"}
              <br />
              Last Movement: ${fault.last_movement ?? "Unknown"}
              <br />
            `);
          }}
        />
      ))}
    </MapContainer>
  );
}

export default Map;
