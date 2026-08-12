import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import stations from "../data/stations.json";

export default function Map() {
  return (
    <MapContainer
      center={[18.5204, 73.8567]}
      zoom={12}
      style={{ height: "100vh", width: "100%" }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {stations.map((station) => (
        <Marker
          key={station.id}
          position={[station.lat, station.lng]}
        >
          <Popup>
            <h3>{station.name}</h3>
            <p>Chargers: {station.chargers}</p>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}