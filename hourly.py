import os
import json
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

STATE_FILE = "oi_state.json"

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

# ======================
# OI CHANGE
# ======================

prev_oi = None

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        prev_oi = json.load(f).get("oi")

with open(STATE_FILE, "w") as f:
    json.dump({"oi": oi}, f)

oi_change_text = "N/A"

if prev_oi is not None:

    diff = oi - prev_oi

    sign = "+" if diff >= 0 else ""

    oi_change_text = f"{sign}{diff/1_000_000:.2f}M"

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

Funding (8h)
{funding:.4f}%

OI
{oi_text}

OI Change
{oi_change_text}
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

if abs(funding) >= 0.05:

    alert = f"""🚨 HYPE Funding Alert

Funding (8h)
{funding:.4f}%
"""

    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": alert
        },
        timeout=30
    )
