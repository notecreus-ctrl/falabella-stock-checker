import requests, os

SKU_ID = os.environ["SKU_ID"]
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
URL = f"https://www.falabella.com/falabella-cl/product/{SKU_ID}/ascended-heroes-booster-bund-pokemon/{SKU_ID}"

def check_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-CL,es;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.falabella.com/"
    }
    r = requests.get(URL, headers=headers)
    print(f"Status: {r.status_code}")
    
    text = r.text.lower()
    print(f"Primeros 1000 chars: {r.text[:1000]}")

    sin_stock = "sin stock" in text or "agotado" in text or "no disponible" in text
    con_stock = "agregar al carro" in text or "añadir al carro" in text or "comprar" in text

    print(f"Sin stock: {sin_stock} - Con stock: {con_stock}")

    if con_stock and not sin_stock:
        notify(f"✅ Pokemon Ascended Heroes está disponible!\n{URL}")
    else:
        print("Sin stock por ahora")

def notify(msg):
    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
