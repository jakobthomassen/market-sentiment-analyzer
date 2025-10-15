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
TICKER_MAP = {
    # Technology
    "AAPL": ["Apple", "AAPL"],
    "MSFT": ["Microsoft", "MSFT"],
    "AMZN": ["Amazon", "AMZN"],
    "GOOGL": ["Google", "Alphabet", "GOOGL", "GOOG"],
    "META": ["Meta", "Facebook", "FB"],
    "NVDA": ["Nvidia", "NVDA"],
    "TSLA": ["Tesla", "TSLA"],
    "NFLX": ["Netflix", "NFLX"],
    "AMD": ["AMD", "Advanced Micro Devices"],
    "PYPL": ["PayPal", "PYPL"],
    "ADBE": ["Adobe", "ADBE"],
    "DIS": ["Disney", "DIS"],
    "INTC": ["Intel", "INTC"],
    "CRM": ["Salesforce", "CRM"],
    "ORCL": ["Oracle", "ORCL"],

    # Finance
    "JPM": ["JPMorgan", "JPM", "Chase"],
    "BAC": ["Bank of America", "BAC"],
    "WFC": ["Wells Fargo", "WFC"],
    "GS": ["Goldman Sachs", "GS"],
    "V": ["Visa", "V"],
    "MA": ["Mastercard", "MA"],
    "BRK.B": ["Berkshire Hathaway", "BRK-B", "BRK.B"],
    "C": ["Citigroup", "Citi", "C"],

    # Consumer & Retail
    "WMT": ["Walmart", "WMT"],
    "COST": ["Costco", "COST"],
    "TGT": ["Target", "TGT"],
    "NKE": ["Nike", "NKE"],
    "MCD": ["McDonald's", "MCD"],
    "SBUX": ["Starbucks", "SBUX"],
    "KO": ["Coca-Cola", "Coke", "KO"],
    "PEP": ["Pepsi", "PepsiCo", "PEP"],
    "HD": ["Home Depot", "HD"],

    # Healthcare & Energy
    "JNJ": ["Johnson & Johnson", "J&J", "JNJ"],
    "PFE": ["Pfizer", "PFE"],
    "XOM": ["Exxon Mobil", "Exxon", "XOM"],
    "CVX": ["Chevron", "CVX"],

    # Other Popular Stocks
    "GME": ["GameStop", "GME"],
    "AMC": ["AMC Entertainment", "AMC"],
    "BA": ["Boeing", "BA"],

    # Norwegian Stocks (Oslo Børs)
    "EQNR": ["Equinor", "Statoil", "EQNR"],
    "DNB": ["DNB", "DNB Bank"],
    "TEL": ["Telenor", "TEL"],
    "NHY": ["Norsk Hydro", "NHY"],
    "YAR": ["Yara", "Yara International", "YAR"],
    "KOG": ["Kongsberg"],
}

def extract_tickers(text: str) -> set[str]:
    """Extracts a set of official ticker symbols found in a piece of text."""
    found_tickers = set()
    for official_ticker, aliases in TICKER_MAP.items():
        for alias in aliases:
            if re.search(r'\b' + re.escape(alias) + r'\b', text, re.IGNORECASE):
                found_tickers.add(official_ticker)
                break # Move to the next official ticker once an alias is found
    return found_tickers

def get_ticker_search_query() -> str:
    """
    Generates a Reddit search query string from all ticker aliases.
    e.g., '"Apple" OR AAPL OR "Microsoft" OR MSFT'
    """
    all_aliases = []
    for aliases in TICKER_MAP.values():
        for alias in aliases:
            # Quote aliases with spaces to treat them as a single search term
            all_aliases.append(f'"{alias}"' if ' ' in alias else alias)
    return " OR ".join(all_aliases)