import numpy as np
import joblib
from tensorflow.keras.models import load_model
from ta import add_all_ta_features
from .data_engine import DataEngine

class AIPredictor:
    def detect_breakout(self, df):
    # Triple confirmation system
    last = df.iloc[-1]
    prev = df.iloc[-2]
    
    # 1. Price action
    price_break = (last['close'] > last['bollinger_hband']) or \
                  (last['close'] < last['bollinger_lband'])
    
    # 2. Volume spike (2x average)
    vol_spike = last['volume'] > 2.0 * df['volume'].rolling(20).mean().iloc[-1]
    
    # 3. RSI divergence
    rsi_bullish = (last['rsi'] > 50) and (last['rsi'] > prev['rsi'])
    rsi_bearish = (last['rsi'] < 50) and (last['rsi'] < prev['rsi'])
    
    return (price_break and vol_spike and 
           ((last['close'] > last['open'] and rsi_bullish) or 
            (last['close'] < last['open'] and rsi_bearish)))
    def __init__(self):
        self.models = self.load_models()
        self.data_engine = DataEngine()
        
    def load_models(self):
        """Load pre-trained models (initially train with Colab)"""
        return {
            'breakout_detector': joblib.load('models/production/breakout_model.pkl'),
            'trend_predictor': load_model('models/production/lstm_trend.h5')
        }
    
    def generate_signal(self, pair):
        """Generate high-confidence trading signal"""
        df = self.data_engine.get_realtime_data(pair)
        df = add_all_ta_features(df, open="open", high="high", low="low", close="close", volume="volume")
        
        # Feature engineering
        features = self.create_features(df)
        sequence = self.create_sequence(df)
        
        # Model predictions
        breakout_prob = self.models['breakout_detector'].predict_proba([features])[0][1]
        trend_pred = self.models['trend_predictor'].predict(sequence)[0]
        
        # Sentiment factor
        sentiment = self.data_engine.get_news_sentiment(pair)
        
        # Signal calculation
        buy_confidence = 0.4*trend_pred[0] + 0.4*breakout_prob + 0.2*sentiment
        sell_confidence = 0.4*trend_pred[1] + 0.4*breakout_prob + 0.2*abs(sentiment)
        
        if buy_confidence > 0.85 and self.is_valid_breakout(df):
            return ('BUY', buy_confidence)
        elif sell_confidence > 0.85 and self.is_valid_breakout(df):
            return ('SELL', sell_confidence)
        
        return ('HOLD', 0)
    
    def create_features(self, df):
        """Feature engineering for ML models"""
        last = df.iloc[-1]
        return np.array([
            last['rsi'],
            last['macd'],
            last['volume_adi'],
            last['bollinger_hband'] - last['close'],
            last['bollinger_lband'] - last['close'],
            last['atr']
        ])
    
    def create_sequence(self, df):
        """Create time sequence for LSTM"""
        return df[['close', 'volume', 'rsi', 'macd']].iloc[-30:].values.reshape(1, 30, 4)
    
    def is_valid_breakout(self, df):
        """Validate breakout with volume and volatility"""
        last = df.iloc[-1]
        return (last['volume'] > 1.8 * df['volume'].rolling(20).mean().iloc[-1] and
                (last['close'] > last['bollinger_hband'] or 
                 last['close'] < last['bollinger_lband']))
