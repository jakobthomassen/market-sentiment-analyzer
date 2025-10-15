"""
tickers.py
----------
Manages ticker symbols and their aliases for extraction from text.
"""

import re

# --- Your Ticker and Alias List ---
# The key is the official ticker symbol (e.g., GME)
# The value is a list of aliases to search for (case-insensitive)
# This list is a starting point and can be expanded or dynamically populated.
TICKER_MAP = { # region can be 'US' or 'NO'
    # Technology
    "AAPL": {"aliases": ["Apple", "AAPL"], "region": "US"},
    "MSFT": {"aliases": ["Microsoft", "MSFT"], "region": "US"},
    "AMZN": {"aliases": ["Amazon", "AMZN"], "region": "US"},
    "GOOGL": {"aliases": ["Google", "Alphabet", "GOOGL", "GOOG"], "region": "US"},
    "META": {"aliases": ["Meta", "Facebook", "FB"], "region": "US"},
    "NVDA": {"aliases": ["Nvidia", "NVDA"], "region": "US"},
    "TSLA": {"aliases": ["Tesla", "TSLA"], "region": "US"},
    "NFLX": {"aliases": ["Netflix", "NFLX"], "region": "US"},
    "AMD": {"aliases": ["AMD", "Advanced Micro Devices"], "region": "US"},
    "PYPL": {"aliases": ["PayPal", "PYPL"], "region": "US"},
    "ADBE": {"aliases": ["Adobe", "ADBE"], "region": "US"},
    "DIS": {"aliases": ["Disney", "DIS"], "region": "US"},
    "INTC": {"aliases": ["Intel", "INTC"], "region": "US"},
    "CRM": {"aliases": ["Salesforce", "CRM"], "region": "US"},
    "ORCL": {"aliases": ["Oracle", "ORCL"], "region": "US"},

    # Finance
    "JPM": {"aliases": ["JPMorgan", "JPM", "Chase"], "region": "US"},
    "BAC": {"aliases": ["Bank of America", "BAC"], "region": "US"},
    "WFC": {"aliases": ["Wells Fargo", "WFC"], "region": "US"},
    "GS": {"aliases": ["Goldman Sachs", "GS"], "region": "US"},
    "V": {"aliases": ["Visa", "V"], "region": "US"},
    "MA": {"aliases": ["Mastercard", "MA"], "region": "US"},
    "BRK.B": {"aliases": ["Berkshire Hathaway", "BRK-B", "BRK.B"], "region": "US"},
    "C": {"aliases": ["Citigroup", "Citi", "C"], "region": "US"},

    # Consumer & Retail
    "WMT": {"aliases": ["Walmart", "WMT"], "region": "US"},
    "COST": {"aliases": ["Costco", "COST"], "region": "US"},
    "TGT": {"aliases": ["Target", "TGT"], "region": "US"},
    "NKE": {"aliases": ["Nike", "NKE"], "region": "US"},
    "MCD": {"aliases": ["McDonald's", "MCD"], "region": "US"},
    "SBUX": {"aliases": ["Starbucks", "SBUX"], "region": "US"},
    "KO": {"aliases": ["Coca-Cola", "Coke", "KO"], "region": "US"},
    "PEP": {"aliases": ["Pepsi", "PepsiCo", "PEP"], "region": "US"},
    "HD": {"aliases": ["Home Depot", "HD"], "region": "US"},

    # Healthcare & Energy
    "JNJ": {"aliases": ["Johnson & Johnson", "J&J", "JNJ"], "region": "US"},
    "PFE": {"aliases": ["Pfizer", "PFE"], "region": "US"},
    "XOM": {"aliases": ["Exxon Mobil", "Exxon", "XOM"], "region": "US"},
    "CVX": {"aliases": ["Chevron", "CVX"], "region": "US"},

    # Other Popular Stocks
    "GME": {"aliases": ["GameStop", "GME"], "region": "US"},
    "AMC": {"aliases": ["AMC Entertainment", "AMC"], "region": "US"},
    "BA": {"aliases": ["Boeing", "BA"], "region": "US"},

    # Norwegian Stocks (Oslo Børs)
    "EQNR": {"aliases": ["Equinor", "Statoil", "EQNR"], "region": "NO"},
    "DNB": {"aliases": ["DNB", "DNB Bank"], "region": "NO"},
    "TEL": {"aliases": ["Telenor", "TEL"], "region": "NO"},
    "NHY": {"aliases": ["Norsk Hydro", "NHY"], "region": "NO"},
    "YAR": {"aliases": ["Yara", "Yara International"], "region": "NO"},
    "KOG": {"aliases": ["Kongsberg"], "region": "NO"},
}

def extract_tickers(text: str) -> list[tuple[str, str]]:
    """Extracts a list of (ticker, region) tuples found in a piece of text."""
    found_tickers = []
    # Use a set to avoid adding the same ticker multiple times
    found_symbols = set()
    for official_ticker, data in TICKER_MAP.items():
        for alias in data["aliases"]:
            if re.search(r'\b' + re.escape(alias) + r'\b', text, re.IGNORECASE):
                if official_ticker not in found_symbols:
                    found_tickers.append((official_ticker, data["region"]))
                    found_symbols.add(official_ticker)
    return found_tickers

def get_ticker_search_query() -> str:
    """
    Generates a Reddit search query string from all ticker aliases.
    e.g., '"Apple" OR AAPL OR "Microsoft" OR MSFT'
    """
    all_aliases = []
    for data in TICKER_MAP.values():
        for alias in data["aliases"]:
            # Quote aliases with spaces to treat them as a single search term
            all_aliases.append(f'"{alias}"' if ' ' in alias else alias)
    return " OR ".join(all_aliases)