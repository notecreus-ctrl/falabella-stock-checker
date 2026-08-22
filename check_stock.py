import requests
import os
import re

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
SKU_ID = os.environ["SKU_ID"]

SEARCH_URL = "https://www.falabella.com/falabella-cl/search?Ntt=Ascended+heroes"
TIMEOUT = 15

def check_search():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-CL,es;q=0.9",
        "Referer": "https://www.falabella.com/"
    }
    r = requests.get(SEARCH_URL, headers=headers, timeout=TIMEOUT)

    c1 = len(re.findall("falabella-cl/product/", r.text))
    c2 = r.text.count('"@type":"Product"')
    c3 = r.text.count("application/ld+json")
    c4 = r.text.count("&quot;@type&quot;:&quot;Product&quot;")
    c5 = r.text.count("&quot;url&quot;:&quot;https://www.falabella.com/falabella-cl/product/")

    print("falabella-cl/product/: " + str(c1))
    print('@type Product: ' + str(c2))
    print("ld+json: " + str(c3))
    print("&quot;@type&quot; Product: " + str(c4))
    print("&quot;url&quot; product: " + str(c5))

check_search()
