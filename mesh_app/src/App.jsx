// export default App;

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ChatComponent from './assets/components/map/ChatComponent';
import WorldMapComponent from './assets/components/map/WorldMapComponent';
import backgroundImage from './assets/components/map/map.png';

const App = () => {
  // Define some example points
  const points = [
    { latitude: 31.7683, longitude: 35.2137, name: 'ירושלים' },
    { latitude: 40.7128, longitude: -74.0060, name: 'ניו יורק' },
    { latitude: 48.8566, longitude: 2.3522, name: 'פריז' },
  ];

  return (
    <Router>
      <div className="min-h-screen flex items-center justify-center">
        <div className="absolute inset-0 flex items-center justify-center bg-no-repeat bg-cover" style={{ backgroundImage: `url(${backgroundImage})` }}>
          <div className="w-full max-w-lg bg-gray-900 bg-opacity-75 rounded-lg p-4">
            <Routes>
              <Route path="/ChatComponent" element={<ChatComponent />} />
              <Route path="/WorldMapComponent" element={<WorldMapComponent points={points} />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
};

export default App;
