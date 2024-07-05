import React, { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import worldMapImage from '../img/MapImg..jpg';

const WorldMapComponent = ({ latitude, longitude }) => {
  const mapRef = useRef(null);
  const [locations, setLocations] = useState([]);

  useEffect(() => {
    // Fetch locations from server
    const fetchLocations = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/get_locations');
        if (response.ok) {
          const data = await response.json();
          setLocations(data);
        } else {
          console.error('Failed to fetch locations');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchLocations();

    // Initialize map
    mapRef.current = L.map('map', {
      center: [latitude, longitude], // Initial center of the map
      zoom: 2, // Initial zoom level
      minZoom: 2, // Minimum zoom level
      maxZoom: 18, // Maximum zoom level
    });

    // Add tile layer (base map)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 19,
    }).addTo(mapRef.current);

    return () => {
      // Clean up map instance
      mapRef.current.remove();
    };
  }, [latitude, longitude]);

  useEffect(() => {
    if (mapRef.current && locations.length > 0) {
      locations.forEach(({ latitude, longitude }) => {
        const marker = L.marker([latitude, longitude]).addTo(mapRef.current);
        marker.bindPopup('<b>Device Location</b>').openPopup();
      });
    }
  }, [locations]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-center bg-cover" style={{ backgroundImage: `url(${worldMapImage})` }}>
      <div id="map" className="w-full h-full"></div>
    </div>
  );
};

export default WorldMapComponent;
