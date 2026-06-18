import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# =========================
# ETF DATA (SoSoValue)
# =========================

ETF_URL = "https://sosovalue.com/_next/data/KWchX1um_BW_mW00I76Pl/assets/etf/us-hype-spot.json"

r = requests.get(ETF_URL, timeout=30)
j = r.json()

history = j["pageProps"]["historyData"]["list"]

latest = history[0]

flow_1d = float(latest["totalNetInflow"])
aum = float(latest["totalNetAssets"])

flow_7d = sum(
    float(row["totalNetInflow"])
    for row in history[:7]
)

flow_1d_m = flow_1d / 1_000_000
flow_7d_m = flow_7d / 1_000_000
aum_m = aum / 1_000_000

# =========================
# DEFI LLAMA REVENUE
# =========================

REV_URL = "https://defillama.com/api/public/protocols/charts?kind=adapter&adapterType=fees&protocol=Hyperliquid"

rev = requests.get(REV_URL, timeout=30).json()

latest_rev = rev[-1][1]
revenue_m = latest_rev / 1_000_000

# =========================
# HYPERLIQUID DATA
# =========================

r = requests.post(
    "https://api.hyperliquid.xyz/info",
    json={"type": "metaAndAssetCtxs"},
    timeout=30
)

data = r.json()

universe = data[0]["universe"]
ctxs = data[1]

funding = 0
oi = 0

for i, asset in enumerate(universe):
    if asset["name"] == "HYPE":
        funding = float(ctxs[i]["funding"]) * 100
        oi = float(ctxs[i]["openInterest"])
        break

if oi >= 1_000_000_000:
    oi_text = f"{oi/1_000_000_000:.2f}B"
elif oi >= 1_000_000:
    oi_text = f"{oi/1_000_000:.2f}M"
else:
    oi_text = f"{oi:,.0f}"

# =========================
# MESSAGE
# =========================

msg = f"""📊 Hyperliquid Daily

Revenue (24h)
${revenue_m:.2f}M

Funding (8h)
{funding:.4f}%

OI
{oi_text}

ETF Flow (1D)
${flow_1d_m:.2f}M

ETF Flow (7D)
${flow_7d_m:.2f}M

ETF AUM
${aum_m:.2f}M
"""

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
