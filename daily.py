import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

msg = """
📊 Hyperliquid Daily

Revenue: TBD
Buyback: TBD

ETF Flow (1D): TBD
ETF Flow (7D): TBD
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

resp = requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": msg
    }
)

print(resp.text)
