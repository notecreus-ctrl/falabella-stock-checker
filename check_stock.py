import requests
import os
import re

SKU_ID = os.environ["SKU_ID"]
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

FALABELLA_URL = "https://www.falabella.com/falabella-cl/product/" + SKU_ID + "/ascended-heroes-booster-bund-pokemon/" + SKU_ID
FALABELLA_ETB_URL = "https://www.falabella.com/falabella-cl/product/152020461/pokemon-tcg-ascended-heroes-elite-trainer-box-ingles/152020462"
LIDER_URL1 = "https://www.lider.cl/ip/juegos-de-mesa/caja-coleccion-caja-de-entrenador-elite-ascended-heroes-en-ingles/00019621413247"
LIDER_URL2 = "https://www.lider.cl/ip/juegos-de-mesa/caja-de-sobres-paquete-de-refuerzo-de-ascended-heroes/00019621414150"
LIDER_URL3 = "https://www.lider.cl/ip/juegos-de-mesa/juego-de-cartas-pokemon-prismatic-evolutio-etb-english/00019621410513"
SEARCH_URL = "https://www.falabella.com/falabella-cl/search?Ntt=Ascended+heroes"
COUNT_FILE = "last_count.txt"

def check_falabella(nombre, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-CL,es;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.falabella.com/"
    }
    r = requests.get(url, headers=headers)
    if '"isOutOfStock":true' in r.text:
        print(nombre + " sin stock")
    elif '"isOutOfStock":false' in r.text:
        print(nombre + " DISPONIBLE")
        notify(nombre + " disponible! " + url)
    else:
        print(nombre + " no determinado")

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

def check_search_count():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-CL,es;q=0.9",
        "Referer": "https://www.falabella.com/"
    }
    r = requests.get(SEARCH_URL, headers=headers)
    matches = re.findall(r'"productId"', r.text)
    current_count = len(matches)
    print("Productos en busqueda Falabella: " + str(current_count))

    last_count = None
    if os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, "r") as f:
            content = f.read().strip()
            if content:
                last_count = int(content)

    print("Conteo anterior: " + str(last_count))

    if last_count is not None and current_count != last_count:
        if current_count > last_count:
            notify("ALERTA Falabella: aumentaron productos Ascended Heroes (" + str(last_count) + " -> " + str(current_count) + "). Revisa: " + SEARCH_URL)
        else:
            notify("ALERTA Falabella: bajaron productos Ascended Heroes (" + str(last_count) + " -> " + str(current_count) + "). Revisa: " + SEARCH_URL)

    with open(COUNT_FILE, "w") as f:
        f.write(str(current_count))

def notify(msg):
    requests.get("https://api.telegram.org/bot" + TOKEN + "/sendMessage", params={"chat_id": CHAT_ID, "text": msg})

check_falabella("Falabella Booster Bundle", FALABELLA_URL)
check_falabella("Falabella ETB Ingles", FALABELLA_ETB_URL)
check_lider("ETB Ingles", LIDER_URL1)
check_lider("Sobres", LIDER_URL2)
check_lider("Prismatic ETB", LIDER_URL3)
check_search_count()
notify("Prueba de sonido")
