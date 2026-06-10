import requests
import os

SKU_ID = os.environ["SKU_ID"]
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

FALABELLA_URL = "https://www.falabella.com/falabella-cl/product/" + SKU_ID + "/ascended-heroes-booster-bund-pokemon/" + SKU_ID
LIDER_URL1 = "https://www.lider.cl/ip/juegos-de-mesa/caja-coleccion-caja-de-entrenador-elite-ascended-heroes-en-ingles/00019621413247"
LIDER_URL2 = "https://www.lider.cl/ip/juegos-de-mesa/caja-de-sobres-paquete-de-refuerzo-de-ascended-heroes/00019621414150"

def check_falabella():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-CL,es;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.falabella.com/"
    }
    r = requests.get(FALABELLA_URL, headers=headers)
    words = ["outofstock", "instock", "isOutOfStock", "addToCart", "soldOut", "sin-stock", "quantityAvailable", "stockStatus"]
    for kw in words:
        idx = r.text.find(kw)
        if idx != -1:
            print("'" + kw + "': " + r.text[max(0,idx-50):idx+150])

def check_lider(nombre, url):
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.lider.cl/"}
    r = requests.get(url, headers=headers)
    if "schema.org/InStock" in r.text:
        print(nombre + " DISPONIBLE")
        notify("Lider: " + nombre + " disponible! " + url)
    elif "schema.org/OutOfStock" in r.text:
        print(nombre + " sin stock")
    else:
        print(nombre + " no determinado")

def notify(msg):
    requests.get("https://api.telegram.org/bot" + TOKEN + "/sendMessage", params={"chat_id": CHAT_ID, "text": msg})

check_falabella()
check_lider("ETB Ingles", LIDER_URL1)
check_lider("Sobres", LIDER_URL2)
