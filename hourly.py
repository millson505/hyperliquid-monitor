import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

r = requests.post(
    "https://api.hyperliquid.xyz/info",
    json={"type": "metaAndAssetCtxs"}
)

data = r.json()

universe = data[0]["universe"]

print("===== ALL SYMBOLS =====")
for asset in universe:
    print(asset["name"])
print("===== END =====")
