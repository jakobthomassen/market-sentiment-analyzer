import React from 'react';

function AboutPage() {
  return (
    <div className="about-container">
      <h2>About This Project</h2>
      <p>
        This Market Sentiment Analyzer is a personal project designed to fetch and analyze discussions
        from various financial subreddits. It scrapes posts and comments, performs sentiment analysis,
        and aggregates the data to provide insights into market trends and public opinion on various stocks.
      </p>
      <h3>Technology Stack</h3>
      <ul>
        <li><strong>Backend:</strong> Python, FastAPI, SQLAlchemy, PRAW</li>
        <li><strong>Frontend:</strong> React, Vite</li>
        <li><strong>Sentiment Analysis:</strong> NLTK (Vader)</li>
        <li><strong>Financial Data:</strong> Finnhub API</li>
      </ul>
      <h3>Source Code</h3>
      <p>
        The complete source code for this project is available on GitHub. Feel free to explore, fork, or contribute!
      </p>
      <a
        href="https://github.com/jakobthomassen/market-sentiment-analyzer"
        target="_blank"
        rel="noopener noreferrer"
        className="github-link"
      >
        View on GitHub
      </a>
    </div>
  );
}

export default AboutPage;