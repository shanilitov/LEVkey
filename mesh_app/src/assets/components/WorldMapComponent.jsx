// // src/assets/components/WorldMapComponent.jsx
// import React, { useEffect, useRef } from 'react';
// import L from 'leaflet';
// import 'leaflet/dist/leaflet.css';
// import worldMapImage from '../img/MapImg..jpg';

// const WorldMapComponent = ({ latitude, longitude }) => {
//   const mapRef = useRef(null);

//   useEffect(() => {
//     // Initialize map
//     mapRef.current = L.map('map', {
//       center: [latitude, longitude], // Initial center of the map
//       zoom: 2, // Initial zoom level
//       minZoom: 2, // Minimum zoom level
//       maxZoom: 18, // Maximum zoom level
//     });

//     // Add tile layer (base map)
//     L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//       attribution: '&copy; OpenStreetMap contributors',
//       maxZoom: 19,
//     }).addTo(mapRef.current);

//     // Add marker based on provided latitude and longitude
//     if (latitude && longitude) {
//       const marker = L.marker([latitude, longitude]).addTo(mapRef.current);
//       marker.bindPopup('<b>Your Location</b>').openPopup();
//     }

//     return () => {
//       // Clean up map instance
//       mapRef.current.remove();
//     };
//   }, [latitude, longitude]);

//   return (
//     <div className="min-h-screen flex items-center justify-center bg-center bg-cover" style={{ backgroundImage: `url(${worldMapImage})` }}>
//       <div id="map" className="w-full h-full"></div>
//     </div>
//   );
// };

// export default WorldMapComponent;
// src/assets/components/WorldMapComponent.jsx
import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import worldMapImage from '../img/MapImg.jpg';

const WorldMapComponent = ({ points }) => {
  const mapRef = useRef(null);

  useEffect(() => {
    // Initialize map
    mapRef.current = L.map('map', {
      center: [0, 0], // Initial center of the map
      zoom: 2, // Initial zoom level
      minZoom: 2, // Minimum zoom level
      maxZoom: 18, // Maximum zoom level
    });

    // Add local tile layer (base map)
    L.tileLayer('/tiles/{z}/{x}/{y}.png', {
      maxZoom: 19,
    }).addTo(mapRef.current);

    // Add markers based on provided points
    points.forEach(point => {
      const marker = L.marker([point.latitude, point.longitude]).addTo(mapRef.current);
      marker.bindPopup(`<b>${point.name}</b>`).openPopup();
    });

    return () => {
      // Clean up map instance
      mapRef.current.remove();
    };
  }, [points]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-center bg-cover" style={{ backgroundImage: `url(${worldMapImage})` }}>
      <div id="map" className="w-full h-full" style={{ height: '500px', width: '100%' }}></div>
    </div>
  );
};

export default WorldMapComponent;
