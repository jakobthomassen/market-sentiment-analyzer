# Market Sentiment Analyzer

A full-stack application designed to scrape financial subreddits, perform sentiment analysis on stock discussions, and visualize the aggregated data in a web-based dashboard.

## About The Project

This project fetches posts and comments from Reddit, identifies mentions of specific stock tickers, calculates sentiment scores, and stores the results in a local database. The frontend provides an interactive dashboard to view sentiment reports, filter by subreddit, and inspect details for individual tickers.

## Built With

*   **Backend:**
    *   [Python](https://www.python.org/)
    *   [FastAPI](https://fastapi.tiangolo.com/) - High-performance web framework
    *   [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
    *   [PRAW](https://praw.readthedocs.io/en/latest/) - Python Reddit API Wrapper
    *   [NLTK (Vader)](https://www.nltk.org/howto/sentiment.html) - Sentiment analysis
*   **Frontend:**
    *   [React](https://reactjs.org/)
    *   [Vite](https://vitejs.dev/) - Frontend tooling
    *   [React Router](https://reactrouter.com/) - Declarative routing
*   **Database:**
    *   [SQLite](https://www.sqlite.org/index.html)
*   **Data Sources:**
    *   [Reddit API](https://www.reddit.com/dev/api/)
    *   [Finnhub API](https://finnhub.io/)

## Features

*   **Hybrid Data Fetching:** Utilizes a "firehose" approach for finance-specific subreddits and a targeted "search" for general subreddits to maximize relevance.
*   **Sentiment Analysis:** Calculates sentiment scores for posts and comments that mention tracked tickers.
*   **Live Financial Data:** Fetches real-time stock quotes and company information from the Finnhub API.
*   **Interactive Dashboard:** A React-based frontend to display aggregated sentiment reports.
*   **Filtering and Sorting:** Allows users to filter data by subreddit and sort by mention count or sentiment score.
*   **Detailed Ticker View:** Click on any ticker in the main report to see a detailed page with its specific market data.

## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

*   Python 3.10+
*   Node.js and npm

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/jakobthomassen/market-sentiment-analyzer.git
    cd market-sentiment-analyzer
    ```

2.  **Backend Setup:**
    *   Navigate to the backend directory:
        ```sh
        cd backend
        ```
    *   (Optional but recommended) Create and activate a virtual environment:
        ```sh
        python -m venv venv
        # On Windows
        .\venv\Scripts\activate
        # On macOS/Linux
        source venv/bin/activate
        ```
    *   Install Python dependencies:
        ```sh
        pip install -r requirements.txt
        ```
    *   Create a `.env` file in the `backend` directory and add your API keys:
        ```
        REDDIT_CLIENT_ID="your_reddit_client_id"
        REDDIT_CLIENT_SECRET="your_reddit_client_secret"
        REDDIT_USER_AGENT="your_reddit_user_agent"
        FINNHUB_API_KEY="your_finnhub_api_key"
        ```

3.  **Frontend Setup:**
    *   Navigate to the frontend directory from the project root:
        ```sh
        cd frontend
        ```
    *   Install Node.js dependencies:
        ```sh
        npm install
        ```

## Usage

You will need two terminals to run the full application.

1.  **Run the Backend API Server:**
    *   In a terminal at the `backend` directory, run:
        ```sh
        uvicorn app.api:app --reload
        ```
    *   The API will be available at `http://localhost:8000`.

2.  **Run the Frontend Development Server:**
    *   In a second terminal at the `frontend` directory, run:
        ```sh
        npm run dev
        ```
    *   Open your browser and navigate to the URL provided (usually `http://localhost:5173`).

3.  **Fetch Data:**
    *   To populate your database, you need to run the data processing scripts. In a new terminal at the `backend` directory, run the script runner:
        ```sh
        python -m app.main
        ```
    *   Use the menu to fetch Reddit data (Option 1) and then update financial data (Option 3).

## Future Ideas

*   **Advanced Sentiment Analysis:** Integrate a more sophisticated, finance-specific model like FinBERT to improve sentiment accuracy.
*   **Historical Sentiment Charting:** Overlay daily average sentiment scores on a price chart to visualize correlations.
*   **Live Data Feed:** Implement a WebSocket connection for a "Live Feed" page that shows new comments and sentiment scores in real-time.
*   **User Authentication:** Allow users to create accounts to save personalized ticker lists or settings.
