import requests
import json
import os
import time

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message):

    if not TELEGRAM_TOKEN:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)


def load_sites():

    with open("sites.json") as f:
        return json.load(f)


def load_uptime():

    if not os.path.exists("uptime.json"):
        return {}

    with open("uptime.json") as f:
        return json.load(f)


def save_uptime(data):

    with open("uptime.json", "w") as f:
        json.dump(data, f)


def check_site(url):

    try:

        r = requests.get(url, timeout=10)

        if r.status_code == 200:
            return True

    except:
        pass

    return False


def main():

    sites = load_sites()

    uptime = load_uptime()

    for site in sites:

        print("Checking", site)

        ok = check_site(site)

        if site not in uptime:
            uptime[site] = {"up":0,"down":0}

        if ok:
            uptime[site]["up"] += 1
            print("UP")

        else:
            uptime[site]["down"] += 1
            print("DOWN")

            send_telegram(f"⚠️ Website DOWN: {site}")

    save_uptime(uptime)


if __name__ == "__main__":
    main()
