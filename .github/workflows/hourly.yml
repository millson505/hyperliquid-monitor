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
ctxs = data[1]

WATCHLIST = ["HYPE", "HYNIX"]

msg = "📈 Funding Monitor\n\n"

for coin in WATCHLIST:
    found = False

    for i, asset in enumerate(universe):
        if asset["name"] == coin:
            ctx = ctxs[i]

            funding = float(ctx["funding"]) * 100
            oi = ctx["openInterest"]

            msg += (
                f"{coin}\n"
                f"Funding: {funding:.4f}%\n"
                f"OI: {oi}\n\n"
            )

            found = True
            break

    if not found:
        msg += f"{coin}\nNot Found\n\n"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

resp = requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": msg
    }
)

print(resp.text)
