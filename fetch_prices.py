import ccxt
import pandas as pd
from datetime import datetime

EXCHANGES = {
    "binance": "BTCUSDT",
    "bybit": "BTCUSDT",
    "okx": "BTC-USDT",
    "kucoin": "BTC-USDT",
    "mexc": "BTCUSDT",
    "bitget": "BTCUSDT",
    "bitmex": "XBTUSD",
    "bitbank": "btc_jpy",
    "gmocoin": "BTC_JPY",
    "hyperliquid": "BTC",
}

TIMEFRAMES = ["1h", "1d"]


def fetch_ohlcv(exchange_name: str, symbol: str, timeframe: str):
    """Fetch OHLCV data using ccxt."""
    if not hasattr(ccxt, exchange_name):
        raise ValueError(f"Exchange '{exchange_name}' not supported by ccxt")

    exchange = getattr(ccxt, exchange_name)({"enableRateLimit": True})
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe)
    # convert to DataFrame
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


def main():
    for name, symbol in EXCHANGES.items():
        for tf in TIMEFRAMES:
            try:
                df = fetch_ohlcv(name, symbol, tf)
                print(f"{name} {symbol} {tf}:")
                print(df.tail())
            except Exception as e:
                print(f"Error fetching {name} {symbol} {tf}: {e}")


if __name__ == "__main__":
    main()
