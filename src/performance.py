import pandas as pd
from datetime import datetime

class PerformanceTracker:
    def __init__(self):
        self.trades = pd.DataFrame(columns=[
            'timestamp', 'pair', 'direction', 'confidence', 
            'amount', 'profit', 'duration', 'success'
        ])
        self.daily_profit = 0.0
        self.starting_balance = 1000.0
        self.current_balance = self.starting_balance
        
    def record_trade(self, trade_result):
        """Record a completed trade"""
        self.trades = self.trades.append(trade_result, ignore_index=True)
        self.current_balance += trade_result['profit']
        if trade_result['timestamp'].date() == datetime.now().date():
            self.daily_profit += trade_result['profit']
    
    def get_win_rate(self):
        """Calculate current win rate"""
        if len(self.trades) == 0:
            return 0.0
        wins = self.trades[self.trades['success']]
        return len(wins) / len(self.trades)
    
    def get_profit_factor(self):
        """Calculate profit factor"""
        wins = self.trades[self.trades['success']]
        losses = self.trades[~self.trades['success']]
        if len(losses) == 0:
            return 99.99
        return wins['profit'].sum() / abs(losses['profit'].sum())
    
    def daily_report(self):
        """Generate daily performance report"""
        today = datetime.now().date()
        daily_trades = self.trades[self.trades['timestamp'].dt.date == today]
        
        if len(daily_trades) == 0:
            return "No trades today."
        
        win_rate = len(daily_trades[daily_trades['success']]) / len(daily_trades)
        profit = daily_trades['profit'].sum()
        
        return f"""
📊 *Daily Performance Report*
════════════════════════════
• Trades: {len(daily_trades)}
• Win Rate: {win_rate:.1%}
• Profit: ${profit:.2f}
• Balance: ${self.current_balance:.2f}
• Profit Factor: {self.get_profit_factor():.2f}
════════════════════════════
"""

    def save_to_csv(self):
        """Save trade history to CSV"""
        self.trades.to_csv('data/trade_history.csv', index=False)
