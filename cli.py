import asyncio
from InquirerPy import inquirer
from bot.client import ClientManager
from bot.orders import Orders
from binance.exceptions import BinanceAPIException
from bot.validators import (
    validate_symbol, validate_side, validate_quantity,
    validate_price, validate_stop_price
)

def print_order_summary(symbol, side, qty, order_type, price=None, stop_price=None):
    print("\n=== Order Request Summary ===")
    print(f"Symbol     : {symbol}")
    print(f"Side       : {side}")
    print(f"Quantity   : {qty}")
    print(f"Order Type : {order_type}")
    if price:
        print(f"Limit Price: {price}")
    if stop_price:
        print(f"Stop Price : {stop_price}")

def print_order_response(order):
    print("\n=== Order Response Details ===")
    print(f"Order ID     : {order.get('orderId')}")
    print(f"Status       : {order.get('status')}")
    print(f"Executed Qty : {order.get('executedQty')}")
    if 'avgPrice' in order:
        print(f"Average Price: {order.get('avgPrice')}")

def print_order_result(order):
    if order:
        print("\n Order placed successfully!")
    else:
        print("\n Order failed.")


async def main():
    manager = await ClientManager.create()
    orders = Orders(manager.client)

    exchange_info = await manager.client.futures_exchange_info()
    valid_symbols = [s["symbol"] for s in exchange_info["symbols"]]

    try:
        while True:
            choice = await inquirer.select(
                message="Main Menu:",
                choices=["Place Order", "Check Balance", "Exit"],
            ).execute_async()

            if choice == "Place Order":
                order_type = await inquirer.select(
                    message="Select order type:",
                    choices=["Market", "Limit", "Stop-Market"],
                ).execute_async()

                try:
                    symbol = validate_symbol(
                        await inquirer.text(message="Enter symbol (e.g. BTCUSDT):").execute_async(),
                        valid_symbols
                    )
                    side = validate_side(await inquirer.select(message="Side:", choices=["BUY", "SELL"]).execute_async())
                    qty = validate_quantity(float(await inquirer.text(message="Quantity:").execute_async()))

                    if order_type == "Market":
                        print_order_summary(symbol, side, qty, "MARKET")
                        order = await orders.place_market_order(symbol, side, qty)
                        if order:
                            print_order_response(order)
                        print_order_result(order)

                    elif order_type == "Limit":
                        price = validate_price(float(await inquirer.text(message="Limit price:").execute_async()))
                        print_order_summary(symbol, side, qty, "LIMIT", price=price)
                        order = await orders.place_limit_order(symbol, side, qty, price)
                        if order:
                            print_order_response(order)
                        print_order_result(order)

                    elif order_type == "Stop-Market":
                        stop_price = float(await inquirer.text(message="Stop price:").execute_async())
                        ticker = await manager.client.futures_symbol_ticker(symbol=symbol)
                        current_price = float(ticker["price"])
                        stop_price = validate_stop_price(stop_price, current_price)

                        print_order_summary(symbol, side, qty, "STOP-MARKET", stop_price=stop_price)
                        order = await orders.place_stop_market_order(symbol, side, qty, stop_price)
                        if order:
                            print_order_response(order)
                        print_order_result(order)

                except ValueError as ve:
                    print(f"\n Input validation error: {ve}")

                except BinanceAPIException as e:
                    if e.code == -4164:
                        print("\n Order rejected: Notional must be ≥ 100 USDT.")
                    elif e.code == -2021:
                        print("\n Invalid stop price: it would immediately trigger at current market.")
                    elif e.code == -2019:
                        print("\n Margin insufficient: not enough balance to place this order.")
                    elif e.code == -2015:
                        print("\n Invalid API key or permissions. Check Futures trading is enabled.")
                    elif e.code == -1121:
                        print("\n Invalid symbol. Please enter a valid trading pair like BTCUSDT.")
                    else:
                        print(f"\n Binance API error {e.code}: {e.message}")

            elif choice == "Check Balance":
                try:
                    balances = await manager.client.futures_account_balance()
                    print("\n=== Futures Account Balance ===")
                    print(f"{'Asset':<8} {'Balance':<15} {'Available':<15}")
                    print("-" * 40)
                    for asset in balances:
                        print(f"{asset['asset']:<8} {asset['balance']:<15} {asset['availableBalance']:<15}")
                except BinanceAPIException as e:
                    print(f"\nFailed to fetch balance. Binance API error {e.code}: {e.message}")

            elif choice == "Exit":
                break

    finally:
        await manager.close()


if __name__ == "__main__":
    asyncio.run(main())