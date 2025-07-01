import pandas as pd
from datetime import datetime

class PerformanceTracker:
    def __init__(self):
        self.trades = []
        self.daily_profit = 0.0
        self.starting_balance = 1000.0  # Adjust as needed
        self.current_balance = self.starting_balance

    def record_trade(self, trade_result):
        """Record a completed trade"""
        self.trades.append({
            'timestamp': datetime.now(),
            'pair': trade_result.get('pair', 'N/A'),
            'direction': trade_result.get('direction', 'N/A'),
            'amount': trade_result.get('amount', 0),
            'profit': trade_result.get('profit', 0),
            'confidence': trade_result.get('confidence', 0),
            'success': trade_result.get('success', False)
        })
        self.current_balance += trade_result['profit']
        self.daily_profit += trade_result['profit']

    def daily_report(self):
        """Generate a daily performance report"""
        if not self.trades:
            return "No trades today."
        
        today_trades = [t for t in self.trades if t['timestamp'].date() == datetime.now().date()]
        win_count = sum(1 for t in today_trades if t['success'])
        loss_count = len(today_trades) - win_count
        win_rate = win_count / len(today_trades) * 100 if today_trades else 0
        total_profit = sum(t['profit'] for t in today_trades)
        avg_profit = total_profit / len(today_trades) if today_trades else 0
        
        return f"""
📅 *Daily Performance Report*
--------------------------------
• Trades: {len(today_trades)}
• Win Rate: {win_rate:.1f}%
• Profit: ${total_profit:.2f}
• Balance: ${self.current_balance:.2f}
• Avg. Profit/Trade: ${avg_profit:.2f}
        """

    def reset_daily(self):
        """Reset daily metrics (call at market close)"""
        self.daily_profit = 0.0
