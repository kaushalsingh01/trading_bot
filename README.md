## Features
- Interactive **menu-driven CLI**.
- Supports **Market**, **Limit**, and **Stop-Market** orders.
- **Balance check** for Futures account.
- Input Validation
- Graceful error handling for common Binance API errors

---

## Installation

Clone the repository and install dependencies: (For Windows)

```bash
git clone https://github.com/yourusername/trading_bot.git
cd trading_bot
python -m venv .venv
source .venv/bin/activate 
pip install -r requirements.txt
```
---

## Configuration

1. Create a `.env` file with your Binance Testnet API keys:
   ```env
   API_KEY=your_api_key
   API_SECRET=your_api_secret
   ```

2. Ensure your account is enabled for **Futures Testnet trading**.

---

## How to Use?

Run the CLI:

```bash
python cli.py
```

You’ll see an interactive menu:

```
Main Menu:
> Place Order
  Check Balance
  Exit
```

### Example Workflows

**Market Order**
```
? Select order type: Market
? Enter symbol (e.g. BTCUSDT): ETHUSDT
? Side: BUY
? Quantity: 0.05
```

**Limit Order**
```
? Select order type: Limit
? Enter symbol (e.g. BTCUSDT): BTCUSDT
? Side: SELL
? Quantity: 0.003
? Limit price: 45000
```

**Stop-Market Order**
```
? Select order type: Stop-Market
? Enter symbol (e.g. BTCUSDT): ETHUSDT
? Side: BUY
? Quantity: 0.05
? Stop price: 1900
```

**Check Balance**
```
=== Futures Account Balance ===
USDT: 10000.0 (available: 10000.0)
```

---

## 📂 Project Structure

```
trading_bot/
│
├── bot/
│   ├── client.py          # client manager
│   ├── orders.py          # Order Logic
│   ├── logging_config.py  # Logger setup
|   ├── validators.py      # Input validatior 
│
├── cli.py             # CLI entry point
├── requirements.txt
└── README.md
```



