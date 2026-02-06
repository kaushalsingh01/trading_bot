def validate_symbol(symbol: str, valid_symbols: list[str]) -> str:
    symbol = symbol.strip().upper()
    if symbol not in valid_symbols:
        raise ValueError(f"Invalid symbol: {symbol}. Must be one of {', '.join(valid_symbols[:10])}...")
    return symbol

def validate_side(side: str) -> str:
    side = side.strip().upper()
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be either BUY or SELL.")
    return side

def validate_quantity(quantity: float) -> float:
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
    return quantity

def validate_price(price: float) -> float:
    if price <= 0:
        raise ValueError("Price must be greater than 0.")
    return price

def validate_stop_price(stop_price: float, current_price: float) -> float:
    if stop_price <= 0:
        raise ValueError("Stop price must be greater than 0.")
    if abs(stop_price - current_price) < 1: 
        raise ValueError("Stop price too close to current market; would immediately trigger.")
    return stop_price