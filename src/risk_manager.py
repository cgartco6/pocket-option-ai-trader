class RiskManager:
    # Initial risk parameters
    RISK_PER_TRADE = 1.0  # 1% of account
    MAX_DAILY_RISK = 5.0  # 5% max daily loss
   
    def adjust_risk():
    """Increase risk after profit milestones"""
    if balance > 200 and balance <= 500:
        return 1.5
    elif balance > 500 and balance <= 1000:
        return 2.0
    elif balance > 1000:
        return 2.5
    return 1.0
    
    def set_oco_orders(self, trade_id):
    # Set 80% take profit and 50% stop loss
    tp_url = f"https://api.pocketoption.com/orders/take_profit"
    sl_url = f"https://api.pocketoption.com/orders/stop_loss"
    
    payload = {
        "trade_id": trade_id,
        "percent": 80  # 80% of potential profit
    }
    requests.post(tp_url, json=payload)
    
    payload["percent"] = 50  # 50% stop loss
    requests.post(sl_url, json=payload)
   
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
