import requests, os

SKU_ID = os.environ["SKU_ID"]
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def check_stock():
    url = f"https://www.falabella.com/s/browse/v1/product/cl/{SKU_ID}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36",
        "Accept": "application/json",
        "Referer": "https://www.falabella.com/"
    }
    r = requests.get(url, headers=headers)
    print(f"Status: {r.status_code}")
    print(f"Respuesta: {r.text[:800]}")

    data = r.json()
    product = data.get("data", {})
    
    if not product:
        print("No se encontró el producto")
        return

    name = product.get("displayName", "Producto")
    skus = product.get("skus", [])
    available = any(s.get("availabilityText", "").lower() == "disponible" for s in skus)
    
    print(f"Producto: {name} - Disponible: {available}")
    
    if available:
        notify(f"✅ {name} está disponible!\nfalabella.com/falabella-cl/product/{SKU_ID}")
    
def notify(msg):
    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": msg}
    )

check_stock()
