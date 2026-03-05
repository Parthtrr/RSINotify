import os
import requests
from rsi_scanner import scan_rsi

def send_telegram_message(bot_token: str, chat_id: str, text: str) -> None:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    resp = requests.post(url, data=data, timeout=30)
    resp.raise_for_status()

def main():
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID environment variables")

    signals = scan_rsi()

    if signals:
        for msg in signals:
            send_telegram_message(bot_token, chat_id, msg)
        print(f"Sent {len(signals)} signal(s).")
    else:
        print("No Buy Signals")

if __name__ == "__main__":
    main()
