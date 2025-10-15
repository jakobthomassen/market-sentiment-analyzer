"""
reddit_fetcher.py
-----------------
This module uses PRAW (Python Reddit API Wrapper) to fetch posts and comments
from target subreddits for market sentiment analysis.

Intended functionality:
- Pull recent posts from specific subreddits (e.g. r/stocks, r/wallstreetbets)
- Optionally include comments
- Store structured data to a CSV
- To be extended later for scheduled automatic updates
"""

# Use 'python -m app.services.reddit_fetcher' for isolated test

import praw
import csv
import os
from datetime import datetime
from app.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT
from ..services.db_writer import insert_posts
from ..analysis.tickers import get_ticker_search_query
from ..database import Base, engine

def get_reddit_client(): # Initialize and return a reddit client.
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    return reddit

def _fetch_comment_tree(comment_forest, parent_id=None, limit_per_level=5):
    """Recursively fetch comments and their replies."""
    comments_data = []
    comment_forest.replace_more(limit=0) # Expand "load more comments"
    
    count = 0
    for comment in comment_forest:
        if count >= limit_per_level:
            break
        comments_data.append({
            "id": comment.id,
            "author": str(comment.author),
            "body": comment.body,
            "upvotes": comment.score,
            "parent_id": parent_id
        })
        # Recursively fetch replies to this comment
        comments_data.extend(_fetch_comment_tree(comment.replies, parent_id=comment.id, limit_per_level=2))
        count += 1
    return comments_data

def fetch_posts(subreddit_config, limit=10, include_comments=True): # Fetches posts based on subreddit configuration.
    reddit = get_reddit_client()
    results = []
    search_query = get_ticker_search_query()

    for region, configs in subreddit_config.items():
        for config in configs:
            sub_name = config["name"]
            fetch_type = config["type"]
            subreddit = reddit.subreddit(sub_name)
            
            post_iterator = []
            if fetch_type == "firehose":
                print(f"Fetching all new posts from r/{sub_name} (Region: {region})...")
                post_iterator = subreddit.new(limit=limit)
            elif fetch_type == "search":
                print(f"Searching for ticker mentions in r/{sub_name} (Region: {region})...")
                post_iterator = subreddit.search(search_query, sort="new", limit=limit)

            for post in post_iterator:
                post_data = {
                    "id": post.id,
                    "subreddit": sub_name,
                    "region": region,
                    "title": post.title,
                    "author": str(post.author),
                    "url": post.url,
                    "created_utc": datetime.utcfromtimestamp(post.created_utc).isoformat(),
                    "upvotes": post.score,
                    "num_comments": post.num_comments,
                    "selftext": post.selftext,
                }
    
                # Optionally fetch top-level comments
                if include_comments:
                    post_data["comments"] = _fetch_comment_tree(post.comments, limit_per_level=5)
    
                results.append(post_data)
    
    return results


# -------------------------                 Connect to reddit using your credentials
# Main execution block                      Fetch posts and store in the database
# -------------------------
if __name__ == "__main__":
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)

    # Define subreddit configurations: 'firehose' for all new, 'search' for ticker-specific.
    subreddit_config = {
        "US": [
            {"name": "stocks", "type": "firehose"},
            {"name": "wallstreetbets", "type": "firehose"}
        ],
        "NO": [
            {"name": "TollbugataBets", "type": "firehose"},
            {"name": "norge", "type": "search"} # Only fetch posts mentioning tickers
        ]
    }

    print(f"Fetching posts...")
    posts_to_insert = fetch_posts(subreddit_config, limit=20, include_comments=True)
    insert_posts(posts_to_insert)
    print("\nProcess finished.")
