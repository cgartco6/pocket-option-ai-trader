import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import joblib

# Load and preprocess historical data
def load_data(pair):
    df = pd.read_csv(f'data/historical/{pair.replace("/", "_")}.csv')
    df = add_all_ta_features(df)
    return df

# Feature engineering
def create_features(df):
    features = df[['rsi', 'macd', 'volume_adi', 'bollinger_hband', 'bollinger_lband', 'atr']]
    labels = np.where(df['close'].shift(-1) > df['close'], 1, 0)
    return features[:-1], labels[:-1]

# Train breakout detection model
def train_breakout_model(X, y):
    model = GradientBoostingClassifier(n_estimators=500, learning_rate=0.01)
    model.fit(X, y)
    joblib.dump(model, f'models/production/breakout_model_{pair}.pkl')
    return model

# Train LSTM trend model
def train_lstm_model(X, y):
    X = X.values.reshape((X.shape[0], 1, X.shape[1]))
    
    model = Sequential([
        LSTM(64, input_shape=(X.shape[1], X.shape[2])),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(loss='binary_crossentropy', optimizer='adam')
    model.fit(X, y, epochs=100, batch_size=32, verbose=1)
    model.save(f'models/production/lstm_trend_{pair}.h5')
    return model

# Main training function
def train_all_models():
    pairs = ["USD_ZAR", "USD_TRY", "EUR_TRY", "GBP_ZAR"]
    
    for pair in pairs:
        print(f"Training models for {pair}")
        df = load_data(pair)
        X, y = create_features(df)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        # Train and save models
        train_breakout_model(X_train, y_train)
        train_lstm_model(X_train, y_train)
        print(f"Completed training for {pair}")

if __name__ == "__main__":
    train_all_models()
