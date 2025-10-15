"""
sentiment.py
------------
Performs sentiment analysis on text data.
"""

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the VADER lexicon if it's not already present
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    print("Downloading VADER lexicon...")
    nltk.download('vader_lexicon')


def analyze_sentiment(text: str) -> float:
    """
    Analyzes text and returns a compound sentiment score.
    Score ranges from -1 (most negative) to +1 (most positive).
    """
    analyzer = SentimentIntensityAnalyzer()
    # The 'compound' score is a useful single metric for sentiment
    return analyzer.polarity_scores(text)['compound']