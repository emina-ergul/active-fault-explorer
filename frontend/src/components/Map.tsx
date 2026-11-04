import { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Popup,
  GeoJSON,
  useMapEvents,
  CircleMarker,
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

const slipTypeColors: Record<string, string> = {
  // Strike-slip types (lateral)
  "Strike-Slip": "#5dff57",

  Dextral: "#5dff57",
  Dextral_Transform: "#5dff57",

  Sinistral: "#5dff57",
  Sinistral_Transform: "#5dff57",

  // normal
  Normal: "#4ae4ff",

  // compression types
  Reverse: "#FB923C",
  Thrust: "#FB923C",
  Subduction_Thrust: "#FB923C",

  //oblique slip types
  Oblique: "#f07cff",

  "Dextral-Reverse": "#f07cff",
  "Reverse-Dextral": "#f07cff",
  "Dextral-Normal": "#f07cff",
  "Normal-Dextral": "#f07cff",

  "Sinistral-Normal": "#f07cff",
  "Normal-Sinistral": "#f07cff",
  "Sinistral-Reverse": "#f07cff",
  "Reverse-Sinistral": "#f07cff",

  "Reverse-Strike-Slip": "#f07cff",
  "Normal-Strike-Slip": "#f07cff",

  // spreading ridge boundary
  Spreading_Ridge: "#ff6464",

  //Folds
  Anticline: "#FBdb24",
  Syncline: "#fbdb24",
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
      className="map-container"
      center={[51, 0]}
      zoom={3}
      style={{ height: "600px", width: "100%" }}
    >
      <TileLayer
      className="map-tiles"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <HandleMapBoundaries />

      {earthquakes.map((earthquake) => (
        <CircleMarker
          key={earthquake.id}
          center={[
            earthquake.geometry.coordinates[1],
            earthquake.geometry.coordinates[0],
          ]}
          radius={earthquake.magnitude * 2}
          color="#ec3f18"
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
        </CircleMarker>
      ))}

      {faults.map((fault) => (
        <GeoJSON
          key={fault.id}
          data={fault.geometry}
          style={{
            color: slipTypeColors[fault.slip_type] || "#6e6f72",
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
