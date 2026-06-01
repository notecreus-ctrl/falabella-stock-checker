import requests
import os

SKU_ID = os.environ["SKU_ID"]
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

FALABELLA_URL = "https://www.falabella.com/falabella-cl/product/" + SKU_ID + "/ascended-heroes-booster-bund-pokemon/" + SKU_ID
LIDER_URL = "https://www.lider.cl/ip/juegos-de-mesa/caja-coleccion-caja-de-entrenador-elite-ascended-heroes-en-ingles/00019621413247"

def check_falabella():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-CL,es;q=0.9",
        "Referer": "https://www.falabella.com/"
    }
    r = requests.get(FALABELLA_URL, headers=headers)
    text = r.text
    if "schema.org/InStock" in text:
        print("FALABELLA DISPONIBLE")
        notify("Pokemon Ascended Heroes disponible en Falabella! " + FALABELLA_URL)
    elif "schema.org/OutOfStock" in text:
        print("Falabella sin stock")
    else:
        print("Falabella: no se pudo determinar")

def check_lider():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-CL,es;q=0.9",
        "Referer": "https://www.lider.cl/"
    }
    r = requests.get(LIDER_URL, headers=headers)
    print("Lider status: " + str(r.status_code))
    keywords = ["sin stock", "agotado", "agregar al carro", "add-to-cart", "instock", "outofstock", "availability"]
    for kw in keywords:
        idx = r.
