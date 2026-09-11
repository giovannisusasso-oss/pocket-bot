import os
import time
import requests

# =========================
# TELEGRAM
# =========================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# SCANNER SETTINGS
# =========================
SYMBOLS = ["BTCUSDT", "ETHUSDT", "XRPUSDT"]
INTERVAL = "1m"
CHECK_EVERY = 60


def telegram_message(text):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Telegram not configured:", text)
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=10
    )


def get_prices(symbol):
    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": INTERVAL,
        "limit": 50
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    return [float(candle[4]) for candle in data]


def ema(values, period):
    multiplier = 2 / (period + 1)

    result = values[0]

    for price in values[1:]:
        result = (price - result) * multiplier + result

    return result


def rsi(values, period=14):
    gains = []
    losses = []

    for i in range(1, len(values)):
        change = values[i] - values[i - 1]

        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    average_gain = sum(gains[-period:]) / period
    average_loss = sum(losses[-period:]) / period

    if average_loss == 0:
        return 100

    rs = average_gain / average_loss

    return 100 - (100 / (1 + rs))


def scan(symbol):
    prices = get_prices(symbol)

    current_price = prices[-1]

    ema9 = ema(prices, 9)
    ema21 = ema(prices, 21)
    current_rsi = rsi(prices)

    signal = "NO SIGNAL"

    if ema9 > ema21 and current_rsi > 50:
        signal = "🟢 CALL"

    elif ema9 < ema21 and current_rsi < 50:
        signal = "🔴 PUT"

    return (
        f"📊 SCANNER\n\n"
        f"Asset: {symbol}\n"
        f"Price: {current_price:.4f}\n"
        f"RSI: {current_rsi:.1f}\n"
        f"EMA 9: {ema9:.4f}\n"
        f"EMA 21: {ema21:.4f}\n\n"
        f"Signal: {signal}"
    )


def main():
    print("Independent scanner started...")

    telegram_message("🤖 Scanner started!")

    while True:
        for symbol in SYMBOLS:
            try:
                message = scan(symbol)

                print(message)
                telegram_message(message)

            except Exception as error:
                print("Error:", error)

        time.sleep(CHECK_EVERY)


if __name__ == "__main__":
    main()
