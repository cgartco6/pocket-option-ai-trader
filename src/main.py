import time
import yaml
from trading_bot import TradingBot

# Load configuration
with open('config/api_keys.yaml', 'r') as f:
    api_keys = yaml.safe_load(f)
with open('config/settings.yaml', 'r') as f:
    settings = yaml.safe_load(f)

# Set environment variables for configuration
class Config:
    TRADING_PAIRS = settings['trading']['pairs']
    TELEGRAM_TOKEN = api_keys['telegram']['token']
    TELEGRAM_CHANNEL = api_keys['telegram']['channel_id']
    POCKET_OPTION_TOKEN = api_keys['pocket_option']['token']
    MAX_TRADES_PER_HOUR = settings['signals']['max_trades_per_hour']
    MAX_DAILY_LOSS = settings['trading']['max_daily_loss']

if __name__ == "__main__":
    bot = TradingBot()
    bot.run()
