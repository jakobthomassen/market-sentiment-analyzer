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

import praw
import csv
import os
from datetime import datetime
from app.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT


def get_reddit_client(): # Initialize and return a reddit client.
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    return reddit


def fetch_posts(subreddits, limit=10, include_comments=True): # Fetches a list of recent posts from a list of subreddits.
    reddit = get_reddit_client()
    results = []

    for sub in subreddits:
        subreddit = reddit.subreddit(sub)
        print(f"Fetching from r/{sub}...")
        for post in subreddit.new(limit=limit):
            post_data = {
                "id": post.id,
                "subreddit": sub,
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
                post.comments.replace_more(limit=0)
                comments = []
                for comment in post.comments[:5]:  # limit to 5 comments
                    comments.append({
                        "author": str(comment.author),
                        "body": comment.body,
                        "upvotes": comment.score,
                    })
                post_data["comments"] = comments

            results.append(post_data)

    return results


def save_to_csv(data, filename="reddit_posts.csv"):
    if not data:
        print("No data to save.")
        return

    keys = ["id", "subreddit", "title", "author", "url", "created_utc", "upvotes", "num_comments", "selftext"]
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for post in data:
            writer.writerow({k: post.get(k, "") for k in keys})
    print(f"Saved {len(data)} posts to {filename}")


# -------------------------                 Connect to reddit using your credentials
# Functional Test Section                   Fetch posts from r/stocks and r/wallstreetbets
# -------------------------                 Save results to reddit_posts.csv in current directory
if __name__ == "__main__": 
    subreddits = ["stocks", "wallstreetbets"]
    posts = fetch_posts(subreddits, limit=5)
    save_to_csv(posts, "reddit_posts.csv")

    print("\nExample post:")
    if posts:
        example = posts[0]
        print(f"Title: {example['title']}")
        print(f"Subreddit: {example['subreddit']}")
        print(f"Comments: {len(example.get('comments', []))}")
