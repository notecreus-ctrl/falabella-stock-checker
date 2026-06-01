import requests
import os

SKU_ID = os.environ["SKU_ID"]
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

FALABELLA_URL = "https://www.falabella.com/falabella-cl/product/" + SKU_ID + "/ascended-heroes-booster-bund-pokemon/" + SKU_ID
LIDER_URL = "https://www.lider.cl/ip/juegos-de-mesa/caja-coleccion-caja-de-entrenador-elite-ascended-heroes-en-ingles/00019621413247"

def check_falabella():
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.falabella.com/"}
    r = requests.get(FALABELLA_URL, headers=headers)
    if "schema.org/InStock" in r.text:
        print("FALABELLA DISPONIBLE")
        notify("Falabella: Ascended Heroes disponible! " + FALABELLA_URL)
    elif "schema.org/OutOfStock" in r.text:
        print("Falabella sin stock")
    else:
        print("Falabella: no determinado")

def check_lider():
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.lider.cl/"}
    r = requests.get(LIDER_URL, headers=headers)
    print("Lider status: " + str(r.status_code))
    text = r.text.lower()
    words = ["sin stock", "agotado", "agregar al carro", "add-to-cart", "instock", "outofstock", "availability"]
    for kw in words:
        idx = text.find(kw)
        if idx != -1:
            print("'" + kw + "': " + r.text[max(0,idx-30):idx+80])

def notify(msg):
    requests.get("https://api.telegram.org/bot" + TOKEN + "/sendMessage", params={"chat_id": CHAT_ID, "text": msg})

check_falabella()
check_lider()
