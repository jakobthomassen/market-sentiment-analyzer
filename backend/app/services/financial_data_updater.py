"""
financial_data_updater.py
-------------------------
Fetches and updates financial data for all known tickers in the database.
"""
from datetime import datetime, timedelta
import time
from ..database import SessionLocal
from ..models import RedditComment, TickerData
from . import finnhub_client

def update_all_ticker_data():
    """
    Finds all unique tickers from comments/posts and updates their financial data.
    """
    session = SessionLocal()
    updated_count = 0
    skipped_count = 0
    # Define how old data can be before we refresh it (e.g., 4 hours)
    staleness_threshold = datetime.utcnow() - timedelta(hours=4)

    try:
        # Get all unique tickers mentioned in our database
        tickers_in_db = session.query(RedditComment.ticker_symbol).filter(RedditComment.ticker_symbol != None).distinct().all()
        unique_tickers = {row[0] for row in tickers_in_db}

        print(f"Found {len(unique_tickers)} unique tickers. Checking for stale financial data...")

        for ticker in unique_tickers:
            try:
                existing_data = session.get(TickerData, ticker)
                # If data exists and is fresh, skip the update for this ticker
                if existing_data and existing_data.last_updated > staleness_threshold:
                    skipped_count += 1
                    continue

                print(f"  - Updating data for {ticker}...")
                profile = finnhub_client.get_company_profile(ticker)
                quote = finnhub_client.get_quote(ticker)
                                
                if existing_data:
                    existing_data.name = profile.get('name')
                    existing_data.current_price = quote.get('c')
                    existing_data.price_change = quote.get('d')
                    existing_data.price_percent_change = quote.get('dp')
                    existing_data.day_high = quote.get('h')
                    existing_data.day_low = quote.get('l')
                else:
                    new_data = TickerData(
                        ticker=ticker, name=profile.get('name'), current_price=quote.get('c'),
                        price_change=quote.get('d'), price_percent_change=quote.get('dp'),
                        day_high=quote.get('h'), day_low=quote.get('l'),
                    )
                    session.add(new_data)
                updated_count += 1
                time.sleep(1) # Respect API rate limits
            except Exception as e:
                print(f"  - FAILED to update data for {ticker}: {e}")

        session.commit()
        print(f"\nSuccessfully updated {updated_count} tickers and skipped {skipped_count} fresh ones.")
    finally:
        session.close()