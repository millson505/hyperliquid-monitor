import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

message = """
📊 Hyperliquid Daily

Revenue: 조회예정
Buyback: 조회예정

HYPE ETF Flow: 조회예정
7D ETF Flow: 조회예정
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": message
    }
)
