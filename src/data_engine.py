import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup

class DataEngine:
    def __init__(self):
        self.historical_data = {}
        self.news_cache = {}
        
    def get_realtime_data(self, pair):
        """Get 1-minute OHLCV data"""
        symbol = pair.replace('/', '')
        try:
            # Use free Alpha Vantage API
            url = f"https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol={symbol}&market=USD&interval=1min&apikey=YOUR_FREE_KEY"
            data = requests.get(url).json()
            df = pd.DataFrame(data['Time Series Crypto (1min)']).T
            df = df.rename(columns={
                '1. open': 'open',
                '2. high': 'high',
                '3. low': 'low',
                '4. close': 'close',
                '5. volume': 'volume'
            }).astype(float)
            return df.iloc[-100:]  # Last 100 periods
        except:
            # Fallback to Yahoo Finance
            return yf.download(tickers=symbol, period='1d', interval='1m')
    
    def get_news_sentiment(self, pair):
        """Scrape financial news sentiment"""
        base, quote = pair.split('/')
        if pair in self.news_cache:
            return self.news_cache[pair]
            
        try:
            # Use free NewsAPI
            url = f"https://newsapi.org/v2/everything?q={base}+{quote}&apiKey=YOUR_FREE_KEY"
            articles = requests.get(url).json()['articles']
            headlines = ' '.join([a['title'] for a in articles[:10]])
            
            # Use free Hugging Face sentiment analysis
            sentiment_api = "https://api-inference.huggingface.co/models/finiteautomata/bertweet-base-sentiment-analysis"
            response = requests.post(sentiment_api, json={"inputs": headlines})
            scores = response.json()[0]
            
            # Calculate bullish score
            sentiment = (scores['positive'] - scores['negative'])
            self.news_cache[pair] = sentiment
            return sentiment
        except:
            return 0  # Neutral if error
