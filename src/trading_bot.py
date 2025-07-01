import time
import requests
from .ai_predictor import AIPredictor
from .risk_manager import RiskManager
from .performance import PerformanceTracker
from .telegram_bot import TelegramBot

class TradingBot:
    def __init__(self):
        self.ai = AIPredictor()
        self.risk = RiskManager()
        self.performance = PerformanceTracker()
        self.telegram = TelegramBot()
        self.active_trades = {}
        
    def run(self):
        """Main trading loop"""
        while True:
            for pair in config.TRADING_PAIRS:
                signal, confidence = self.ai.generate_signal(pair)
                
                if signal != 'HOLD' and self.risk.can_trade():
                    trade_size = self.risk.calculate_size(confidence)
                    self.execute_trade(pair, signal, confidence, trade_size)
            
            # Check open trades
            self.check_trade_results()
            
            # Daily performance report
            if self.is_report_time():
                self.send_performance_report()
                
            time.sleep(30)  # Check every 30 seconds
    
    def execute_trade(self, pair, direction, confidence, amount):
        """Execute trade via Pocket Option API"""
        try:
            # Pocket Option API call
            url = "https://api.pocketoption.com/api/trade"
            payload = {
                "symbol": pair.replace("/", ""),
                "amount": amount,
                "timeframe": 1,  # 1-minute trade
                "direction": direction.lower(),
                "token": config.POCKET_OPTION_TOKEN
            }
            response = requests.post(url, data=payload).json()
            
            if response['success']:
                trade_id = response['data']['trade_id']
                self.active_trades[trade_id] = {
                    'pair': pair,
                    'direction': direction,
                    'confidence': confidence,
                    'amount': amount,
                    'open_time': time.time()
                }
                self.telegram.send_trade_alert(pair, direction, confidence, amount)
        except Exception as e:
            self.telegram.send_alert(f"🚨 Trade Error: {str(e)}")
    
    def check_trade_results(self):
        """Check completed trades"""
        for trade_id in list(self.active_trades.keys()):
            if time.time() - self.active_trades[trade_id]['open_time'] > 70:  # 1m + 10s buffer
                result = self.get_trade_result(trade_id)
                self.performance.record_trade(result)
                del self.active_trades[trade_id]
    
    def get_trade_result(self, trade_id):
        """Retrieve trade outcome"""
        url = f"https://api.pocketoption.com/api/history/{trade_id}"
        response = requests.get(url).json()
        return {
            'profit': response['data']['profit'],
            'success': response['data']['profit'] > 0
        }
    
    def send_performance_report(self):
        """Send daily summary to Telegram"""
        report = self.performance.daily_report()
        self.telegram.send_report(report)
