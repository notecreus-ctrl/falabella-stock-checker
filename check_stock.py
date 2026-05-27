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
    text = r.text.lower()

    # Buscar fragmentos clave alrededor de palabras de stock
    keywords = ["sin stock", "agotado", "agregar al carro", "add-to-cart", "addtocart", "out-of-stock", "outofstock", "availability"]
    for kw in keywords:
        idx = text.find(kw)
        if idx != -1:
            print("ENCONTRADO '" + kw + "': ...'" + r.text[max(0,idx-50):idx+100] + "'...")

check_stock()
