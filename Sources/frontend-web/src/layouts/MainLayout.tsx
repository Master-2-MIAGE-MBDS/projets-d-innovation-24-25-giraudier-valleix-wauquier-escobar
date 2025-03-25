import React from 'react';
import Sidebar from '../components/Sidebar';
import { Outlet } from 'react-router-dom';
import './MainLayout.css'; // Nous créerons ce fichier CSS
import Footer from '../components/Footer';

const MainLayout: React.FC = () => {
  return (
    <>
      <div className="main-layout">
        <div className='page-content'>
          {/* side bar empty area */}
          <div></div>
          {/* page content */}
          <Outlet />
        </div>
        <Footer />
      </div>
      {/* relative position sidebar */}
      <Sidebar />
    </>
  );
};

export default MainLayout;