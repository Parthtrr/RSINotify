import requests
import time
from rsi_scanner import scan_rsi

# -------- TELEGRAM SETTINGS --------

BOT_TOKEN = "8790765430:AAEkYhJ7SZBYo1cGZLI7unnmzwh2xUbzqFg"
CHAT_ID = "7936542416"

URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# -------- LOOP --------

while True:

    signals = scan_rsi()

    if signals:

        for msg in signals:

            data = {
                "chat_id": CHAT_ID,
                "text": msg
            }

            response = requests.post(URL, data=data)

            print(response.text)

    else:
        print("No Buy Signals")

    time.sleep(600)