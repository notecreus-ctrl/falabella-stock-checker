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
    matches = re.findall(r'falabella-cl/product/[^"&\s<>]+', r.text)
    seen = set()
    for m in matches:
        if m not in seen:
            seen.add(m)
            print(m)

check_search()
