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
    words = ["ascended", "pokemon", "results", "totalCount", "numFound", "productos", "booster", "trainer"]
    for kw in words:
        idx = r.text.lower().find(kw.lower())
        if idx != -1:
            print("'" + kw + "': " + r.text[max(0,idx-30):idx+150])

check_search()
