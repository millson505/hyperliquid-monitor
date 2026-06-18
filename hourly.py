import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

r = requests.post(
    "https://api.hyperliquid.xyz/info",
    json={"type": "metaAndAssetCtxs"},
    timeout=30
)

data = r.json()

universe = data[0]["universe"]
ctxs = data[1]

msg = "📈 HYPE Monitor\n\n"

for i, asset in enumerate(universe):

    if asset["name"] == "HYPE":

        ctx = ctxs[i]

        funding = float(ctx["funding"]) * 100
        oi = float(ctx["openInterest"])

        if oi >= 1_000_000_000:
            oi_text = f"{oi/1_000_000_000:.2f}B"
        elif oi >= 1_000_000:
            oi_text = f"{oi/1_000_000:.2f}M"
        else:
            oi_text = f"{oi:,.0f}"

        msg += (
            f"Funding: {funding:.4f}%\n"
            f"OI: {oi_text}"
        )

        break

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

resp = requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": msg
    },
    timeout=30
)

print(resp.text)
