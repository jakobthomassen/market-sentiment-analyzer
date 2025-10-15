"""
schemas.py
----------
Pydantic models for API data validation and serialization.
"""
from pydantic import BaseModel
from typing import List, Optional

class ReportRow(BaseModel):
    ticker: str
    name: Optional[str]
    mentions: int
    avg_sentiment: float
    current_price: Optional[float]
    price_change: Optional[float]
    price_percent_change: Optional[float]
    day_high: Optional[float]
    day_low: Optional[float]

    class Config:
        orm_mode = True

class QuoteData(BaseModel):
    c: float # Current price
    d: Optional[float] # Change
    dp: Optional[float] # Percent change
    h: float # High price of the day
    l: float # Low price of the day
    o: Optional[float] = None # Open price of the day

class TickerDetails(BaseModel):
    ticker: str
    name: str
    quote: QuoteData
    pe_ratio: Optional[float]
    market_cap: Optional[float]