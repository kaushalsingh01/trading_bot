import asyncio
import argparse
from bot.client import ClientManager
from bot.orders import OrderManager

async def main():
    parser = argparse.ArgumentParser(description="Trading Bot CLI")
    parser.add_argument("--market", action="store_true", help="Place a market order")
    parser.add_argument("--limit", action="store_true", help="Place a limit order")
    parser.add_argument("--symbol", type=str, required=True, help="Trading pair symbol (e.g. BTCUSDT)")
    parser.add_argument("--side", type=str, choices=["BUY", "SELL"], required=True, help="Order side")
    parser.add_argument("--quantity", type=float, required=True, help="Order quantity")
    parser.add_argument("--price", type=float, help="Price for limit order")

    args = parser.parse_args()

    manager = await ClientManager.create()
    order_manager = OrderManager(manager.client)

    if args.market:
        order = await order_manager.place_market_order(args.symbol, args.side, args.quantity)
        print(order)

    elif args.limit:
        if not args.price:
            raise ValueError("Price is required for limit orders")
        order = await order_manager.place_limit_order(args.symbol, args.side, args.quantity, args.price)
        print(order)

    await manager.close()

if __name__ == "__main__":
    asyncio.run(main())