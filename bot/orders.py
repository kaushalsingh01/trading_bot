from binance import AsyncClient
from binance.enums import (
    SIDE_BUY,
    SIDE_SELL,
    ORDER_TYPE_MARKET,
    ORDER_TYPE_LIMIT,
    TIME_IN_FORCE_GTC
)
from bot.logging_config import LogManager
from binance.exceptions import BinanceAPIException

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
        except BinanceAPIException as e:
            self._handle_api_exception(e, "Market order")
            return None

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
        except BinanceAPIException as e:
            self._handle_api_exception(e, "Limit order")
            return None

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
        except BinanceAPIException as e:
            self._handle_api_exception(e, "Stop‑market order")
            return None

    def _handle_api_exception(self, e: BinanceAPIException, context: str):
        if e.code == -4164:
            self.logger.error(f"{context} rejected: Notional must be ≥ 100 USDT.")
        elif e.code == -2021:
            self.logger.error(f"{context} rejected: Stop price would immediately trigger.")
        elif e.code == -2019:
            self.logger.error(f"{context} rejected: Insufficient margin.")
        elif e.code == -2015:
            self.logger.error(f"{context} rejected: Invalid API key or permissions.")
        else:
            self.logger.error(f"{context} failed. Binance API error {e.code}: {e.message}")