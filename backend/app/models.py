"""
models.py
----------
Defines database schema for Reddit posts and comments.
"""

from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class RedditPost(Base):
    __tablename__ = "reddit_posts"

    id = Column(String, primary_key=True, index=True)
    subreddit = Column(String, index=True)
    region = Column(String, index=True)
    title = Column(Text)
    author = Column(String)
    url = Column(String, unique=True)
    created_utc = Column(DateTime, default=datetime.utcnow)
    upvotes = Column(Integer)
    num_comments = Column(Integer)
    selftext = Column(Text)
    sentiment_score = Column(Float, nullable=True)
    ticker_symbol = Column(String, nullable=True, index=True) # For simplicity, stores one ticker.

    comments = relationship("RedditComment", back_populates="post", cascade="all, delete-orphan")

class RedditComment(Base):
    __tablename__ = "reddit_comments"

    id = Column(String, primary_key=True, index=True)
    post_id = Column(String, ForeignKey("reddit_posts.id"))
    parent_id = Column(String, ForeignKey("reddit_comments.id"), nullable=True) # Link to parent comment
    author = Column(String)
    body = Column(Text)
    upvotes = Column(Integer)
    sentiment_score = Column(Float, nullable=True)
    ticker_symbol = Column(String, nullable=True, index=True)
    region = Column(String, index=True)

    post = relationship("RedditPost", back_populates="comments")
    # Self-referential relationship for comment replies
    parent = relationship("RedditComment", remote_side=[id], back_populates="replies")
    replies = relationship("RedditComment", back_populates="parent", cascade="all, delete-orphan")

class TickerData(Base):
    __tablename__ = "ticker_data"

    ticker = Column(String, primary_key=True, index=True)
    name = Column(String)
    current_price = Column(Float)
    price_change = Column(Float)
    price_percent_change = Column(Float)
    day_high = Column(Float)
    day_low = Column(Float)
    pe_ratio = Column(Float, nullable=True)
    market_cap = Column(Float, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
