"""
main.py
-------
Main script for running development and data processing tasks.
"""

from datetime import datetime
from app.database import SessionLocal, Base, engine
from app.models import RedditComment, RedditPost
from app.services.reddit_fetcher import fetch_posts
from app.services.db_writer import insert_posts
from app.services.finnhub_client import get_company_profile, get_quote
from app.services.financial_data_updater import update_all_ticker_data

def run_reddit_fetcher():
    """Initializes DB and fetches new data from Reddit."""
    print("\n--- Fetching New Reddit Data ---")
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)

    subreddit_config = {
        "US": [
            {"name": "stocks", "type": "firehose"},
            {"name": "wallstreetbets", "type": "firehose"},
        ],
        "NO": [
            {"name": "TollbugataBets", "type": "firehose"},
            {"name": "norge", "type": "search"},
        ],
    }

    print("Fetching posts...")
    posts_to_insert = fetch_posts(subreddit_config, limit=20, include_comments=True)
    insert_posts(posts_to_insert)
    print("\nReddit fetch process finished.")

def run_finnhub_test():
    """Tests the connection to the Finnhub API by fetching a company profile."""
    print("\n--- Running Finnhub API Test ---")
    ticker = "AAPL"
    try:
        print(f"Fetching data for {ticker}...")

        profile = get_company_profile(ticker)
        print(f"\nProfile for {profile.get('name')}:")
        print(f"  Industry: {profile.get('finnhubIndustry')}")

        quote = get_quote(ticker)
        print(f"\nLatest Quote:")
        print(f"  Current Price: {quote.get('c')}")
        print(f"  Day's High: {quote.get('h')}")
        print(f"  Day's Low: {quote.get('l')}")

        # The 'get_basic_financials' endpoint is premium and is commented out for the free tier.
        # financials = get_basic_financials(ticker)
        # print(f"\nBasic Financials:")
        # print(f"  P/E Ratio: {financials.get('metric', {}).get('peNormalizedAnnual')}")
        # print(f"  Market Cap: {financials.get('metric', {}).get('marketCapitalization')}")
    except Exception as e:
        print(f"Error fetching profile for {ticker}: {e}")

def run_sentiment_analysis_review():
    """Reviews the latest sentiment scores stored in the database."""
    print("\n--- Reviewing Stored Sentiment Analysis ---")
    session = SessionLocal()
    try:
        comments_to_review = session.query(RedditComment).filter(RedditComment.sentiment_score != None).order_by(RedditComment.id.desc()).limit(5).all()

        if not comments_to_review:
            print("No comments with sentiment scores found. Run the Reddit fetcher first.")
            return

        for comment in comments_to_review:
            score = comment.sentiment_score
            print(f"\nComment: '{comment.body[:100]}...'")
            print(f"Ticker: {comment.ticker_symbol}, Score: {score:.2f}")
    finally:
        session.close()

def main_menu():
    """Displays the main menu and runs the selected task."""
    while True:
        print("\n--- Main Menu ---")
        print("1. Fetch new Reddit data")
        print("2. Test Finnhub connection")
        print("3. Update all financial data from Finnhub")
        print("4. Review latest sentiment analysis")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            run_reddit_fetcher()
        elif choice == '2':
            run_finnhub_test()
        elif choice == '3':
            update_all_ticker_data()
        elif choice == '4':
            run_sentiment_analysis_review()
        elif choice == '5':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
