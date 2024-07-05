// src/assets/components/WorldMapComponent.jsx
import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import worldMapImage from '../img/world-map-detailed.jpg';

const WorldMapComponent = ({ points }) => {
  const mapRef = useRef(null);

  useEffect(() => {
    // Initialize map
    const w = 3600; // Width of the image
    const h = 1800; // Height of the image
    const southWest = L.latLng(-90, -180);
    const northEast = L.latLng(90, 180);
    const bounds = L.latLngBounds(southWest, northEast);

    mapRef.current = L.map('map', {
      crs: L.CRS.Simple,
      maxBounds: bounds,
      maxZoom: 4,
      minZoom: 1,
      zoom: 2,
      center: [0, 0]
    });

    const imageBounds = [[-90, -180], [90, 180]];
    L.imageOverlay(worldMapImage, imageBounds).addTo(mapRef.current);

    points.forEach(point => {
      const marker = L.marker([point.latitude, point.longitude]).addTo(mapRef.current);
      marker.bindPopup(`<b>${point.name}</b>`);
    });

    return () => {
      mapRef.current.remove();
    };
  }, [points]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div id="map" className="w-full h-full" style={{ height: '500px', width: '100%' }}></div>
    </div>
  );
};

export default WorldMapComponent;
