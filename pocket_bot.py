import os
import asyncio
from pocket_option import PocketOption

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Pocket Option
PO_SESSION = os.getenv("PO_SESSION")
PO_UID = os.getenv("PO_UID")

ASSETS = [
    "EURUSD_otc",
    "AUDUSD_otc",
    "USDJPY_otc",
    "EURCHF_otc",
    "GBPUSD_otc",
]

async def main():
    client = PocketOption(
        ssid=PO_SESSION,
        uid=PO_UID
    )

    await client.connect()

    print("Pocket Option collegato.")

    while True:
        for asset in ASSETS:
            try:
                candles = await client.get_candles(asset, 60, 50)

                if candles:
                    print(asset, candles[-1])

            except Exception as e:
                print(f"{asset}: {e}")

        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
