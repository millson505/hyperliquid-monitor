import os
import requests
for asset in universe: print(asset["name"])
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

r = requests.post(
    "https://api.hyperliquid.xyz/info",
    json={"type": "metaAndAssetCtxs"}
)

data = r.json()

universe = data[0]["universe"]
ctxs = data[1]

# 보고 싶은 종목
WATCHLIST = {
    "HYPE": "HYPE",
    "SKHX": "xyz:SKHXUSD"
}

msg = "📈 Funding Monitor\n\n"

for display_name, symbol in WATCHLIST.items():
    found = False

    for i, asset in enumerate(universe):
        if asset["name"] == symbol:
            ctx = ctxs[i]

            funding = float(ctx["funding"]) * 100
            oi = float(ctx["openInterest"])

            if oi >= 1_000_000_000:
                oi_text = f"{oi/1_000_000_000:.2f}B"
            elif oi >= 1_000_000:
                oi_text = f"{oi/1_000_000:.2f}M"
            elif oi >= 1_000:
                oi_text = f"{oi/1_000:.2f}K"
            else:
                oi_text = f"{oi:.0f}"

            msg += (
                f"{display_name}\n"
                f"Funding: {funding:.4f}%\n"
                f"OI: {oi_text}\n\n"
            )

            found = True
            break

    if not found:
        msg += f"{display_name}\nNot Found\n\n"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

resp = requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": msg
    }
)

print(resp.text)
