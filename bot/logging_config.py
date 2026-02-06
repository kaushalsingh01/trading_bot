import logging

class LogManager:
    def __init__(self, log_file: str = "trading_bot.log", level: int = logging.INFO):
        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("TradingBot")

    def get_logger(self, name: str = None):
        if name:
            return logging.getLogger(f"TradingBot.{name}")
        return self.logger