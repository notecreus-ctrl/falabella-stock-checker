import requests
import os

SKU_ID = os.environ["SKU_ID"]
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
URL = "https://www.falabella.com/falabella-cl/product/" + SKU_ID + "/ascended-heroes-booster-bund-pokemon/" + SKU_ID

def check_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-CL,es;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.falabella.com/"
    }
    r = requests.get(URL, headers=headers)
    text = r.text

    if "schema.org/OutOfStock" in text or "schema.org/InStock" in text:
        print("DISPONIBLE - enviando notificacion")
        notify("Pokemon Ascended Heroes esta disponible en Falabella! " + URL)
    elif "schema.org/OutOfStock" in text:
        print("Sin stock confirmado")
    else:
        print("No se pudo determinar el stock")
        print(r.text[:500])

def notify(msg):
    requests.get("https://api.telegram.org/bot" + TOKEN + "/sendMessage", params={"chat_id": CHAT_ID, "text": msg})

check_stock()
