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

SEARCH_FALABELLA_ASCENDED = "https://www.falabella.com/falabella-cl/search?Ntt=Ascended+heroes"
SEARCH_FALABELLA_30TH = "https://www.falabella.com/falabella-cl/search?Ntt=pokemon+30th+celebration"
SEARCH_LIDER_30TH = "https://www.lider.cl/search?Ntt=pokemon+30th+celebration"
SEARCH_RIPLEY_30TH = "https://simple.ripley.cl/search?query=pokemon+30th+celebration"
SEARCH_ANSALDO_30TH = "https://ansaldo.cl/search?q=pokemon+30th+celebration"

URLS_FILE = "last_urls.txt"
URLS_30TH_FALABELLA_FILE = "last_urls_30th_falabella.txt"
URLS_30TH_LIDER_FILE = "last_urls_30th_lider.txt"
URLS_30TH_RIPLEY_FILE = "last_urls_30th_ripley.txt"
URLS_30TH_ANSALDO_FILE = "last_urls_30th_ansaldo.txt"
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
        matches = re.findall(r'falabella-cl/product/[^"&\s<>]+', r.text)
        seen = set()
        current_urls = set()
        for m in matches:
            if m not in seen:
                seen.add(m)
                if keyword in m.lower():
                    current_urls.add(m.strip())

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

def check_search_lider_30th():
    try:
        headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.lider.cl/"}
        r = requests.get(SEARCH_LIDER_30TH, headers=headers, timeout=30)
        matches = re.findall(r'href="(/ip/[^"]+)"', r.text)
        seen = set()
        current_urls = set()
        for m in matches:
            if m not in seen:
                seen.add(m)
                if "30th-celebration" in m.lower():
                    current_urls.add(m.strip())

        print("Lider 30th URLs: " + str(len(current_urls)))

        last_urls = set()
        if os.path.exists(URLS_30TH_LIDER_FILE):
            with open(URLS_30TH_LIDER_FILE, "r") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line:
                        last_urls.add(line)

        nuevas = current_urls - last_urls
        if nuevas:
            for url in nuevas:
                notify("ALERTA Lider 30th: nuevo producto! https://www.lider.cl" + url)

        with open(URLS_30TH_LIDER_FILE, "w") as f:
            for url in sorted(current_urls):
                f.write(url.strip() + "\n")

    except Exception as e:
        error = "Lider 30th error: " + str(e)
        print(error)
        notify("ERROR - " + error)

def check_search_ripley_30th():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
            "Accept-Language": "es-CL,es;q=0.9",
            "Referer": "https://simple.ripley.cl/"
        }
        r = requests.get(SEARCH_RIPLEY_30TH, headers=headers, timeout=30)
        print("Ripley 30th status: " + str(r.status_code))

        if r.status_code == 200:
            matches = re.findall(r'href="(/[^"]*30th-celebration[^"]*)"', r.text, re.IGNORECASE)
            seen = set()
            current_urls = set()
            for m in matches:
                if m not in seen:
                    seen.add(m)
                    current_urls.add(m.strip())

            print("Ripley 30th URLs: " + str(len(current_urls)))

            last_urls = set()
            if os.path.exists(URLS_30TH_RIPLEY_FILE):
                with open(URLS_30TH_RIPLEY_FILE, "r") as f:
                    for line in f.readlines():
                        line = line.strip()
                        if line:
                            last_urls.add(line)

            nuevas = current_urls - last_urls
            if nuevas:
                for url in nuevas:
                    notify("ALERTA Ripley 30th: nuevo producto! https://simple.ripley.cl" + url)

            with open(URLS_30TH_RIPLEY_FILE, "w") as f:
                for url in sorted(current_urls):
                    f.write(url.strip() + "\n")

    except Exception as e:
        error = "Ripley 30th error: " + str(e)
        print(error)
        notify("ERROR - " + error)

def check_search_ansaldo_30th():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://ansaldo.cl/"
        }
        r = requests.get(SEARCH_ANSALDO_30TH, headers=headers, timeout=30)
        print("Ansaldo 30th status: " + str(r.status_code))

        matches = re.findall(r'href="(https://ansaldo\.cl/products/[^"]+)"', r.text)
        seen = set()
        current_urls = set()
        for m in matches:
            if m not in seen:
                seen.add(m)
                if "30th-celebration" in m.lower():
                    current_urls.add(m.strip())

        print("Ansaldo 30th URLs: " + str(len(current_urls)))

        last_urls = set()
        if os.path.exists(URLS_30TH_ANSALDO_FILE):
            with open(URLS_30TH_ANSALDO_FILE, "r") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line:
                        last_urls.add(line)

        nuevas = current_urls - last_urls
        if nuevas:
            for url in nuevas:
                precio_match = re.search(r'"price":"([\d.]+)"', r.text)
                precio = int(float(precio_match.group(1))) if precio_match else None
                if precio:
                    notify("ALERTA Ansaldo 30th: nuevo producto a $" + str(precio) + "! " + url)
                else:
                    notify("ALERTA Ansaldo 30th: nuevo producto! " + url)

        with open(URLS_30TH_ANSALDO_FILE, "w") as f:
            for url in sorted(current_urls):
                f.write(url.strip() + "\n")

    except Exception as e:
        error = "Ansaldo 30th error: " + str(e)
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
check_search_falabella(SEARCH_FALABELLA_ASCENDED, URLS_FILE, "ascended", "Ascended Heroes Falabella")
check_search_falabella(SEARCH_FALABELLA_30TH, URLS_30TH_FALABELLA_FILE, "30th-celebration", "30th Falabella")
check_search_lider_30th()
check_search_ripley_30th()
check_search_ansaldo_30th()


def find_asmodee():
    try:
        r = requests.get("https://api.mercadolibre.com/sites/MLC/search?q=pokemon+etb&nickname=ASMODEE", timeout=TIMEOUT)
        data = r.json()
        print("Asmodee status: " + str(r.status_code))
        print("Total resultados: " + str(data.get("paging", {}).get("total", 0)))
        if data.get("results"):
            seller = data["results"][0].get("seller", {})
            print("Seller ID: " + str(seller.get("id")))
            print("Seller nickname: " + str(seller.get("nickname")))
    except Exception as e:
        print("Asmodee error: " + str(e))

find_asmodee()
