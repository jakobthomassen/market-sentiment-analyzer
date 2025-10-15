"""
db_writer.py
------------
Handles inserting fetched Reddit data into the database while avoiding duplicates.
"""

from datetime import datetime
from sqlalchemy.exc import IntegrityError
from ..database import SessionLocal
from ..models import RedditPost, RedditComment
from ..analysis.sentiment import analyze_sentiment
from ..analysis.tickers import extract_tickers


def insert_posts(posts):
    """Insert new Reddit posts and comments, skipping duplicates."""
    session = SessionLocal()
    added_count = 0
    updated_count = 0

    try:
        for post_data in posts:
            # Check if post already exists
            existing_post = session.get(RedditPost, post_data["id"])

            # --- Efficient Analysis Step ---
            # Combine title and selftext for analysis
            post_text_to_analyze = f"{post_data['title']} {post_data['selftext']}"
            found_tickers = extract_tickers(post_text_to_analyze)
            
            sentiment_score = None
            ticker_symbol = None
            # The post's region defaults to the subreddit's region, but can be overridden by a ticker.
            post_region = post_data["region"]
            if found_tickers:
                ticker_symbol, post_region = found_tickers[0] # (ticker, region)
                sentiment_score = analyze_sentiment(post_text_to_analyze)

            if existing_post:
                # Update existing post's metrics
                existing_post.upvotes = post_data["upvotes"]
                existing_post.num_comments = post_data["num_comments"]

                # --- Logic to sync comments ---
                existing_comments = {c.id: c for c in existing_post.comments}
                fetched_comments_map = {c_data['id']: c_data for c_data in post_data.get("comments", [])}

                # Update existing comments and add new ones
                for c_id, c_data in fetched_comments_map.items():
                    if c_id in existing_comments:
                        # Update upvotes on existing comment
                        existing_comments[c_id].upvotes = c_data["upvotes"]
                    else:
                        # Prioritize ticker in comment, else inherit from post.
                        comment_tickers = extract_tickers(c_data["body"])
                        comment_sentiment = None
                        comment_ticker_symbol = None
                        comment_region = existing_post.region # Default to post's region

                        if comment_tickers:
                            comment_ticker_symbol, comment_region = comment_tickers[0]
                            comment_sentiment = analyze_sentiment(c_data["body"])
                        elif existing_post.ticker_symbol:
                            # Inherit ticker and region from post if comment has no ticker
                            comment_ticker_symbol = existing_post.ticker_symbol
                            comment_sentiment = analyze_sentiment(c_data["body"])

                        # Add new comment
                        new_comment = RedditComment(
                            id=c_data["id"],
                            author=c_data["author"],
                            body=c_data["body"],
                            upvotes=c_data["upvotes"],
                            parent_id=c_data.get("parent_id"),
                            region=comment_region,
                            post=existing_post,
                            sentiment_score=comment_sentiment,
                            ticker_symbol=comment_ticker_symbol,
                        )
                        existing_post.comments.append(new_comment)
                session.add(existing_post)
                updated_count += 1
            else:
                # Insert new post
                new_post = RedditPost(
                    id=post_data["id"],
                    subreddit=post_data["subreddit"],
                    region=post_region,
                    title=post_data["title"],
                    author=post_data["author"],
                    url=post_data["url"],
                    created_utc=datetime.fromisoformat(post_data["created_utc"]),
                    upvotes=post_data["upvotes"],
                    num_comments=post_data["num_comments"],
                    selftext=post_data["selftext"],
                    sentiment_score=sentiment_score,
                    ticker_symbol=ticker_symbol,
                )

                # Process and link all comments for the new post
                comment_map = {}
                for c_data in post_data.get("comments", []):
                    # Prioritize ticker in comment, else inherit from post.
                    comment_tickers = extract_tickers(c_data["body"])
                    comment_sentiment = None
                    comment_ticker_symbol = None
                    comment_region = post_region # Default to post's region

                    if comment_tickers:
                        comment_ticker_symbol, comment_region = comment_tickers[0]
                        comment_sentiment = analyze_sentiment(c_data["body"])
                    elif ticker_symbol: # Inherit from the new post
                        comment_ticker_symbol = ticker_symbol
                        comment_sentiment = analyze_sentiment(c_data["body"])

                    comment = RedditComment(id=c_data["id"], author=c_data["author"], body=c_data["body"], upvotes=c_data["upvotes"], sentiment_score=comment_sentiment, ticker_symbol=comment_ticker_symbol, region=comment_region)
                    comment_map[comment.id] = comment

                # Establish relationships after creating all comment objects
                for c_data in post_data.get("comments", []):
                    comment = comment_map[c_data["id"]]
                    parent_id = c_data.get("parent_id")
                    if parent_id:
                        parent_comment = comment_map.get(parent_id)
                        if parent_comment:
                            comment.parent = parent_comment
                    else:
                        # Only top-level comments are linked directly to the post
                        comment.post = new_post
                
                session.add(new_post)
                added_count += 1

        session.commit()
        print(f"Inserted {added_count} new posts and updated {updated_count} existing posts.")
    except IntegrityError:
        session.rollback()
        print("IntegrityError: Skipping duplicate entries.")
    finally:
        session.close()
