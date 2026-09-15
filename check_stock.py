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
LIDER_URL4 = "https://www.lider.cl/ip/juegos-de-mesa/coleccion-pokemon-coleccion-ascended-heroes-premium-poster-gardevoir-ingles/00082065050024"
LIDER_URL5 = "https://www.lider.cl/ip/figuras-de-accion-y-coleccionables/pokemon-151-poster-collection-ingles/00082065085316"
LIDER_URL6 = "https://www.lider.cl/ip/juegos-de-mesa/caja-con-poster-y-sobres-premium-poster-lucario-ascended-heroes-ingles/00019621414143"
LIDER_URL7 = "https://www.lider.cl/ip/juegos-de-mesa/pokemon-premium-poster-collection-mega-gardevoir-ingles/01019621414143"
LIDER_URL8 = "https://www.lider.cl/ip/juguetes-por-edad/pokemon-tcg-ascended-heroes-premium-poster-collection-ing-mega-gardevoir/00780544040607"
LIDER_URL9 = "https://super.lider.cl/ip/jugueteria/00019621414143"
LIDER_URL10 = "https://www.lider.cl/ip/juegos-de-mesa/disfruta-de-la-coleccion-premium-de-prismatic-evolution-ingles/00019621411280"
LIDER_URL11 = "https://www.lider.cl/ip/juegos-de-mesa/caja-de-sobres-con-figura-disfruta-de-la-coleccion-premium-de-prismatic-evolution-ingles/00019621411276"

SEARCH_FALABELLA_ASCENDED = "https://www.falabella.com/falabella-cl/search?Ntt=Ascended+heroes"

URLS_FILE = "last_urls.txt"
SOBRES_STATE_FILE = "sobres_state.txt"
TIMEOUT = 15

def check_falabella(nombre, url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "es-CL,es;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "https://www.falabella.com/"
        }
        r = requests.get(url, headers=headers, timeout=TIMEOUT)
        if '"isOutOfStock":true' in r.text:
            print(nombre + " sin stock")
        elif '"isOutOfStock":false' in r.text:
            print(nombre + " DISPONIBLE")
            notify(nombre + " disponible! " + url)
        else:
            print(nombre + " no determinado")
    except Exception as e:
        error = nombre + " error: " + str(e)
        print(error)
        notify("ERROR - " + error)

def check_lider(nombre, url):
    try:
        headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.lider.cl/"}
        r = requests.get(url, headers=headers, timeout=TIMEOUT)
        if "schema.org/InStock" in r.text:
            print(nombre + " DISPONIBLE")
            notify("Lider: " + nombre + " disponible! " + url)
        elif "schema.org/OutOfStock" in r.text:
            print(nombre + " sin stock")
        else:
            print(nombre + " no determinado")
    except Exception as e:
        error = nombre + " error: " + str(e)
        print(error)
        notify("ERROR - " + error)

def check_lider_sobres(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.lider.cl/"}
        r = requests.get(url, headers=headers, timeout=TIMEOUT)

        last_state = ""
        if os.path.exists(SOBRES_STATE_FILE):
            with open(SOBRES_STATE_FILE, "r") as f:
                last_state = f.read().strip()

        if "schema.org/InStock" in r.text:
            precio = None
            match = re.search(r'"price"\s*:\s*"?([\d]+)"?', r.text)
            if match:
                precio = int(match.group(1))
                print("Lider Sobres precio: " + str(precio))

            if precio is not None and precio <= 50000:
                current_state = "instock_normal"
                if last_state != "instock_normal":
                    notify("Lider: Sobres disponible a $" + str(precio) + "! " + url)
            elif precio is not None and precio > 50000:
                current_state = "instock_caro"
                if last_state != "instock_caro":
                    notify("Lider: Sobres disponible pero precio elevado $" + str(precio) + " (envio internacional)")
            else:
                current_state = "instock_sin_precio"
                if last_state != "instock_sin_precio":
                    notify("Lider: Sobres disponible (verificar precio)! " + url)

            print("Lider Sobres estado: " + current_state)

        elif "schema.org/OutOfStock" in r.text:
            current_state = "outofstock"
            print("Lider Sobres sin stock")
        else:
            current_state = last_state
            print("Lider Sobres no determinado")

        with open(SOBRES_STATE_FILE, "w") as f:
            f.write(current_state)

    except Exception as e:
        error = "Lider Sobres error: " + str(e)
        print(error)
        notify("ERROR - " + error)

def get_falabella_precio(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.falabella.com/"
        }
        r = requests.get(url, headers=headers, timeout=TIMEOUT)
        match = re.search(r'"originalPrice":(\d+)', r.text)
        if match:
            return int(match.group(1))
        match2 = re.search(r'"price":(\d+)', r.text)
        if match2:
            return int(match2.group(1))
        return None
    except:
        return None

def check_search_falabella(search_url, urls_file, keyword, nombre):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "es-CL,es;q=0.9",
            "Referer": "https://www.falabella.com/"
        }
        r = requests.get(search_url, headers=headers, timeout=30)
        matches = re.findall(r'falabella-cl/product/[^"&\s<>\\]+', r.text)
        seen = set()
        current_urls = set()
        for m in matches:
            m = m.split("\\u0026")[0].split("&")[0].strip()
            if m not in seen:
                seen.add(m)
                if keyword in m.lower() and "espanol" not in m.lower() and "español" not in m.lower():
                    current_urls.add(m)

        print(nombre + " URLs: " + str(len(current_urls)))

        last_urls = set()
        if os.path.exists(urls_file):
            with open(urls_file, "r") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line:
                        last_urls.add(line)

        nuevas = current_urls - last_urls
        if nuevas:
            for url in nuevas:
                precio = get_falabella_precio("https://www." + url)
                if precio:
                    notify("ALERTA " + nombre + ": nuevo producto a $" + str(precio) + "! https://www." + url)
                else:
                    notify("ALERTA " + nombre + ": nuevo producto! https://www." + url)

        with open(urls_file, "w") as f:
            for url in sorted(current_urls):
                f.write(url.strip() + "\n")

    except Exception as e:
        error = nombre + " busqueda error: " + str(e)
        print(error)
        notify("ERROR - " + error)

def notify(msg):
    try:
        requests.get("https://api.telegram.org/bot" + TOKEN + "/sendMessage", params={"chat_id": CHAT_ID, "text": msg}, timeout=TIMEOUT)
    except Exception as e:
        print("Notify error: " + str(e))

check_falabella("Falabella Booster Bundle", FALABELLA_URL)
check_falabella("Falabella ETB Ingles", FALABELLA_ETB_URL)
check_lider("ETB Ingles", LIDER_URL1)
check_lider_sobres(LIDER_URL2)
check_lider("Prismatic ETB", LIDER_URL3)
check_lider("Poster Gardevoir Ingles", LIDER_URL4)
check_lider("Pokemon 151 Poster Ingles", LIDER_URL5)
check_lider("Poster Lucario Ascended Ingles", LIDER_URL6)
check_lider("Poster Mega Gardevoir Ingles", LIDER_URL7)
check_lider("Poster Mega Gardevoir Ingles v2", LIDER_URL8)
check_lider("Lider Super Poster", LIDER_URL9)
check_lider("Prismatic Evolution Premium Ingles", LIDER_URL10)
check_lider("Prismatic Evolution Sobres Figura Ingles", LIDER_URL11)
check_search_falabella(SEARCH_FALABELLA_ASCENDED, URLS_FILE, "ascended", "Ascended Heroes Falabella")
