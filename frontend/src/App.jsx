import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';
import Report from './Report';
import TickerPage from './TickerPage';
import AboutPage from './AboutPage';

function App() {
  return (
    <div className="app-layout">
      <Header />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Report />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/ticker/:tickerSymbol" element={<TickerPage />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default App;