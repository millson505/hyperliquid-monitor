import requests

r = requests.get(
    "https://sosovalue.com/_next/data/KWchX1um_BW_mW00I76Pl/assets/etf/us-hype-spot.json"
)

data = r.json()

print(data.keys())
print(data["pageProps"].keys())
