import requests

r = requests.get("https://sosovalue.com/_next/data/KWchX1um_BW_mW00I76Pl/assets/etf/us-hype-spot.json")

print(type(r.json()))
print(r.json())
exit()
