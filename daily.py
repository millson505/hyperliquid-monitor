import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# ===== HYPE ETF =====

ETF_URL = "https://sosovalue.com/_next/data/KWchX1um_BW_mW00I76Pl/assets/etf/us-hype-spot.json"

r = requests.get(ETF_URL, timeout=30)
data = r.json()

etf_data = data["pageProps"]["data"]["list"]

latest = etf_data[0]

flow_1d = float(latest["totalNetInflow"])
aum = float(latest["totalNetAssets"])

flow_7d = 0

for row in etf_data[:7]:
    flow_7d += float(row["totalNetInflow"])

flow_1d_m = flow_1d / 1_000_000
flow_7d_m = flow_7d / 1_000_000
aum_m = aum / 1_000_000

# ===== HYPE OI =====

r = requests.post(
    "https://api.hyperliquid.xyz/info",
    json={"type": "metaAndAssetCtxs"},
    timeout=30
)

data = r.json()

universe = data[0]["universe"]
ctxs = data[1]

funding = None
oi = None

for i, asset in enumerate(universe):

    if asset["name"] == "HYPE":

        ctx = ctxs[i]

        funding = float(ctx["funding"]) * 100
        oi = float(ctx["openInterest"])

        break

if oi >= 1_000_000_000:
    oi_text = f"{oi/1_000_000_000:.2f}B"
elif oi >= 1_000_000:
    oi_text = f"{oi/1_000_000:.2f}M"
else:
    oi_text = f"{oi:,.0f}"

msg = f"""
📊 Hyperliquid Daily

HYPE Funding
{funding:.4f}%

HYPE OI
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
