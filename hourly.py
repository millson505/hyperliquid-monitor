import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# ======================
# HYPERLIQUID
# ======================

r = requests.post(
    "https://api.hyperliquid.xyz/info",
    json={"type": "metaAndAssetCtxs"},
    timeout=30
)

data = r.json()

universe = data[0]["universe"]
ctxs = data[1]

hl_funding = 0
oi = 0

for i, asset in enumerate(universe):
    if asset["name"] == "HYPE":
        hl_funding = float(ctxs[i]["funding"]) * 100
        oi = float(ctxs[i]["openInterest"])
        break

# ======================
# BACKPACK
# ======================

bp = requests.get(
    "https://api.backpack.exchange/api/v1/markPrices",
    timeout=30
).json()

bp_funding = None

for item in bp:
    if item["symbol"] == "HYPE_USDC_PERP":
        bp_funding = float(item["fundingRate"]) * 100
        break

# ======================
# FORMAT
# ======================

if oi >= 1_000_000_000:
    oi_text = f"{oi/1_000_000_000:.2f}B"
elif oi >= 1_000_000:
    oi_text = f"{oi/1_000_000:.2f}M"
else:
    oi_text = f"{oi:,.0f}"

msg = f"""📈 HYPE Monitor

HL Funding (1h)
{hl_funding:.4f}%

Backpack Funding (1h)
{bp_funding:.4f}%

OI
{oi_text}
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": msg
    },
    timeout=30
)

# ======================
# FUNDING ALERT
# ======================

if abs(hl_funding) >= 0.05:

    alert = f"""🚨 HYPE Funding Alert

HL Funding
{hl_funding:.4f}%
"""

    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": alert
        },
        timeout=30
    )
