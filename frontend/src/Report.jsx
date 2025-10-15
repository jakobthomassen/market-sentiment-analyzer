import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { MultiSelectFilter } from './MultiSelectFilter';

// A simple component to render a flag emoji
const Flag = ({ region }) => {
  if (region === 'US') return <span role="img" aria-label="USA Flag">🇺🇸</span>;
  if (region === 'NO') return <span role="img" aria-label="Norway Flag">🇳🇴</span>;
  return null;
};

// The URL where our FastAPI backend is running.
const API_BASE_URL = 'http://localhost:8000/api';

function Report() {
  const [reportData, setReportData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // State for UI controls
  const [subreddits, setSubreddits] = useState([]);
  const [selectedSubreddits, setSelectedSubreddits] = useState([]);
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
      if (selectedSubreddits.length > 0) {
        selectedSubreddits.forEach(sub => params.append('subreddit', sub));
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
  }, [selectedSubreddits, sortBy, order]); // Re-run this effect when any of these values change

  const handleRowClick = (ticker) => {
    navigate(`/ticker/${ticker}`);
  };

  const handleSort = (newSortBy) => {
    const newOrder = sortBy === newSortBy && order === 'desc' ? 'asc' : 'desc';
    setSortBy(newSortBy);
    setOrder(newOrder);
  };

  const SortableHeader = ({ title, sortKey }) => {
    const isSorting = sortBy === sortKey;
    const arrow = isSorting ? (order === 'desc' ? '▼' : '▲') : '';
    return (
      <th onClick={() => handleSort(sortKey)} className="sortable-header">
        {title} {arrow}
      </th>
    );
  };

  return (
    <div className="report-container">
      <h1>Ticker Sentiment Report</h1>
      <div className="controls">
        <MultiSelectFilter
          options={subreddits}
          selectedOptions={selectedSubreddits}
          onChange={setSelectedSubreddits}
        />
      </div>
      <table>
        <thead>
          <tr>
            <th style={{ width: '10%' }}>Ticker</th>
            <th style={{ width: '25%' }}>Name</th>
            <SortableHeader title="Mentions" sortKey="mentions" />
            <SortableHeader title="Sentiment" sortKey="sentiment" />
            <SortableHeader title="Price" sortKey="price" />
            <SortableHeader title="Change" sortKey="change" />
            <th style={{ width: '10%' }}>Day High</th>
            <th style={{ width: '10%' }}>Day Low</th>
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr><td colSpan="8">Loading report...</td></tr>
          ) : error ? (
            <tr><td colSpan="8" style={{ color: 'red' }}>{error}</td></tr>
          ) : reportData.length === 0 ? (
            <tr><td colSpan="8">No data found for the selected filters.</td></tr>
          ) : (
            reportData.map((item) => (
              <tr key={`${item.ticker}-${item.region}`} onClick={() => handleRowClick(item.ticker)} className="clickable-row">
                <td>
                  <Flag region={item.region} /> <strong>{item.ticker}</strong>
                </td>
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