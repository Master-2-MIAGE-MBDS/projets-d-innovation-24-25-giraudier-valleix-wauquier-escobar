import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import "./Sidebar.css"

//icons
import homeIcon from '../assets/images/nav-icons/Home.svg';
import signIcon from '../assets/images/nav-icons/sign.svg';
import oscultIcon from '../assets/images/nav-icons/oscult.svg';

interface NavItem {
  id: number;
  path: string;
  icon?: string;
}

interface SidebarProps {
  items?: NavItem[];
  className?: string;
}

const defaultNavItems: NavItem[] = [
  {
    id: 1,
    path: '/',
    icon: homeIcon
  },
  {
    id: 2,
    path: '/sign',
    icon: signIcon
  },
  {
    id: 3,
    path: '/oscult',
    icon: oscultIcon
  }
];

const Sidebar: React.FC<SidebarProps> = ({ items = defaultNavItems, className = '' }) => {

    const [activeItem, setActiveItem] = useState<number>(items.find(item => item.path === window.location.pathname)?.id ?? 1);
  
    return (
      <div className={`sidebar-container ${className}`}>
        <nav className={'sidebar'}>
          {items.map((item) => (
              <Link key={item.id}
                to={item.path}
                className={`nav-elem`}
                onClick={() => setActiveItem(item.id)}
              >
                <div className={`tick ${activeItem === item.id ? 'active' : ''}`}></div>
                {item.icon && <div className={'nav-icon-container'}>
                    <img src={item.icon} className="nav-icon"/>
                  </div>}
              </Link>
          ))}
        </nav>
      </div>
    );
  };
  
  export default Sidebar;