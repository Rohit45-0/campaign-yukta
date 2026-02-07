import React from 'react';
import './Header.css';

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <svg className="logo-icon" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M20 20L50 80L80 20H65L50 55L35 20H20Z" fill="#F7941D"/>
            <path d="M50 35L65 65H35L50 35Z" fill="#1a1a2e"/>
          </svg>
          <span className="logo-text">yukta<span>media</span></span>
        </div>
        <p className="tagline">Deal Document Extractor</p>
      </div>
    </header>
  );
}

export default Header;
