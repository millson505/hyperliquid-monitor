import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

r = requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": "테스트"
    }
)

print(r.text)
