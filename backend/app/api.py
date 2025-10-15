"""
api.py
------
FastAPI application for serving market sentiment data.
"""

from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from .database import SessionLocal
from .models import RedditComment, RedditPost, TickerData
from .schemas import ReportRow, TickerDetails
from .services import finnhub_client

app = FastAPI()

# --- CORS Middleware ---
# This allows your React frontend (running on a different port) to communicate with this backend.
origins = [
    "http://localhost:5173",  # Default Vite dev server URL
    "http://localhost:3000",  # Default Create React App dev server URL
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dependency for getting a DB session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/subreddits", response_model=List[str])
def get_subreddits(db: Session = Depends(get_db)):
    """Returns a list of unique subreddits from the database."""
    results = db.query(RedditPost.subreddit).distinct().order_by(RedditPost.subreddit).all()
    return [row[0] for row in results]

@app.get("/api/report", response_model=List[ReportRow])
def get_sentiment_report(
    db: Session = Depends(get_db),
    subreddit: List[str] = Query(None, description="Filter by a list of subreddits"),
    sort_by: str = Query("mentions", description="Sort by 'mentions' or 'sentiment'"),
    order: str = Query("desc", description="Sort order 'asc' or 'desc'"),
):
    """Generates and returns the aggregated sentiment report for all tickers."""
    # Query for sentiment aggregation
    query = db.query(
        RedditComment.ticker_symbol.label("ticker"),
        RedditComment.region.label("region"),
        func.count(RedditComment.id).label("mentions"),
        func.avg(RedditComment.sentiment_score).label("avg_sentiment"),
        TickerData.name,
        TickerData.current_price,
        TickerData.price_change,
        TickerData.price_percent_change,
        TickerData.day_high,
        TickerData.day_low,
    ).join(
        TickerData, RedditComment.ticker_symbol == TickerData.ticker, isouter=True
    ).filter(RedditComment.ticker_symbol != None)

    if subreddit and len(subreddit) > 0:
        # Use a subquery for more robust filtering. This finds all post_ids that match the subreddit filter.
        subquery = db.query(RedditPost.id).filter(RedditPost.subreddit.in_(subreddit))
        # Then filter the comments to only include those whose post_id is in the subquery result.
        query = query.filter(RedditComment.post_id.in_(subquery))

    query = query.group_by(RedditComment.ticker_symbol, RedditComment.region)

    sort_column = func.count(RedditComment.id) if sort_by == "mentions" else func.avg(RedditComment.sentiment_score)
    sort_logic = sort_column.desc() if order == "desc" else sort_column.asc()
    query = query.order_by(sort_logic)

    results = query.all()
    return results

@app.get("/api/ticker/{ticker_symbol}", response_model=TickerDetails)
def get_ticker_details(ticker_symbol: str, db: Session = Depends(get_db)):
    """
    Fetches detailed financial data for a given ticker symbol from the database.
    """
    ticker_data = db.get(TickerData, ticker_symbol.upper())
    if not ticker_data:
        raise HTTPException(status_code=404, detail="Ticker data not found. Please run the financial data update from the main menu.")

    return {
        "ticker": ticker_data.ticker,
        "name": ticker_data.name,
        "quote": {
            "c": ticker_data.current_price,
            "d": ticker_data.price_change,
            "dp": ticker_data.price_percent_change,
            "h": ticker_data.day_high,
            "l": ticker_data.day_low,
        },
        "pe_ratio": ticker_data.pe_ratio,
        "market_cap": ticker_data.market_cap,
    }