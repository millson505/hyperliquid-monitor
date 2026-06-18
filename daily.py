import requests

ETF_URL = "https://sosovalue.com/_next/data/KWchX1um_BW_mW00I76Pl/assets/etf/us-hype-spot.json"

r = requests.get(ETF_URL, timeout=30)
j = r.json()

print(type(j["pageProps"]["historyData"]))
print(j["pageProps"]["historyData"])

exit()
