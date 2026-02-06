from binance import AsyncClient
from binance.enums import (
    SIDE_BUY,
    SIDE_SELL,
    ORDER_TYPE_MARKET,
    ORDER_TYPE_LIMIT,
    TIME_IN_FORCE_GTC
)
from bot.logging_config import LogManager
ORDER_TYPE_STOP_MARKET = "STOP_MARKET"

class Orders:
    def __init__(self, client: AsyncClient):
        log_manager = LogManager()
        self.logger = log_manager.get_logger("OrderManager")
        self.client = client

    async def place_market_order(self, symbol: str, side: str, quantity: float):
        try:
            order = await self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            self.logger.info(f"Market order placed: {order}")
            return order
        except Exception as e:
            self.logger.exception("Error placing market order")
            raise

    async def place_limit_order(self, symbol: str, side: str, quantity: float, price: float):
        try:
            order = await self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price
            )
            self.logger.info(f"Limit order placed: {order}")
            return order
        except Exception as e:
            self.logger.exception("Error placing limit order")
            raise

    async def place_stop_market_order(self, symbol: str, side: str, quantity: float, stop_price: float):
        try:
            order = await self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_STOP_MARKET,
                quantity=quantity,
                stopPrice=stop_price
            )
            self.logger.info(f"Stop‑market order placed: {order}")
            return order
        except Exception as e:
            self.logger.exception("Error placing stop‑market order")
            raise