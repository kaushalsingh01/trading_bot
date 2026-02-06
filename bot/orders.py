from binance import AsyncClient
from bot.logging_config import LogManager

class Orders:
    def __init__(self, client:AsyncClient):
        log_manager = LogManager
        self.logger = log_manager.get_logger("OrderManager")
        self.client = client
    
    async def  place_market_order(self, symbol:str, side:str, quantity:float):
        try: 
            order = await self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity
            )
            self.logger.info(f"Market order placed: {order}")
            return order
        except Exception as e:
            self.logger.exception("Error placing market order")
            raise
    
    async def place_limit_order(self, symbol:str, side:str, qunatity:float, price:float):
        try:
            order = await self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                timeInForce="GTC",
                qunatity=qunatity,
                price=price
            )
            self.logger.info(f"Limit order placed: {order}")
            return order
        except Exception as e:
            self.logger.exception("Error placing limit order")
            raise
        