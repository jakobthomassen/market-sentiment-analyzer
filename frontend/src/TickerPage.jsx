import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

const API_BASE_URL = 'http://localhost:8000/api';

function TickerPage() {
  const { tickerSymbol } = useParams(); // Get ticker from URL
  const [details, setDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDetails = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/ticker/${tickerSymbol}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setDetails(data);
      } catch (e) {
        setError('Failed to load ticker details.');
        console.error(e);
      } finally {
        setLoading(false);
      }
    };

    fetchDetails();
  }, [tickerSymbol]);

  if (loading) return <div className="status-message">Loading details for {tickerSymbol}...</div>;
  if (error) return <div className="status-message error">{error}</div>;
  if (!details) return null;

  const quote = details.quote;
  const priceChange = quote.d > 0 ? 'positive' : 'negative';

  return (
    <div className="ticker-details-container">
      <Link to="/" className="back-link">&larr; Back to Report</Link>
      <div className="ticker-header">
        <h1>{details.name} ({details.ticker})</h1>
        <div className="quote-header">
          <span className="current-price">${quote.c.toFixed(2)}</span>
          <span className={`price-change ${priceChange}`}>
            {quote.d.toFixed(2)} ({quote.dp.toFixed(2)}%)
          </span>
        </div>
      </div>

      <div className="financials-grid">
        <div className="metric-box">
          <span className="metric-label">Market Cap</span>
          <span className="metric-value">{details.market_cap ? `${(details.market_cap / 1000).toFixed(2)}B` : 'N/A'}</span>
        </div>
        <div className="metric-box">
          <span className="metric-label">P/E Ratio</span>
          <span className="metric-value">{details.pe_ratio ? details.pe_ratio.toFixed(2) : 'N/A'}</span>
        </div>
        <div className="metric-box">
          <span className="metric-label">Day High</span>
          <span className="metric-value">${quote.h.toFixed(2)}</span>
        </div>
        <div className="metric-box">
          <span className="metric-label">Day Low</span>
          <span className="metric-value">${quote.l.toFixed(2)}</span>
        </div>
      </div>
    </div>
  );
}

export default TickerPage;