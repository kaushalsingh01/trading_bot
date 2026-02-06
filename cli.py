import argparse
import asyncio
from bot.client import ClientManager
from bot.orders import Orders

async def main():
    parser = argparse.ArgumentParser(description="Trading Bot CLI")

    parser.add_argument("--symbol", type=str, required=True, help="Trading pair symbol (e.g. BTCUSDT)")
    parser.add_argument("--side", type=str, choices=["BUY", "SELL"], required=True, help="Order side")
    parser.add_argument("--quantity", type=float, required=True, help="Order quantity")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--market", action="store_true", help="Place a market order")
    group.add_argument("--limit", action="store_true", help="Place a limit order")
    group.add_argument("--stop", action="store_true", help="Place a stop‑market order")

    parser.add_argument("--price", type=float, help="Price for limit order")
    parser.add_argument("--stop-price", type=float, help="Stop price for stop‑market order")

    args = parser.parse_args()

    manager = await ClientManager.create()
    orders = Orders(manager.client)

    try:
        if args.market:
            order = await orders.place_market_order(args.symbol, args.side, args.quantity)
            print(order)

        elif args.limit:
            if not args.price:
                raise ValueError("Price is required for limit orders")
            order = await orders.place_limit_order(args.symbol, args.side, args.quantity, args.price)
            print(order)

        elif args.stop:
            if not args.stop_price:
                raise ValueError("Stop price is required for stop‑market orders")
            order = await orders.place_stop_market_order(args.symbol, args.side, args.quantity, args.stop_price)
            print(order)

    finally:
        await manager.close()

if __name__ == "__main__":
    asyncio.run(main())