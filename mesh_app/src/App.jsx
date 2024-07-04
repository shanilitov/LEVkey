// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ChatComponent from './assets/components/ChatComponent';
import WorldMapComponent from './assets/components/WorldMapComponent';
import backgroundImage from './assets/img/ChatImg.png';

const App = () => {
  return (
    <Router>
      <div className="min-h-screen flex items-center justify-center">
        <div className="absolute inset-0 flex items-center justify-center bg-no-repeat bg-cover" style={{ backgroundImage: `url(${backgroundImage})` }}>
          <div className="w-full max-w-lg bg-gray-900 bg-opacity-75 rounded-lg p-4">
            <Routes>
              <Route path="/ChatComponent" element={<ChatComponent />} />
              <Route path="/WorldMapComponent" element={<WorldMapComponent latitude={34.0522} longitude={-118.2437} />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
};

export default App;
