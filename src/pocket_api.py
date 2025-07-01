import requests
import time

class PocketOptionAPI:
    def __init__(self, api_token):
        self.base_url = "https://api.pocketoption.com"
        self.token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        })
    
    def place_trade(self, pair, amount, direction, duration=1):
        """Place a binary option trade"""
        payload = {
            "symbol": pair.replace("/", ""),
            "amount": amount,
            "timeframe": duration,
            "direction": direction.lower()
        }
        
        response = self.session.post(
            f"{self.base_url}/api/trade",
            json=payload
        )
        
        if response.status_code == 200:
            return response.json()
        return {"success": False, "error": response.text}
    
    def get_trade_result(self, trade_id):
        """Check trade outcome"""
        response = self.session.get(
            f"{self.base_url}/api/history/{trade_id}"
        )
        
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_balance(self):
        """Get current account balance"""
        response = self.session.get(
            f"{self.base_url}/api/account"
        )
        
        if response.status_code == 200:
            return response.json().get('balance', 0)
        return 0
