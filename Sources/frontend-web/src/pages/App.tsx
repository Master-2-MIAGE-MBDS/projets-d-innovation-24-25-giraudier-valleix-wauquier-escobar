import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainLayout from '../layouts/MainLayout';
import Home from '../pages/Home';
import Sign from '../pages/Sign';
import Oscult from '../pages/Oscult';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Home />} />
          <Route path="sign" element={<Sign />} />
          <Route path="oscult" element={<Oscult />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;