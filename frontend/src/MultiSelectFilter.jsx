import React, { useState, useRef, useEffect } from 'react';

export function MultiSelectFilter({ options, selectedOptions, onChange }) {
  const [isOpen, setIsOpen] = useState(false);
  const wrapperRef = useRef(null);

  const handleToggle = (option) => {
    const newSelection = selectedOptions.includes(option)
      ? selectedOptions.filter((item) => item !== option)
      : [...selectedOptions, option];
    onChange(newSelection);
  };

  const handleSelectAll = () => {
    if (selectedOptions.length === options.length) {
      onChange([]); // Deselect all
    } else {
      onChange(options); // Select all
    }
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [wrapperRef]);

  return (
    <div className="multiselect-filter" ref={wrapperRef}>
      <button
        className="filter-button"
        onClick={() => setIsOpen(!isOpen)}
      >
        Filter Subreddits ({selectedOptions.length || 'All'})
      </button>
      <p className="filter-notice">
        Note: Filter is under development and may be inaccurate.
      </p>
      {isOpen && (
        <div className="dropdown-menu">
          <div className="dropdown-item" onClick={handleSelectAll}><strong>{selectedOptions.length === options.length ? 'Deselect All' : 'Select All'}</strong></div>
          {options.map(option => (
            <div key={option} className="dropdown-item" onClick={() => handleToggle(option)}>
              <input type="checkbox" checked={selectedOptions.includes(option)} readOnly />
              {option}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}