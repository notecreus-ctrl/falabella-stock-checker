import requests
import os

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

RIPLEY_URL = "https://simple.ripley.cl/cartas-pokemon-ascended-heroes-elite-box-en-2000411014267p"

def check_ripley():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-CL,es;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Referer": "https://simple.ripley.cl/"
    }
    r = requests.get(RIPLEY_URL, headers=headers)
    print("Ripley status: " + str(r.status_code))
    if r.status_code == 200:
        words = ["sin stock", "agotado", "agregar al carro", "add-to-cart", "instock", "outofstock", "schema.org"]
        text = r.text.lower()
        for kw in words:
            idx = text.find(kw)
            if idx != -1:
                print("'" + kw + "': " + r.text[max(0,idx-30):idx+80])

def notify(msg):
    requests.get("https://api.telegram.org/bot" + TOKEN + "/sendMessage", params={"chat_id": CHAT_ID, "text": msg})

check_ripley()
