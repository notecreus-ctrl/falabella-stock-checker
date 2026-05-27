import requests, os

SKU_ID = os.environ["SKU_ID"]
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def check_stock():
    # Intentamos con dos endpoints distintos
    urls = [
        f"https://www.falabella.com/s/browse/v1/listing/cl?skuId={SKU_ID}",
        f"https://www.falabella.com/s/browse/v1/listing/cl?productId={SKU_ID}",
    ]
    
    for url in urls:
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36",
            "Accept": "application/json",
            "Referer": "https://www.falabella.com/"
        }
        r = requests.get(url, headers=headers)
        print(f"Status: {r.status_code} - URL: {url}")
        print(f"Respuesta: {r.text[:500]}")  # imprime los primeros 500 caracteres
        
        data = r.json()
        results = data.get("data", {}).get("results", [])
        if results:
            product = results[0]
            name = product.get("displayName", "Producto")
            available = product.get("quantityAvailable", 0)
            print(f"Producto: {name} - Stock: {available}")
            if available > 0:
                notify(f"✅ {name} está disponible!\nfalabella.com/falabella-cl/product/{SKU_ID}")
            return

    print("No se encontró el producto en ningún endpoint")

def notify(msg):
    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": msg}
    )

check_stock()
