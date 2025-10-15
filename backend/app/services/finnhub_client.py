"""
finnhub_client.py
-----------------
Handles all interactions with the Finnhub API.
"""
from datetime import datetime, timedelta
import time

import finnhub
from ..config import FINNHUB_API_KEY

_finnhub_client = None

def get_finnhub_client():
    """Initializes and returns a singleton Finnhub client."""
    global _finnhub_client
    if _finnhub_client is None:
        _finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
    return _finnhub_client

def get_company_profile(ticker: str) -> dict:
    """Fetches a company profile for a given ticker."""
    client = get_finnhub_client()
    # Using profile2 for more detailed data
    return client.company_profile2(symbol=ticker)

def get_quote(ticker: str) -> dict:
    """Fetches the latest quote data for a given ticker."""
    client = get_finnhub_client()
    return client.quote(symbol=ticker)

def get_basic_financials(ticker: str) -> dict:
    """Fetches basic financial metrics like P/E ratio."""
    client = get_finnhub_client()
    return client.company_basic_financials(symbol=ticker, metric='all')