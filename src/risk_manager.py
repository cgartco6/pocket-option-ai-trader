class RiskManager:
    def __init__(self, balance=1000):
        self.balance = balance
        self.daily_loss = 0
        self.trade_count = 0
        self.last_trade = None
        
    def calculate_size(self, confidence):
        """Dynamic position sizing"""
        base_size = min(50, self.balance * 0.02)  # Max $50 or 2%
        return base_size * (0.5 + confidence)  # Scale with confidence
        
    def can_trade(self):
        """Check trading conditions"""
        # Avoid over-trading
        if self.trade_count > config.MAX_TRADES_PER_HOUR:
            return False
            
        # Prevent chasing losses
        if self.daily_loss > config.MAX_DAILY_LOSS * self.balance:
            return False
            
        # Minimum time between trades
        if self.last_trade and time.time() - self.last_trade < 60:
            return False
            
        return True
    
    def update_balance(self, profit):
        """Update after trade completion"""
        self.balance += profit
        if profit < 0:
            self.daily_loss += abs(profit)
        self.trade_count += 1
        self.last_trade = time.time()
