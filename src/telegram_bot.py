import telegram
from datetime import datetime

class TelegramBot:
    def __init__(self):
        self.bot = telegram.Bot(token=config.TELEGRAM_TOKEN)
        
    def send_trade_alert(self, pair, direction, confidence, amount):
        """Send real-time trade alert"""
        emoji = "🚀" if direction == "BUY" else "🔻"
        message = f"""
        {emoji} *AI Trade Executed* {emoji}
        ▬▬▬▬▬▬▬▬▬▬▬▬▬
        • Pair: `{pair}`
        • Direction: {direction}
        • Confidence: {confidence:.0%} 
        • Amount: ${amount}
        • Time: {datetime.now().strftime('%H:%M:%S')}
        """
        self.bot.send_message(
            chat_id=config.TELEGRAM_CHANNEL,
            text=message,
            parse_mode='Markdown'
        )
    
    def send_report(self, report):
        """Send performance report"""
        self.bot.send_message(
            chat_id=config.TELEGRAM_CHANNEL,
            text=f"📊 *Daily Report*\n{report}",
            parse_mode='Markdown'
        )
    
    def send_alert(self, message):
        """Send system alert"""
        self.bot.send_message(
            chat_id=config.TELEGRAM_CHANNEL,
            text=f"⚠️ {message}"
        )
