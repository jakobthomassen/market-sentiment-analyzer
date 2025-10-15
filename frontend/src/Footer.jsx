import React from 'react';

function Footer() {
  return (
    <footer className="app-footer">
      <p>&copy; {new Date().getFullYear()} Market Sentiment Project. All rights reserved.</p>
    </footer>
  );
}

export default Footer;