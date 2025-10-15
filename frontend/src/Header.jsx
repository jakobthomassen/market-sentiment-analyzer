import React from 'react';
import { NavLink } from 'react-router-dom';

function Header() {
  return (
    <header className="app-header">
      <div className="logo">
        <h1>Market Sentiment Analyzer</h1>
      </div>
      <nav className="main-nav">
        <NavLink to="/">Dashboard</NavLink>
        <NavLink to="/about">About</NavLink>
        {/* A placeholder for a future feature */}
        <a href="#" className="disabled-link" onClick={(e) => e.preventDefault()}>Live Feed</a>
      </nav>
    </header>
  );
}

export default Header;