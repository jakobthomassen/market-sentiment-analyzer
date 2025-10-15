import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// The URL where our FastAPI backend is running.
const API_BASE_URL = 'http://localhost:8000/api';

function Report() {
  const [reportData, setReportData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // State for UI controls
  const [subreddits, setSubreddits] = useState([]);
  const [selectedSubreddit, setSelectedSubreddit] = useState('');
  const [sortBy, setSortBy] = useState('mentions');
  const [order, setOrder] = useState('desc');

  useEffect(() => {
    // Fetch the list of available subreddits for the filter dropdown
    const fetchSubreddits = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/subreddits`);
        const data = await response.json();
        setSubreddits(data);
      } catch (e) {
        console.error("Failed to fetch subreddits:", e);
      }
    };

    fetchSubreddits();
  }, []);

  useEffect(() => {
    const fetchReportData = async () => {
      setLoading(true);
      setError(null);

      // Build the URL with query parameters
      const params = new URLSearchParams({
        sort_by: sortBy,
        order: order,
      });
      if (selectedSubreddit) {
        params.append('subreddit', selectedSubreddit);
      }

      const url = `${API_BASE_URL}/report?${params.toString()}`;

      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setReportData(data);
      } catch (e) {
        console.error("Failed to fetch report data:", e);
        setError("Failed to load data. Is the backend server running?");
      } finally {
        setLoading(false); // This runs whether the fetch succeeded or failed.
      }
    };

    fetchReportData();
  }, [selectedSubreddit, sortBy, order]); // Re-run this effect when any of these values change

  const handleRowClick = (ticker) => {
    navigate(`/ticker/${ticker}`);
  };

  return (
    <div className="report-container">
      <h1>Ticker Sentiment Report</h1>
      <div className="controls">
        <select value={selectedSubreddit} onChange={(e) => setSelectedSubreddit(e.target.value)}>
          <option value="">All Subreddits</option>
          {subreddits.map(sub => <option key={sub} value={sub}>{sub}</option>)}
        </select>
        <button onClick={() => {
          // If already sorting by mentions, flip order. Otherwise, sort descending.
          const newOrder = sortBy === 'mentions' && order === 'desc' ? 'asc' : 'desc';
          setSortBy('mentions');
          setOrder(newOrder);
        }}>Sort by Mentions</button>
        <button onClick={() => {
          // If already sorting by sentiment, flip order. Otherwise, sort descending.
          const newOrder = sortBy === 'sentiment' && order === 'desc' ? 'asc' : 'desc';
          setSortBy('sentiment');
          setOrder(newOrder);
        }}>Sort by Sentiment</button>
      </div>
      <table>
        <thead>
          <tr>
            <th style={{ width: '10%' }}>Ticker</th>
            <th style={{ width: '25%' }}>Name</th>
            <th style={{ width: '10%' }}>Mentions</th>
            <th style={{ width: '15%' }}>Sentiment</th>
            <th style={{ width: '15%' }}>Price</th>
            <th style={{ width: '15%' }}>Change</th>
            <th style={{ width: '10%' }}>Day High</th>
            <th style={{ width: '10%' }}>Day Low</th>
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr><td colSpan="3">Loading report...</td></tr>
          ) : error ? (
            <tr><td colSpan="3" style={{ color: 'red' }}>{error}</td></tr>
          ) : reportData.length === 0 ? (
            <tr><td colSpan="3">No data found for the selected filters.</td></tr>
          ) : (
            reportData.map((item) => (
              <tr key={item.ticker} onClick={() => handleRowClick(item.ticker)} className="clickable-row">
                <td><strong>{item.ticker}</strong></td>
                <td>{item.name || 'N/A'}</td>
                <td style={{ textAlign: 'center' }}>{item.mentions}</td>
                <td style={{ color: item.avg_sentiment > 0 ? '#4caf50' : '#f44336' }}>
                  {item.avg_sentiment.toFixed(3)}
                </td>
                <td>{item.current_price ? `$${item.current_price.toFixed(2)}` : 'N/A'}</td>
                <td style={{ color: item.price_change > 0 ? '#4caf50' : '#f44336' }}>
                  {item.price_change ? `${item.price_change.toFixed(2)} (${item.price_percent_change.toFixed(2)}%)` : 'N/A'}
                </td>
                <td>{item.day_high ? `$${item.day_high.toFixed(2)}` : 'N/A'}</td>
                <td>{item.day_low ? `$${item.day_low.toFixed(2)}` : 'N/A'}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Report;