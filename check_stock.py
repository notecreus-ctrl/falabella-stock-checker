import requests
import os

SKU_ID = os.environ["SKU_ID"]
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

RIPLEY_URL = "https://simple.ripley.cl/cartas-pokemon-ascended-heroes-elite-box-en-2000411014267p"

def check_ripley():
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://simple.ripley.cl/"}
    r = requests.get(RIPLEY_URL, headers=headers)
    print("Ripley status: " + str(r.status_code))
    words = ["sin stock", "agotado", "agregar al carro", "add-to-cart", "instock", "outofstock", "schema.org"]
    text = r.text.lower()
    for kw in words:
        idx = text.find(kw)
        if idx != -1:
            print("'" + kw + "': " + r.text[max(0,idx-30):idx+80])

def notify(msg):
    requests.get("https://api.telegram.org/bot" + TOKEN + "/sendMessage", params={"chat_id": CHAT_ID, "text": msg})

check_ripley()
